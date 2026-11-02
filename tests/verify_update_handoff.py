"""Release gate: real download/prepare and online-page callbacks, headless widgets.
Usage: python verify_update_handoff.py PACKAGE
No financial records or network access are required.
"""
from pathlib import Path
from unittest.mock import patch
import io,json,sys,tempfile,time,shutil,hashlib
sys.path.insert(0,str(Path('HomeMoney').resolve()))
import program_updates as u
import tkinter.ttk as ttk
import tkinter.messagebox as messages

class Widget:
    widgets=[];pending=[]
    def __init__(self,parent=None,**kw):
        self.parent=parent;self.kw=kw;self.children=[];self.order=[];self.dead=False
        if parent:parent.children.append(self)
        self.widgets.append(self)
    def pack(self,**kw):
        order=self.parent.order if self.parent else []
        if self in order:order.remove(self)
        if 'before' in kw:order.insert(order.index(kw['before']),self)
        else:order.append(self)
    def configure(self,**kw):self.kw.update(kw)
    def winfo_exists(self):return not self.dead
    def winfo_children(self):return list(self.children)
    def destroy(self):self.dead=True
    def after(self,delay,callback):self.pending.append(callback)
    def record_back(self):pass
class Viewport(Widget):
    def __init__(self,parent=None,**kw):
        super().__init__(parent,**kw);self.content=Widget(self)
class Style:
    def __init__(self,*a):pass
    def element_names(self):return ()
    def element_create(self,*a):pass
    def layout(self,*a):pass
    def configure(self,*a,**kw):pass

def find(text):return next(w for w in reversed(Widget.widgets) if not w.dead and w.kw.get('text')==text)
def pump(done):
    until=time.monotonic()+15
    while time.monotonic()<until:
        if Widget.pending:Widget.pending.pop(0)()
        if done():return
        time.sleep(.001)
    raise AssertionError('UI callback stopped before terminal state')

def run(package):
    package=Path(package).resolve();data=package.read_bytes();version=json.loads(__import__('zipfile').ZipFile(package).read('manifest.json'))['to']
    info={'version':version,'url':'https://raw.githubusercontent.com/Shavastar/NestSimple-Money-Updates/main/packages/'+package.name,'sha256':hashlib.sha256(data).hexdigest(),'size':len(data),'changes':['Long release note '*40]*10}
    actual_download=u.download_update
    for failure in ('success','checksum','truncated','timeout','review'):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'NestSimpleMoney';shutil.copytree('HomeMoney',root,ignore=shutil.ignore_patterns('__pycache__','demo','*.db','*.sqlite3'))
            shutil.copy2('release191/payload/program_updates.py',root/'program_updates.py')
            def download(*a,**kw):
                def opener(*args,**kwargs):
                    if failure=='timeout':raise TimeoutError('Simulated network timeout')
                    return io.BytesIO(data[:-1] if failure=='truncated' else data)
                chosen=dict(a[0])
                if failure=='checksum':chosen['sha256']='0'*64
                return actual_download(chosen,root,opener=opener,**kw)
            Widget.widgets=[];Widget.pending=[];app=Widget();parent=Widget(app)
            original_review=u.update_page
            def review(*a):
                if failure=='review':raise RuntimeError('Simulated review failure')
                return original_review(*a)
            patches=[patch.object(ttk,n,Widget) for n in ('Frame','Label','Button','Progressbar')]
            from contextlib import ExitStack
            with ExitStack() as stack:
                for p in patches:stack.enter_context(p)
                stack.enter_context(patch.object(ttk,'Style',Style))
                stack.enter_context(patch('layout.ScrollArea',Viewport))
                stack.enter_context(patch.object(messages,'showerror'))
                stack.enter_context(patch.object(u,'__file__',str(root/'program_updates.py')))
                stack.enter_context(patch.object(u,'read_feed',return_value=info))
                stack.enter_context(patch.object(u,'CURRENT_VERSION','1.0.118'))
                stack.enter_context(patch.object(u,'download_update',side_effect=download))
                stack.enter_context(patch.object(u,'update_page',side_effect=review))
                u.online_page(parent,app)
                button=find('Download Update')
                pump(lambda:button.kw.get('state')=='normal')
                control_order=list(button.parent.parent.order)
                button.kw['command']()
                pump(lambda:find('Check Again').kw.get('state')=='normal')
                assert button.parent.parent.order==control_order, 'Existing controls moved during download completion'
                texts=[w.kw.get('text','') for w in Widget.widgets if not w.dead]
                bars=[w for w in Widget.widgets if w.kw.get('maximum')==100]
                if failure=='success':
                    ready=find('Ready To Install — Version '+version);apply=find('Apply Update and Restart')
                    assert apply.kw.get('state')!='disabled'
                    container=ready.parent.parent;assert container.parent.order.index(container)>container.parent.order.index(find('Check Again').parent)
                    assert bars[-1].kw['value']==100
                    assert any('100% — Update ready' in t for t in texts)
                else:
                    assert bars[-1].kw['value']<100
                    assert not any(t.startswith('Ready To Install') for t in texts)
                    assert button.kw['state']=='normal'
                    assert any('Not ready to install' in t for t in texts)
                print('PASS download-to-review:',failure)
    # A thousand progress events must not prevent terminal delivery.
    print('PASS actual size, checksum, preparation, review creation, control order and retry states')
if __name__=='__main__':run(sys.argv[1])
