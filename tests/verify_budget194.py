from pathlib import Path
import sys,ast,random
sys.path.insert(0,'HomeMoney')
from budget_hierarchy import *
from finance import CATEGORIES
from visuals import draw_pair
assert list(GROUPS)==['Banking','Home','Utilities','Transport','Family And Personal','Giving','Other']
assert [colour(g,g) for g in GROUPS]==['#ed2525','#fff127','#55bb61','#49c5f3','#a04dab','#ef4787','#ffb47b']
assert parent('Internet')=='Home' and parent('Mobile phone')=='Family And Personal'
assert all(parent(n)==g for g in GROUPS for n in GROUPS[g])
items=[(n,(i*100,i*70)) for i,n in enumerate(CATEGORIES)]
for expanded in [None,*GROUPS]:
 rows=chart_rows(items,expanded)
 assert [n for n,v,g in rows if not n.startswith('  ')]==list(GROUPS)
 assert tuple(sum(v[j] for n,v,g in rows) for j in (0,1))==tuple(sum(v[j] for n,v in items) for j in (0,1))
 assert [n.strip() for n,v,g in rows if n.startswith('  ')]==[n for n,v in items if parent(n)==expanded]
 for g,children in ordered(items):
  assert [colour('  '+n,g,items) for n,v in children]==[WHEEL[(ANCHORS[g]+i+1)%20] for i in range(len(children))]
class Tree:
 def __init__(self):self.data={};self.children={'':[]};self.options={'columns':('Category','Amount')};self.bindings={}
 def insert(self,parent,index,iid,**kw):self.data[iid]=kw;self.children[iid]=[];self.move(iid,parent,index)
 def move(self,key,parent,index):
  for children in self.children.values():
   if key in children:children.remove(key)
  target=self.children[parent];target.append(key) if index=='end' else target.insert(index,key)
 def detach(self,key):
  for children in self.children.values():
   if key in children:children.remove(key)
 def get_children(self,key=''):return tuple(self.children[key])
 def item(self,key,option=None,**kw):
  self.data[key].update(kw)
  return self.data[key].get(option) if option else self.data[key]
 def exists(self,key):return key in self.data
 def __getitem__(self,key):return self.options[key]
 def configure(self,**kw):self.options.update(kw)
 def column(self,*a,**kw):pass
 def tag_configure(self,*a,**kw):pass
 def bind(self,event,callback,**kw):self.bindings[event]=callback
 def identify_row(self,y):return y
tr=Tree()
for n,v in items:tr.insert('','end',iid=n,values=(n,v[0]))
group_tree(tr);assert leaf_keys(tr)==[n for g,children in ordered(items) for n,v in children]
# Numeric sort within each group, with headings staying in their approved order.
for i,n in enumerate(sorted(leaf_keys(tr),key=lambda n:tr.item(n,'values')[1],reverse=True)):tr.move(n,'',i)
group_tree(tr)
assert [tr.item(n,'values')[0] for n in tr.get_children()]==list(GROUPS)
for g in tr.get_children():assert [tr.item(n,'values')[1] for n in tr.get_children(g)]==sorted([tr.item(n,'values')[1] for n in tr.get_children(g)],reverse=True)
# Refilter after all rows are detached, then restore every original category.
for n in leaf_keys(tr):tr.move(n,'','end')
for g in tr._budget_group_ids:tr.detach(g)
for n,v in items:tr.detach(n)
for n,v in items:
 if parent(n)=='Home':tr.move(n,'','end')
group_tree(tr);assert len(leaf_keys(tr))==sum(parent(n)=='Home' for n,v in items)
for n,v in items:tr.move(n,'','end')
group_tree(tr);assert set(leaf_keys(tr))==set(CATEGORIES)
class Canvas:
 def __init__(self):self.items={};self.bindings={};self.i=0
 def winfo_width(self):return 1000
 def find_all(self):return tuple(self.items)
 def delete(self,*a):self.items.clear()
 def make(self,kind,*a,**kw):self.i+=1;self.items[self.i]=(kind,a,kw);return self.i
 def create_text(self,*a,**kw):return self.make('text',*a,**kw)
 def create_rectangle(self,*a,**kw):return self.make('rect',*a,**kw)
 def create_oval(self,*a,**kw):return self.make('oval',*a,**kw)
 def create_arc(self,*a,**kw):return self.make('arc',*a,**kw)
 def configure(self,**kw):pass
 def addtag_withtag(self,tag,item):pass
 def tag_bind(self,tag,event,callback):self.bindings[tag,event]=callback
opened=[]
spec=dict(_budget_chart=True,pie_title='Budget',pie=[(n,v[0]) for n,v in items],bar_title='Budget',bar=items,unit='money',series=('Planned','Actual'),open_category=opened.append)
for mode in ('pie','bar'):
 c=Canvas();draw_pair(c,spec,'#2463d3',mode=mode)
 next(v for (tag,event),v in c.bindings.items() if event=='<Button-1>')()
 assert c._budget_expanded in GROUPS
 if mode=='bar':
  next(v for (tag,event),v in c.bindings.items() if event=='<Double-Button-1>')(None)
  assert opened[-1] in CATEGORIES
for p in Path('HomeMoney').glob('*.py'):ast.parse(p.read_text(),filename=str(p),feature_version=(3,10))
print('PASS group order, colours, every category, zero rows, expansion totals, clockwise child colours, grouped numeric sort, filter/restore, chart click expansion and leaf edit, Python 3.10 syntax')
