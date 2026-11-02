"""Installed, data-only package updater. Package code is never used as a runner."""
from pathlib import Path,PurePosixPath
import hashlib,json,os,shutil,stat,subprocess,sys,time,uuid,zipfile
import queue,re,threading,urllib.request,urllib.parse
from file_io import atomic_replace

LIMIT=100*1024*1024

def allowed(name):
    p=PurePosixPath(name)
    return bool(name and '\\' not in name and not p.is_absolute() and '..' not in p.parts and (len(p.parts)==1 and (p.suffix=='.py' or name in ('STYLE_GUIDE.md','AGENTS.md')) or len(p.parts)==2 and p.parts[0]=='assets' and p.suffix=='.png'))

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def stage_root(root):
    return Path(root).resolve().parent/'temp'/'program-updates'

def prepare(package,root):
    root=Path(root).resolve();folder=stage_root(root)/uuid.uuid4().hex;folder.mkdir(parents=True)
    try:
        with zipfile.ZipFile(package) as archive:
            members=archive.infolist();names=[m.filename for m in members]
            if len(names)!=len(set(names)) or sum(m.file_size for m in members)>LIMIT:raise ValueError('Update is too large or contains duplicate files.')
            manifest=json.loads(archive.read('manifest.json'))
            files=manifest['files']
            if not files or not isinstance(manifest.get('to'),str):raise ValueError('Invalid update manifest.')
            expected={'manifest.json','What Changed.html'}|{'payload/'+name for name in files}
            if set(names)!=expected:raise ValueError('Unexpected update contents.')
            for member in members:
                if stat.S_ISLNK(member.external_attr>>16):raise ValueError('Links are not allowed in updates.')
            for name in files:
                if not allowed(name):raise ValueError('This update contains a forbidden program path.')
            for member in members:
                path=folder/member.filename
                if not path.resolve().is_relative_to(folder):raise ValueError('Invalid update path.')
                path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(archive.read(member))
        validate(root,folder)
        return folder,manifest
    except Exception:
        shutil.rmtree(folder,ignore_errors=True);raise

def validate(root,folder):
    root=Path(root).resolve();folder=Path(folder);manifest=json.loads((folder/'manifest.json').read_text())
    if not (root/'app.py').is_file():raise ValueError('The program folder could not be found.')
    for name,entry in manifest['files'].items():
        if not allowed(name):raise ValueError('Forbidden update path.')
        target=root/name
        if not target.resolve().is_relative_to(root):raise ValueError('Update target is outside the program folder.')
        if digest(folder/'payload'/name)!=entry['new']:raise ValueError('An update file is damaged: '+name)
        actual=digest(target) if target.is_file() else None
        if actual not in entry['old']+[entry['new']]:raise ValueError('Program files differ from supported versions: '+name)
    return manifest

def file_operation(action):
    """Retry temporary file contention without bypassing Windows permissions."""
    for attempt in range(6):
        try:return action()
        except PermissionError:
            if attempt==5:raise
            time.sleep(0.2*(attempt+1))

class UpdateInstallError(OSError):
    pass

def replace_file(source,target):
    temporary=target.with_name(target.name+'.update-'+uuid.uuid4().hex)
    try:
        file_operation(lambda:shutil.copy2(source,temporary))
        file_operation(lambda:atomic_replace(temporary,target))
    finally:
        try:file_operation(lambda:temporary.unlink(missing_ok=True))
        except OSError:pass

