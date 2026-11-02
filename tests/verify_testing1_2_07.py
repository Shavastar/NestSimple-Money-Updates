from pathlib import Path
import sys
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
import testing_ui as ui
class Panel:
 animate=ui.TestingPanel.animate
 toggle=ui.TestingPanel.toggle
 def __init__(self):self.position=-1.;self.target=0.;self.job=None;self.pending=None;self.exists=True
 def after_cancel(self,job):self.pending=None
 def after(self,ms,fn):self.pending=fn;return 1
 def winfo_exists(self):return self.exists
 def place_configure(self,**kw):assert -1<=kw['relx']<=0
 def destroy(self):self.exists=False
clock=[0.]
with patch.object(ui.time,'monotonic',side_effect=lambda:clock[0]):
 p=Panel();p.animate(0);clock[0]=.11;p.pending();assert -1<p.position<0
 p.toggle();assert p.target==-1
 clock[0]=.15;p.pending();p.toggle();assert p.target==0
 clock[0]=.5;p.pending();assert p.position==0 and p.exists
 p.toggle();clock[0]=1.;p.pending();assert p.position==-1 and not p.exists
source=Path(ui.__file__).read_text()
assert 'TestingPanel(app.outer)' in source and 'tk.Toplevel' not in source and 'focus_force' not in source
print('PASS slide-in, both toggle directions during animation, close-slide cleanup, content-only parent and no separate window')

