import sys,ast
from pathlib import Path
sys.path.insert(0,'HomeMoney')
from table_ui import column_widths,fixed_columns
class Grid:
 def __init__(self):self.columns={}
 def columnconfigure(self,index,**kw):self.columns[index]=kw
for width in (480,640,800,1024,1280,1536):
 for weights,inset,leading in (((3,2,2,2),0,42),((4,2,2,2,2),8,0)):
  widths=column_widths(width,weights,inset,leading)
  assert sum(widths)+2*inset+leading==width
  header=Grid();body=Grid()
  for g in (header,body):fixed_columns(g,([leading] if leading else [])+widths)
  assert header.columns==body.columns
  assert all(v['weight']==0 and v['uniform']=='' for v in header.columns.values())
for name in ('budget_review','budget_planner','table_ui','visuals','budget_chart','tools_list'):
 ast.parse(Path('HomeMoney',name+'.py').read_text())
s=Path('HomeMoney/budget_review.py').read_text();assert 'self.align_columns(self.scroll.canvas.winfo_width())' in s
assert "lambda e:self.align_columns(e.width)" in s
assert 'self.selected=set()' in s and 'self.selected.clear()' not in s
print('PASS shared header/body pixel boundaries at six viewport widths; resize and rerender wiring; source compilation')
