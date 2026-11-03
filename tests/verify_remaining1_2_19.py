from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import sys
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
import storage_page
from visuals import category_colour
assert category_colour('Hard drive space remaining',0)=='#2463d3'
store=SimpleNamespace(root=Path('.'),db=SimpleNamespace(execute=lambda *a:SimpleNamespace(fetchone=lambda:(3,))))
snapshot=dict(drives=[dict(drive='C:',total=1000,used=700,free=300),dict(drive='E:',total=2000,used=800,free=1200)],application_bytes=55,database_bytes=22)
with patch.object(storage_page,'storage_snapshot',return_value=snapshot):spec=storage_page.storage_report(store)
assert spec['pie']==[('Hard drive space remaining',1500),('Program size',55),('Database size',22)]
assert spec['bar']==[(n,(v,)) for n,v in spec['pie']]
assert spec['_record_total']==21 and 'record' not in spec['pie_note'].casefold()
print('PASS remaining-space label and actual free bytes across two drives, identical pie/bar values, program/database unchanged, records excluded from pie')

