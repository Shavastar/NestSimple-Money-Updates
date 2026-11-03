from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import sys
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
import expense_page as e
class W:
 def __init__(self,parent=None,**kw):self.master=parent;self.content=self;self.tabs=[];self.position={};self.children=[]
 def grid(self,**kw):self.position=kw
 def grid_configure(self,**kw):self.position.update(kw)
 def pack(self,**kw):pass
 def columnconfigure(self,*a,**kw):pass
 def configure(self,*args,**kw):pass
 def bind(self,*a,**kw):pass
 def add(self,child,text):self.tabs.append((text,child))
 def winfo_children(self):return []
 def winfo_width(self):return 1000
form=SimpleNamespace(vars={'account':SimpleNamespace(trace_add=lambda *a:None)},row=1)
with patch.object(e.tk,'Frame',W),patch.object(e.ttk,'Frame',W),patch.object(e.ttk,'Label',W),patch.object(e.ttk,'Separator',W),patch.object(e.ttk,'Notebook',W),patch.object(e.ttk,'Style',W),patch('layout.ScrollArea',W),patch.object(e,'large_icon',return_value=W()):
 for kind in ('Income','Expense'):
  layout=e.ExpenseLayout.__new__(e.ExpenseLayout);layout.host=W();layout.form=form;layout.account=W();layout.kind=kind;layout.account_icon=lambda:None
  layout.details();assert [label for label,child in layout.tabs.tabs][:2]==['Original Image','Contact information']
  assert layout.tabs.position['column']==1 and form.contact_body is layout.tabs.tabs[1][1].content
  left,original,splits,contact=e.detail_columns(W(),SimpleNamespace(),kind)
  assert contact.master.tabs[0][0]=='Original Image' and contact.master.tabs[1][0]=='Contact'
  if kind=='Expense':assert splits is contact.master.tabs[2][1].content
source=Path(__file__).parent/'current-source'
assert "contact_tabs=False,subpage=True" in (source/'modern_ui.py').read_text(encoding='utf-8')
bill=(source/'manual_bill.py').read_text(encoding='utf-8');assert "self.tabs=ttk.Notebook(bill);self.tabs.grid(row=0,column=1" in bill
print('PASS Income/Expense entry and details: Original then Contact share right notebook; split pane mapping preserved; Bill entry right notebook; no desktop windows')

