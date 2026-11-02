from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
import currency_menu as m
from currencies import CURRENCIES,format_money,configure_display
from budget_review import COLUMNS
assert set(m.NOTE_COLOURS)==set(m.COUNTRIES)==set(CURRENCIES)
assert all('(CAD)' not in x for x in COLUMNS)
saved={};store=SimpleNamespace(preference=lambda key,default:saved.get(key,default),set_preference=lambda key,value:saved.update({key:value}))
app=SimpleNamespace(store=store)
with patch.object(m.messagebox,'showinfo') as message:
 assert not m.select_currency(app,'USD') and 'display_currency' not in saved
 message.assert_called_once()
 saved['fx_rate:USD']='1.4';assert m.select_currency(app,'USD');assert saved['display_currency']=='USD'
 assert format_money(14000)=='USD 100.00'
 assert m.select_currency(app,'CAD');assert format_money(14000)=='$140.00'
class Image:
 def __init__(self,**kw):assert kw['width']==34 and kw['height']==20
 def put(self,colour,to):assert len(colour)==7 and 0<=to[0]<to[2]<=34 and 0<=to[1]<to[3]<=20
with patch.object(m.tk,'PhotoImage',Image):
 for code in CURRENCIES:m.banknote(None,code)
print('PASS ten banknote icons, header labels, saved selection, rate conversion and missing-rate handling; no GUI opened')

