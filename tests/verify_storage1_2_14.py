from pathlib import Path
import sys
from unittest.mock import patch
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
import storage_page
from visuals import draw_pair,category_colour,PALETTE
class Canvas:
 def __init__(self):self.items=[]
 def winfo_width(self):return 1000
 def delete(self,*a):self.items=[]
 def find_all(self):return tuple(range(len(self.items)))
 def create(self,kind,*args,**kw):self.items.append((kind,args,kw));return len(self.items)
 def create_text(self,*a,**kw):return self.create('text',*a,**kw)
 def create_rectangle(self,*a,**kw):return self.create('rectangle',*a,**kw)
 def create_arc(self,*a,**kw):return self.create('arc',*a,**kw)
 def create_oval(self,*a,**kw):return self.create('oval',*a,**kw)
 def configure(self,**kw):pass
store=SimpleNamespace(root=Path('.'),db=SimpleNamespace(execute=lambda *a:SimpleNamespace(fetchone=lambda:(3,))))
snapshot=dict(drives=[dict(drive='C:',total=1000,used=700,free=300),dict(drive='E:',total=2000,used=800,free=1200)],application_bytes=55,database_bytes=22)
with patch.object(storage_page,'storage_snapshot',return_value=snapshot):spec=storage_page.storage_report(store)
assert spec['bar']==[(n,(v,)) for n,v in spec['pie']] and len(spec['bar'])==4
assert 'Program size:' in spec['note'] and 'Database size:' in spec['note'] and 'Record numbers:' in spec['note']
colours=[category_colour(n,i) for i,(n,v) in enumerate(spec['pie'])]
assert colours==[PALETTE[i] for i in (0,7,14,1)] and len(set(category_colour('',i) for i in range(20)))==20
pie=Canvas();draw_pair(pie,spec,'#f00000',mode='pie')
bar=Canvas();draw_pair(bar,spec,'#f00000',mode='bar')
assert [kw['fill'] for kind,args,kw in pie.items if kind=='arc']==colours
assert [kw['fill'] for kind,args,kw in bar.items if kind=='rectangle' and args[0]==190 and kw['fill']!='#edf2f8']==colours
print('PASS two-drive/four-category storage pie and bars: identical values, order, contrasting wheel colours and matching legends; program/database/record details retained')

