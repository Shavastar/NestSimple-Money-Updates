from pathlib import Path
import sys,ast
from types import SimpleNamespace
from unittest.mock import patch
sys.path.insert(0,str(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'current-source'))
import page_messages as page
from budget_review import COLUMNS,review_sort_key,sorted_review_rows,BudgetReview
from budget_planner import plan_changes
from friendly_messages import CHOICES,dismiss_result
rows=[('Housing','1,200.00','900.00','↓ Down 300.00'),('Groceries','100.00','600.00','↑ Up 500.00'),('Utilities','20.00','20.00','Unchanged'),('Savings','0.00','0.00','Unchanged')]
actuals={'Housing':58000,'Groceries':5000,'Utilities':0}
for column in range(5):
 for reverse in (False,True):
  sorted_rows=sorted_review_rows(rows,column,reverse,actuals)
  values=[review_sort_key(r,column,actuals) for r in sorted_rows if review_sort_key(r,column,actuals) is not None]
  assert values==sorted(values,reverse=reverse),(column,reverse,values)
  assert len(sorted_rows)==len(rows)
assert sorted_review_rows(rows,2,False,actuals)[-1][0]=='Savings'
assert sorted_review_rows(rows,2,True,actuals)[-1][0]=='Savings'
assert [r[0] for r in sorted_review_rows(rows,4,False,actuals)]==['Housing','Utilities','Savings','Groceries']
assert len(COLUMNS)==5 and 'Actuals' in COLUMNS[2]
review=BudgetReview.__new__(BudgetReview);review.rows=rows;review.actuals=actuals;review.sort_column=None;review.reverse=False;review.selected={'Housing'};calls=[];review.render=lambda:calls.append(True)
review.sort(1);assert not review.reverse
review.sort(1);assert review.reverse
review.sort(2);assert not review.reverse
assert review.selected=={'Housing'} and len(calls)==3
amounts={'Housing':SimpleNamespace(get=lambda:'1200.00')}
assert plan_changes(amounts,{'Housing':90000})[0][1:3]==('1,200.00','900.00')
for start,end in ((0,400),(400,0)):
 offsets=[page.slide_offset(start,end,t,.18) for t in (-.1,0,.03,.09,.18,.3)]
 assert offsets[0]==start and offsets[-1]==end
 assert offsets==sorted(offsets,reverse=start>end)
clock=[0.0];jobs=[];positions=[];destroyed=[];unbound=[]
sheet=page.PageMessage.__new__(page.PageMessage)
sheet._offset=0;sheet._job=None;sheet._closing=False;sheet._host_binding='binding'
sheet.host=SimpleNamespace(unbind=lambda *args:unbound.append(args))
sheet.winfo_exists=lambda:True;sheet.winfo_ismapped=lambda:True
sheet.place_configure=lambda **kw:positions.append(kw['y'])
def after(delay,callback):
 identifier=str(len(jobs)+1);jobs.append((identifier,callback));return identifier
sheet.after=after;sheet.after_cancel=lambda job:None
def pump():
 while jobs:
  _,callback=jobs.pop(0);clock[0]+=.02;callback()
with patch.object(page.time,'monotonic',side_effect=lambda:clock[0]),patch.object(page.tk.Frame,'destroy',side_effect=lambda window:destroyed.append(window)):
 sheet._animate(400,.18);pump();assert sheet._offset==400 and positions[-1]==-400
 sheet.destroy();sheet.destroy();assert not destroyed;pump()
 assert sheet._offset==0 and positions[-1]==0 and destroyed==[sheet] and len(unbound)==1
assert dismiss_result('yesno')=='no' and dismiss_result('okcancel')=='cancel'
assert dict(CHOICES['yesno'])=={'Yes':'yes','No':'no'}
tags=('button','Button','root','all')
assert page.message_bindtags(tags,'sheet')==('button','Button','sheet','root','all')
assert page.message_bindtags(page.message_bindtags(tags,'sheet'),'sheet')==page.message_bindtags(tags,'sheet')
root=Path(__file__).parent/'current-source'
for name in ('page_messages.py','message_art.py','friendly_messages.py','budget_review.py','budget_planner.py'):
 tree=ast.parse((root/name).read_text(encoding='utf-8'),feature_version=(3,10))
 if name in ('page_messages.py','friendly_messages.py'):
  assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='Toplevel' for n in ast.walk(tree)),name
print('PASS headless: all five column sort keys/directions, signed changes, missing actuals last, toggle and selection preservation, CAD formatting, slide-up/down endpoints, delayed close and duplicate-dismiss guard, cleanup, existing answer values, no Toplevel construction, Python 3.10 syntax')
