import sys
from types import SimpleNamespace
sys.path.insert(0,'HomeMoney')
import ast
from pathlib import Path
module=ast.parse(Path('HomeMoney/visuals.py').read_text())
function=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='install_trend_hover')
namespace={'tr':lambda text:text,'money':lambda amount:f'${amount/100:.2f}'}
exec(compile(ast.Module(body=[function],type_ignores=[]),'visuals.py','exec'),namespace)
install_trend_hover=namespace['install_trend_hover']
class Canvas:
 def __init__(self):self.items={1:[97,97,103,103]};self.bound={};self.text=[]
 def coords(self,item):return self.items.get(item,[])
 def delete(self,tag):self.text=[]
 def canvasx(self,x):return x+20
 def canvasy(self,y):return y+70
 def winfo_width(self):return 700
 def create_text(self,*a,**kw):self.text.append(kw['text']);return 2
 def bbox(self,item):return (20,20,160,80)
 def create_rectangle(self,*a,**kw):return 3
 def tag_raise(self,*a):pass
 def bind(self,event,callback):self.bound[event]=callback
c=Canvas();install_trend_hover(c,[('2026-10',12500,20000)],['Actual','Suggested'],[(1,0)])
# Both chart layout passes move rendered points by 24 pixels.
c.items[1]=[97,145,103,151]
c.bound['<Motion>'](SimpleNamespace(x=80,y=78));assert '2026-10' in c.text[0] and 'Actual:' in c.text[0] and 'Suggested:' in c.text[0]
c.bound['<Motion>'](SimpleNamespace(x=80,y=30));assert not c.text
c.bound['<Motion>'](SimpleNamespace(x=80,y=78));c.bound['<Leave>']();assert not c.text
print('PASS trend hover after layout shifts and scrolling, exact series and leave')
