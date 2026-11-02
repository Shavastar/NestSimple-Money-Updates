from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
from page_messages import sheet_bounds
class W:
 def __init__(self,x,width,height=400,children=(),marked=False,visible=True):self.x=x;self.width=width;self.height=height;self.children=children;self._message_list=marked;self.visible=visible
 def winfo_width(self):return self.width
 def winfo_height(self):return self.height
 def winfo_rootx(self):return self.x
 def winfo_children(self):return self.children
 def winfo_viewable(self):return self.visible
row=W(124,872,marked=True);sheet=W(110,900,marked=True)
host=W(100,920,children=[row,sheet,W(100,920,marked=True,visible=False)])
assert sheet_bounds(host,sheet)==(24,872)
row.width=600;assert sheet_bounds(host,sheet)==(24,600)
row.width=1200;assert sheet_bounds(host,sheet)==(24,896)
host.children=[];assert sheet_bounds(host)==(14,892)
host.width=10;assert sheet_bounds(host)==(4,2)
print('PASS slide-up width follows visible list, resize, host clipping, hidden-page exclusion and inset fallback')