def apply(root,folder):
    root=Path(root).resolve();folder=Path(folder);manifest=validate(root,folder)
    candidates=list(manifest['files'])+['What Changed.html']
    sources={name:folder/name if name=='What Changed.html' else folder/'payload'/name for name in candidates}
    names=[name for name in candidates if not (root/name).is_file() or digest(root/name)!=digest(sources[name])]
    backup=root/'program-update-backups'/('in-app-'+time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:6]);backup.mkdir(parents=True)
    existed={name:(root/name).is_file() for name in names}
    for name in names:
        if existed[name]:
            (backup/name).parent.mkdir(parents=True,exist_ok=True)
            file_operation(lambda name=name:shutil.copy2(root/name,backup/name))
            if digest(root/name)!=digest(backup/name):raise ValueError('Program backup verification failed: '+name)
    replaced=[]
    try:
        for name in names:
            target=root/name;target.parent.mkdir(parents=True,exist_ok=True)
            replaced.append(name);replace_file(sources[name],target)
            if digest(target)!=digest(sources[name]):raise ValueError('Installed file verification failed: '+name)
    except Exception as error:
        failures=[]
        for name in reversed(replaced):
            try:
                if existed[name]:
                    if (root/name).is_file() and digest(root/name)==digest(backup/name):continue
                    replace_file(backup/name,root/name)
                    if digest(root/name)!=digest(backup/name):raise ValueError('Restored file does not match backup')
                else:file_operation(lambda name=name:(root/name).unlink(missing_ok=True))
            except Exception as restore_error:failures.append(name+': '+str(restore_error))
        if failures:
            detail='Update failed: '+str(error)+'\nRestoration could not complete for:\n'+'\n'.join(failures)+'\nProgram backup: '+str(backup)+'\nDo not start the app until these program files are restored. Household data was not replaced.'
        else:detail='Update failed: '+str(error)+'\nPrevious program files were retained or restored and verified.\nProgram backup: '+str(backup)
        try:(folder/'result.txt').write_text(detail,encoding='utf-8')
        except OSError:pass
        raise UpdateInstallError(detail) from error
    (folder/'installed-files.txt').write_text('\n'.join(str(root/name) for name in names)+'\nBackup: '+str(backup),encoding='utf-8')
    return backup

def alive(pid):
    if sys.platform=='win32':
        import ctypes
        api=ctypes.windll.kernel32;api.OpenProcess.restype=ctypes.c_void_p
        handle=api.OpenProcess(0x100000,False,int(pid))
        if not handle:return api.GetLastError()==5
        try:return api.WaitForSingleObject(ctypes.c_void_p(handle),0)==258
        finally:api.CloseHandle(ctypes.c_void_p(handle))
    try:os.kill(int(pid),0);return True
    except ProcessLookupError:return False
    except PermissionError:return True

def acquire_lock(root):
    path=stage_root(root)/'apply.lock'
    for attempt in range(2):
        try:
            with path.open('x') as stream:stream.write(str(os.getpid()))
            return path
        except FileExistsError:
            try:pid=int(path.read_text())
            except (OSError,ValueError):raise ValueError('Another update is starting. Try again shortly.')
            if alive(pid):raise ValueError('Another update is already running.')
            path.unlink(missing_ok=True)
    raise ValueError('Could not obtain the program update lock.')

def active_sessions(root):
    """Read registered PID files only; close-request.json is a command, not a session."""
    sessions=stage_root(root)/'sessions';tokens=[]
    for entry in sessions.glob('*.json'):
        if not entry.stem.isascii() or not entry.stem.isdecimal():continue
        try:
            data=json.loads(entry.read_text())
        except FileNotFoundError:continue  # A window finished closing during enumeration.
        except (OSError,ValueError) as error:
            raise ValueError('Cannot read app session '+entry.name+'. Close all app windows and retry.') from error
        if (not isinstance(data,dict) or type(data.get('pid')) is not int
                or data['pid']<=0 or str(data['pid'])!=entry.stem
                or not isinstance(data.get('token'),str) or not data['token']):
            raise ValueError('Invalid app session '+entry.name+'. Close all app windows and retry.')
        if alive(data['pid']):tokens.append(data)
        else:entry.unlink(missing_ok=True)
    return tokens

def install_session(app,root=None):
    root=Path(root or Path(__file__).resolve().parent);sessions=stage_root(root)/'sessions';sessions.mkdir(parents=True,exist_ok=True)
    token=uuid.uuid4().hex;entry=sessions/(str(os.getpid())+'.json');entry.write_text(json.dumps({'pid':os.getpid(),'token':token}))
    def check():
        request=sessions/'close-request.json'
        try:targets=json.loads(request.read_text()).get('sessions',[]) if request.is_file() else []
        except (OSError,ValueError):targets=[]
        if token in targets:
            app.close();entry.unlink(missing_ok=True);return
        if app.winfo_exists():app.after(500,check)
    app.after(500,check)
    receipt=os.environ.pop('NESTSIMPLE_RESTART_RECEIPT',None)
    restart_token=os.environ.pop('NESTSIMPLE_RESTART_TOKEN',None)
    if receipt and restart_token:
        receipt=Path(receipt).resolve()
        if receipt.is_relative_to(stage_root(root).resolve()):
            def ready():
                if app.winfo_exists() and app.winfo_viewable():
                    temporary=receipt.with_suffix('.tmp')
                    temporary.write_text(json.dumps({'pid':os.getpid(),'version':CURRENT_VERSION,'token':restart_token}),encoding='utf-8')
                    os.replace(temporary,receipt)
                elif app.winfo_exists():app.after(100,ready)
            app.after(750,ready)

