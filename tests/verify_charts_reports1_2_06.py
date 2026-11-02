from pathlib import Path
import sys,json,ast
from types import SimpleNamespace
from unittest.mock import patch
base=Path(__file__).parent.resolve();sys.path.insert(0,str(base/'current-source'))
from finance import Store,INCOME_CATEGORIES
from reports import range_report
from chart_hierarchy import rows_for,colour_for,style_section,BLUE
from category_reports import create_category_pdf
from report_order import sort_entries,choose_order,sort_table
from visuals import draw_pair,bind_budget_slice
data=base/'chart-report-fixture';data.mkdir(exist_ok=True)
store=Store(data);store.backup_enabled=False
if not store.accounts():
 for i,kind in enumerate(('Chequing','Savings','Cash','Credit card','Investments','Loan','Mortgage')*2):store.account(f'Account {i+1:02d}',kind,'-500' if kind in ('Credit card','Loan','Mortgage') else '1000','2025-12-01')
 accounts=list(store.accounts());income_category=store.income_categories()[0]
 for i in range(24):
  day=f'2026-{i%12+1:02d}-{i%20+1:02d}'
  store.transaction(day,'Income',f'Income Entry {i:02d}',income_category,'120.00',account=accounts[0]['id'])
  store.transaction(day,'Expense',f'Expense Entry {i:02d} '+('a long readable description '*12 if i==0 else ''),'Groceries','80.00',account=accounts[0]['id'],splits=[('Groceries','30.00'),('Electricity','50.00')] if i%2==0 else None)
  bill=store.add_bill(f'Supplier {i:02d}',day,'Housing' if i%2 else 'Groceries','60.00')
  if i%3==0:store.pay_bill(bill,day)
profile={'household':'Disposable Chart Report Test','backup_dir':str(data/'backups')};(data/'backups').mkdir(exist_ok=True)
app=SimpleNamespace(store=store,profile=profile,current='Charts',month=SimpleNamespace(get=lambda:'2026-11'))
output=base/'report-qa';output.mkdir(exist_ok=True)
specs={}
for section in ('Accounts','Income','Transactions','Bills'):
 spec=range_report(store,section,'2026-01-01','2026-12-31',profile);specs[section]=spec
 assert spec['_category_chart'] and spec['_chart_section']==section
 total=sum(v for n,v in spec['pie'])
 opened=set(spec['_group_order'])
 pie=rows_for(spec,[(n,(v,)) for n,v in spec['pie']],opened)
 assert sum(v[0] for n,v,g in pie)==total
 bars=rows_for(spec,spec['bar'],opened,True)
 for group in spec['_group_order']:
  children=[v for n,v,g in bars if g==group and n.startswith('  ')]
  if children:assert next(v for n,v,g in bars if n==group)==tuple(sum(v[j] for v in children) for j in range(len(children[0])))
 entries=spec['_records']
 assert len(sort_entries(entries,'category',spec['_group_order']))==len(entries)
 assert [r['day'] for r in sort_entries(entries,'date')]==sorted((r['day'] for r in entries),reverse=True)
 assert [str(r.get('sort_name',r['source'])).casefold() for r in sort_entries(entries,'alphabetical')]==sorted(str(r.get('sort_name',r['source'])).casefold() for r in entries)
 for mode in ('category','date','alphabetical'):
  create_category_pdf(app,output/(section+'-'+mode+'.pdf'),spec,mode)
 # Inclusive date limits also apply to grouped transaction and bill details.
 chosen=range_report(store,section,'2026-03-01','2026-07-31',profile)
 if section!='Accounts':assert all('2026-03-01'<=r['day']<='2026-07-31' for r in chosen['_records'])
income=specs['Income'];assert income['_stats'][1][1]==24
assert all(r['name'] for r in specs['Transactions']['_records'])
paid=next(r for r in store.bills() if r['paid_transaction'])
assert next(r['name'] for r in specs['Transactions']['_records'] if r['id']==paid['paid_transaction'])==paid['payee']
expenses=store.db.execute("SELECT sum(amount) FROM transactions WHERE kind='Expense'").fetchone()[0]
assert sum(v[1] for n,v in specs['Transactions']['bar'])==expenses
with patch('friendly_messages.show',return_value='date') as show:
 assert choose_order(app,11)=='date';assert show.call_args.kwargs['vertical_buttons']
 assert len(show.call_args.kwargs['choices'])==4
with patch('friendly_messages.show',return_value='cancel') as show:assert choose_order(app,11) is None
with patch('friendly_messages.show') as show:assert choose_order(app,10)=='displayed';assert not show.called
assert sort_table([('2026-01-01','Z'),('2026-09-01','A'),('Date not recorded','B')],['Date','Source'],'date')[0][0]=='2026-09-01'
class Canvas:
 def __init__(self):self.items={};self.i=0;self.bindings={}
 def winfo_width(self):return 1000
 def find_all(self):return tuple(self.items)
 def delete(self,item):
  if item=='all':self.items.clear()
  else:self.items.pop(item,None)
 def create(self,kind,*coords,**kw):self.i+=1;self.items[self.i]=(kind,coords,kw);return self.i
 def create_text(self,*a,**kw):return self.create('text',*a,**kw)
 def create_rectangle(self,*a,**kw):return self.create('rectangle',*a,**kw)
 def create_oval(self,*a,**kw):return self.create('oval',*a,**kw)
 def create_arc(self,*a,**kw):return self.create('arc',*a,**kw)
 def configure(self,**kw):pass
 def addtag_withtag(self,*a):pass
 def tag_bind(self,tag,event,callback):self.bindings[tag,event]=callback
for spec in specs.values():
 for mode in ('pie','bar'):
  canvas=Canvas();draw_pair(canvas,spec,'#f00000',mode=mode)
  next(cb for (tag,event),cb in canvas.bindings.items() if event=='<Button-1>')()
  assert canvas._budget_expanded
  if mode=='bar':
   colours={kw.get('fill') for kind,coords,kw in canvas.items.values() if kind=='rectangle'}
   assert colours<={'#2463d3','#91b7e6','#edf2f8'},colours
# Planner rows no longer add width outside the pixel column allocation.
text=(base/'current-source/budget_planner.py').read_text(encoding='utf-8')
assert "self.rows[category].pack(fill='x',padx=(24,0))" not in text
assert 'scroll.vertical.grid()' in text
for name in ('chart_hierarchy.py','category_reports.py','report_order.py','visuals.py','reports.py','app.py','budget_planner.py','page_print.py','budget_print.py','planning_print.py','calendar_print.py','card_print.py','bills_print.py'):
 ast.parse((base/'current-source'/name).read_text(encoding='utf-8'),feature_version=(3,10))
(output/'qa-summary.json').write_text(json.dumps({s:{'records':len(v['_records']),'pie_total':sum(n for _,n in v['pie']),'groups':v['_group_order']} for s,v in specs.items()},indent=2),encoding='utf-8')
store.db.close()
print('PASS four sections, grouped expansion and totals, split accounting, date boundaries, blue bars, record sorting, slide-up sort choices/cancel/threshold, Planner inset, 12 complete PDFs and Python 3.10 syntax')

