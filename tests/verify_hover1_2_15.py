from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
from testing_ui import HoverDismiss,pointer_over
class W:
 def __init__(self,x,y,w,h,parent=None):self.box=(x,y,w,h);self.master=parent;self.target=0;self.callback=None;self.canceled=False
 def winfo_exists(self):return True
 def winfo_viewable(self):return True
 def winfo_rootx(self):return self.box[0]
 def winfo_rooty(self):return self.box[1]
 def winfo_width(self):return self.box[2]
 def winfo_height(self):return self.box[3]
 def after(self,ms,fn):self.callback=fn;return 'pending'
 def after_cancel(self,job):self.canceled=True
 def bind(self,*a,**kw):pass
 def animate(self,target):self.target=target
host=W(300,0,700,800);panel=W(300,0,700,800,host);button=W(10,600,120,40);position=[(30,620)];clock=[0.]
app=SimpleNamespace(testing_button=button,winfo_pointerxy=lambda:position[0])
with patch('testing_ui.time.monotonic',side_effect=lambda:clock[0]):
 watch=HoverDismiss(app,panel)
 for now in (.1,.2,1.):clock[0]=now;watch.check();assert panel.target==0
 position[0]=(250,620);clock[0]=1.1;watch.check();clock[0]=1.3;watch.check();assert panel.target==0
 position[0]=(500,400);clock[0]=1.4;watch.check();assert watch.outside_since is None
 position[0]=(20,20);clock[0]=2.;watch.check();clock[0]=2.5;watch.check();assert panel.target==-1
 panel.target=0;watch.job='pending';watch.cleanup(SimpleNamespace(widget=panel));assert panel.canceled and watch.job is None
assert not pointer_over(W(-400,0,700,800,host),30,300)
print('PASS hover button and panel stay open, crossing gap grace, leaving both closes, clipped panel excluded, cleanup cancels timer; no keyboard-focus dismissal')