REPOSITORY='Shavastar/NestSimple-Money-Updates'
FEED_URL='https://raw.githubusercontent.com/'+REPOSITORY+'/main/latest.json'
CURRENT_VERSION='1.2.01'

def version_tuple(value):
    if not isinstance(value,str) or not re.fullmatch(r'\d+\.\d+\.\d+',value):raise ValueError('Invalid update version.')
    return tuple(map(int,value.split('.')))

def valid_download_url(url):
    parsed=urllib.parse.urlsplit(url)
    prefix='/'+REPOSITORY+'/main/packages/'
    return parsed.scheme=='https' and parsed.netloc=='raw.githubusercontent.com' and parsed.path.startswith(prefix) and parsed.path.endswith('.nsmupdate') and not parsed.query and not parsed.fragment and '..' not in parsed.path.split('/')

def read_feed(opener=None):
    opener=opener or urllib.request.urlopen
    request=urllib.request.Request(FEED_URL+'?check='+uuid.uuid4().hex,headers={'User-Agent':'NestSimple-Money-Updater','Cache-Control':'no-cache'})
    with opener(request,timeout=20) as response:
        raw=response.read(65537)
    if len(raw)>65536:raise ValueError('Update information is too large.')
    info=json.loads(raw)
    version_tuple(info.get('version'))
    if not valid_download_url(info.get('url','')):raise ValueError('Update download must be in the NestSimple update repository.')
    if not re.fullmatch('[0-9a-f]{64}',str(info.get('sha256',''))):raise ValueError('Missing update checksum.')
    if type(info.get('size')) is not int or not 0<info['size']<=LIMIT:raise ValueError('Invalid update size.')
    if not isinstance(info.get('changes'),list) or not all(isinstance(v,str) for v in info['changes']):raise ValueError('Invalid release notes.')
    return info

def download_update(info,root,opener=None,progress=None,phase=None):
    opener=opener or urllib.request.urlopen
    if not valid_download_url(info['url']):raise ValueError('Invalid update download address.')
    folder=stage_root(root)/'downloads';folder.mkdir(parents=True,exist_ok=True)
    target=folder/(uuid.uuid4().hex+'.nsmupdate');total=0;checksum=hashlib.sha256()
    try:
        if progress:progress(0,info['size'])
        request=urllib.request.Request(info['url'],headers={'User-Agent':'NestSimple-Money-Updater'})
        with opener(request,timeout=30) as response,target.open('wb') as out:
            while True:
                block=response.read(65536)
                if not block:break
                total+=len(block)
                if total>info['size'] or total>LIMIT:raise ValueError('Update download exceeds its expected size.')
                out.write(block);checksum.update(block)
                if progress:progress(total,info['size'])
        if phase:phase('verifying')
        if total!=info['size'] or checksum.hexdigest()!=info['sha256']:raise ValueError('The update download is incomplete or damaged.')
        if phase:phase('preparing')
        staged,manifest=prepare(target,root)
        if manifest['to']!=info['version']:
            shutil.rmtree(staged,ignore_errors=True);raise ValueError('Downloaded version does not match the update information.')
        return staged
    finally:target.unlink(missing_ok=True)

