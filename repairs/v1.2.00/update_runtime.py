"""Visible install/restart lifecycle with a receipt from the reopened app."""
from pathlib import Path
import json,os,subprocess,sys,time,traceback,uuid

def run_worker(root,folder,u):
    import tkinter as tk
    from tkinter import ttk
    root=Path(root).resolve();folder=Path(folder).resolve()
    request=json.loads((folder/'request.json').read_text(encoding='utf-8'))
    sessions=u.stage_root(root)/'sessions';sessions.mkdir(parents=True,exist_ok=True)
    win=tk.Tk();win.title('NestSimple Money Repair And Update');win.geometry('660x260');win.resizable(False,False)
    body=ttk.Frame(win,padding=20);body.pack(fill='both',expand=True)
    ttk.Label(body,text='Installing And Reopening NestSimple Money',font=('Segoe UI',15,'bold')).pack(anchor='w',pady=(0,14))
    status=ttk.Label(body,text='Checking the program and waiting for its windows to close...',wraplength=610);status.pack(anchor='w',pady=(0,12))
    actions=ttk.Frame(body);actions.pack(anchor='w',side='bottom')
    lock=None;child=None;stream=None;installed=False;finished=False
    log=folder/'restart.log';receipt=folder/'restart-ready.json';token=uuid.uuid4().hex
    def record(message):
        with (folder/'result.txt').open('a',encoding='utf-8') as output:output.write(message+'\n')
    def cleanup():
        nonlocal lock
        (sessions/'close-request.json').unlink(missing_ok=True)
        if lock is not None:lock.unlink(missing_ok=True);lock=None
    def close():
        if finished:win.destroy()
    def fail(message):
        nonlocal finished
        finished=True;cleanup();record('FAILED: '+message)
        status.configure(text=message+'\n\nDetails: '+str(folder/'result.txt'))
        if installed:retry.pack(side='left',padx=(0,12))
        done.pack(side='left')
    def callback_error(*error):
        record(''.join(traceback.format_exception(*error)))
        fail('The repair stopped before completion. See the saved details; household files were not replaced.')
    win.report_callback_exception=callback_error;win.protocol('WM_DELETE_WINDOW',close)
    def launch():
        nonlocal child,stream,finished
        finished=False;retry.pack_forget();done.pack_forget();receipt.unlink(missing_ok=True)
        environment=dict(os.environ,**request.get('environment',{}))
        environment.update(NESTSIMPLE_RESTART_RECEIPT=str(receipt),NESTSIMPLE_RESTART_TOKEN=token)
        # Keep the exact interpreter and household selected by the running app.
        command=[sys.executable,str(root/'launch.pyw')]
        record('Launching: '+json.dumps(command))
        try:
            stream=log.open('ab')
            child=subprocess.Popen(command,cwd=root,env=environment,stdout=stream,stderr=stream,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        except Exception as error:
            if stream:stream.close()
            fail('The program files were installed, but Windows could not start the app: '+str(error));return
        status.configure(text='Program files verified. Waiting for the reopened app to confirm it is ready...')
        deadline=time.monotonic()+30
        def check():
            nonlocal finished
            try:ready=json.loads(receipt.read_text(encoding='utf-8'))
            except (OSError,ValueError):ready={}
            if ready.get('token')==token and ready.get('pid')==child.pid and ready.get('version')==u.validate(root,folder)['to']:
                finished=True;stream.close();record('REOPENED: '+json.dumps(ready));status.configure(text='Repair complete. NestSimple Money reopened and confirmed version '+ready['version']+'.');win.after(1200,win.destroy);return
            if child.poll() is not None or time.monotonic()>=deadline:
                stream.close();record('Restart exit status: '+str(child.poll()))
                fail('The program files were installed, but the app did not confirm a successful start. Check any startup error window before choosing Retry Reopen.');return
            win.after(200,check)
        win.after(200,check)
    retry=ttk.Button(actions,text='Retry Reopen',command=launch)
    done=ttk.Button(actions,text='Close',command=close)
    def start():
        nonlocal lock,installed
        try:
            u.validate(root,folder);lock=u.acquire_lock(root)
            targets=request.get('sessions',[])
            (sessions/'close-request.json').write_text(json.dumps({'sessions':[s['token'] for s in targets]}),encoding='utf-8')
            deadline=time.monotonic()+40
            record('Waiting for sessions: '+json.dumps(targets))
        except Exception as error:fail('The repair could not start: '+str(error));return
        def wait():
            nonlocal installed
            if any(u.alive(s['pid']) for s in targets):
                if time.monotonic()<deadline:win.after(150,wait);return
                fail('A NestSimple Money process has not closed. No program files were changed. Close its windows and run the repair again.');return
            try:
                status.configure(text='Verifying the package and saving a program backup...');win.update_idletasks()
                backup=u.apply(root,folder);installed=True;record('INSTALLED: '+str(backup));cleanup()
            except Exception as error:fail('The update could not be installed: '+str(error));return
            launch()
        win.after(150,wait)
    win.after(200,start);win.mainloop()
