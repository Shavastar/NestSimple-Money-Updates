from pathlib import Path
from unittest.mock import patch
import sys,ast
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
from currency_menu import spaced_icon
calls=[]
class Image:
 def __init__(self,**kw):self.options=kw;self.tk=self
 def call(self,*args):calls.append(args)
 def width(self):return 28
 def height(self):return 28
with patch('currency_menu.tk.PhotoImage',Image):
 image=spaced_icon(None,Image());assert image.options['width']==40 and image.options['height']==28
 assert calls[-1][-2:]==(6,0)
root=Path(__file__).parent/'current-source'
for name in ('modern_ui.py','currency_ui.py','storage_page.py','currency_menu.py','table_ui.py'):
 ast.parse((root/name).read_text(encoding='utf-8-sig'),feature_version=(3,10))
s=(root/'storage_page.py').read_text(encoding='utf-8-sig')
assert "troughcolor='#91b7e6'" in s and "background='#2463d3'" in s
assert "style='StorageWhite.TLabelframe'" in s and "style='StorageWhite.TLabel'" in s
print('PASS icon padding six pixels each side, full image height retained, white drive labels and blue/light-blue progress configuration, Python 3.10 syntax')