def download_progress(received,total):
    """Reserve completion for verified, prepared packages; never round up early."""
    percent=min(99,max(0,received*100//total)) if total else 0
    text=(f'Downloading: {percent}% — {received:,} / {total:,} bytes'
          if received<total else 'All bytes received. Waiting for download to finish...')
    return percent,text

def online_page(parent,app):
    from tkinter import ttk,messagebox
    root=Path(__file__).resolve().parent
    from layout import ScrollArea
    # Older installations have ScrollArea without a vertical_only constructor option.
    # Do not forward newer keywords into ttk.Frame on those installations.
    viewport=ScrollArea(parent,min_width=0,min_height=0)
    viewport.vertical_only=True
    viewport.pack(fill='both',expand=True)
    frame=ttk.Frame(viewport.content,padding=18);frame.pack(fill='both',expand=True)
    ttk.Label(frame,text='Program Updates',font=('Segoe UI',16,'bold')).pack(anchor='w',pady=(0,10))
    status=ttk.Label(frame,text='Checking GitHub for updates...',wraplength=700);status.pack(anchor='w',pady=(0,12))
    # Readiness must remain above variable-length release notes.
    notes=None
    controls=ttk.Frame(frame);controls.pack(anchor='w',pady=8)
    # Clam elements honour colour options even when Windows uses native themes.
    style=ttk.Style(frame)
    for element in ('trough','pbar'):
        name='UpdateDownload.Horizontal.Progressbar.'+element
        if name not in style.element_names():
            style.element_create(name,'from','clam','Horizontal.Progressbar.'+element)
    style.layout('UpdateDownload.Horizontal.TProgressbar',[
        ('UpdateDownload.Horizontal.Progressbar.trough',{'sticky':'nswe','children':[
            ('UpdateDownload.Horizontal.Progressbar.pbar',{'side':'left','sticky':'ns'})]})])
    style.configure('UpdateDownload.Horizontal.TProgressbar',background='#3B82C4',
                    lightcolor='#3B82C4',darkcolor='#3B82C4',bordercolor='#3B82C4',troughcolor='#E5E7EB')
    progress=ttk.Progressbar(frame,style='UpdateDownload.Horizontal.TProgressbar',mode='determinate',maximum=100);progress.pack(fill='x',pady=(4,0))
    progress_text=ttk.Label(frame,text='');progress_text.pack(anchor='w',pady=(2,8))
    results=queue.Queue();state={'info':None,'busy':False}
    def background(work):
        state['busy']=True;check.configure(state='disabled');download.configure(state='disabled');choose.configure(state='disabled')
        def run():
            try:results.put(('ok',work()))
            except Exception as error:results.put(('error',str(error)))
        threading.Thread(target=run,daemon=True).start();frame.after(100,poll)
    def poll():
        if not frame.winfo_exists():return
        try:poll_result()
        except Exception as error:
            state['busy']=False
            check.configure(state='normal');choose.configure(state='normal')
            if state['info']:download.configure(state='normal')
            status.configure(text='Update could not finish: '+str(error))
            progress_text.configure(text='Installation has not started. Retry or use the standalone repair installer.')
            messagebox.showerror('Update Could Not Finish',str(error),parent=app)
    def poll_result():
        try:kind,value=results.get_nowait()
        except queue.Empty:frame.after(100,poll);return
        # Coalesce queued byte reports so verification/readiness cannot wait
        # behind one UI callback per network block. Preserve phase/result order.
        while kind=='progress' and not results.empty():
            kind,value=results.get_nowait()
        if kind=='progress':
            percent,text=download_progress(*value)
            progress.configure(value=percent)
            progress_text.configure(text=text)
            frame.after(20,poll);return
        if kind=='phase':
            text={'verifying':'Download finished. Verifying size and checksum...',
                  'preparing':'Download verified. Preparing update files...',
                  'ready':'Download verified. Opening installation review...'}[value]
            progress_text.configure(text=text)
            frame.after(20,poll);return
        state['busy']=False;check.configure(state='normal');choose.configure(state='normal')
        if kind=='error':
            status.configure(text='Could not check or download the update. '+value)
            progress.configure(value=0);progress_text.configure(text='Not ready to install. Try again.')
            if state['info']:download.configure(state='normal')
            return
        if isinstance(value,Path):
            # Keep readiness and installation review on the download page.
            # A navigation/render exception must never silently end this callback.
            try:
                for child in review.winfo_children():child.destroy()
                update_page(review,app,value)
                progress.configure(value=100)
                progress_text.configure(text='100% — Update ready to install. Review below, then Apply Update and Restart.')
                status.configure(text='Download verified. Installation has not started.')
            except Exception as error:
                status.configure(text='Could not open installation review: '+str(error))
                progress.configure(value=0)
                progress_text.configure(text='Not ready to install. Choose Update File to retry.')
                download.configure(state='normal')
            return
        state['info']=None
        notes.configure(text='\n'.join(str(i)+'. '+text for i,text in enumerate(value['changes'],1)))
        if version_tuple(value['version'])>version_tuple(CURRENT_VERSION):
            state['info']=value;status.configure(text='Version '+value['version']+' is available. Installed version: '+CURRENT_VERSION+'.')
            download.configure(state='normal')
        else:status.configure(text='You are up to date. Installed version: '+CURRENT_VERSION+'.')
    def check_now():
        if state['busy']:return
        progress.configure(value=0);progress_text.configure(text='')
        state['info']=None;status.configure(text='Checking GitHub for updates...');background(read_feed)
    def download_now():
        if state['busy'] or not state['info']:return
        progress.configure(value=0);progress_text.configure(text='Starting download...')
        info=state['info'];status.configure(text='Downloading and checking version '+info['version']+'...')
        background(lambda:download_update(info,root,progress=lambda received,total:results.put(('progress',(received,total))),
                                          phase=lambda step:results.put(('phase',step))))
    check=ttk.Button(controls,text='Check Again',command=check_now);check.pack(side='left',padx=(0,8))
    download=ttk.Button(controls,text='Download Update',command=download_now,state='disabled');download.pack(side='left',padx=(0,8))
    choose=ttk.Button(controls,text='Choose Update File',command=lambda:choose_update_file(app));choose.pack(side='left')
    review=ttk.Frame(frame);review.pack(fill='x')
    ttk.Label(frame,text='Program files and release notes come from Shavastar/NestSimple-Money-Updates. Household data stays on this computer. Installation requires a separate review and Apply Update and Restart.',wraplength=700).pack(anchor='w',pady=12)
    notes=ttk.Label(frame,text='',wraplength=700,justify='left');notes.pack(anchor='w',pady=(0,12))
    check_now()

def open_update(app):
    app.open_record('program_update','online')

def choose_update_file(app):

    from tkinter import filedialog,messagebox
    root=Path(__file__).resolve().parent
    path=filedialog.askopenfilename(parent=app,title='Select NestSimple Update',filetypes=[('NestSimple Update','*.nsmupdate')])
    if not path:return
    try:folder,manifest=prepare(path,root)
    except Exception as error:messagebox.showerror('Update Not Loaded',str(error),parent=app);return
    app.open_record('program_update',str(folder))

def stage_runner(folder):
    """Stage only the installed updater and its installed replacement helper."""
    folder=Path(folder);installed=Path(__file__).resolve().parent
    for source_name,target_name in (('file_io.py','file_io.py'),('update_runtime.py','update_runtime.py'),('program_updates.py','installed-updater.py')):
        source=installed/source_name;target=folder/target_name
        shutil.copy2(source,target)
        if digest(source)!=digest(target):raise ValueError('Updater staging verification failed: '+source_name)
    return folder/'installed-updater.py'

def update_page(parent,app,folder):
    import tkinter as tk
    from tkinter import ttk,messagebox
    if str(folder)=='online':return online_page(parent,app)
    folder=Path(folder);root=Path(__file__).resolve().parent;manifest=validate(root,folder)
    frame=ttk.Frame(parent,padding=18);frame.pack(fill='both',expand=True)
    ttk.Label(frame,text='Ready To Install — Version '+manifest['to'],font=('Segoe UI',16,'bold')).pack(anchor='w',pady=(0,12))
    controls=ttk.Frame(frame);controls.pack(anchor='w',pady=10)
    def apply_restart():
        apply_button.configure(state='disabled')
        try:
            tokens=active_sessions(root)
            (folder/'request.json').write_text(json.dumps({'sessions':tokens,'environment':{k:v for k,v in os.environ.items() if k in ('NESTSIMPLE_PROFILE_FILE','NESTSIMPLE_DEMO_WINDOW','NESTSIMPLE_DEMO_FOLDER')}}))
            runner=stage_runner(folder)
            subprocess.Popen([sys.executable,str(runner),'--apply',str(root),str(folder)],cwd=root,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        except Exception as error:
            apply_button.configure(state='normal');messagebox.showerror('Update Not Started','The update could not start. Your app remains open and no program or household files were changed.\n\nPlease retry. If this continues, use the standalone repair installer.\n\nDetails: '+str(error),parent=app)
    apply_button=ttk.Button(controls,text='Apply Update and Restart',command=apply_restart);apply_button.pack(side='left',padx=(0,8))
    if all((root/name).is_file() and digest(root/name)==entry['new'] for name,entry in manifest['files'].items()):
        apply_button.configure(state='disabled');ttk.Label(frame,text='This update is already installed.').pack(anchor='w',pady=8)
    ttk.Button(controls,text='Cancel',command=app.record_back).pack(side='left')
    ttk.Label(frame,text=f"{len(manifest['files'])} program files. A backup will be saved before changes.\nAll NestSimple Money windows will close, then this household will reopen.\nHousehold data, settings and testing edits are preserved.",wraplength=700).pack(anchor='w',pady=(0,12))

def worker(root,folder):
    from update_runtime import run_worker
    return run_worker(root,folder,sys.modules[__name__])

if __name__=='__main__' and len(sys.argv)==4 and sys.argv[1]=='--apply':worker(sys.argv[2],sys.argv[3])
