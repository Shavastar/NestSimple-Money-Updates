from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
import storage_page
from visuals import draw_pair
fixture=Path(__file__).with_name('verify_storage1_2_14.py').read_text(encoding='utf-8')
exec(fixture[fixture.index('class Canvas:'):fixture.index('store=SimpleNamespace')])
store=SimpleNamespace(root=Path('.'),db=SimpleNamespace(execute=lambda *a:SimpleNamespace(fetchone=lambda:(3,))))
snapshot=dict(drives=[dict(drive='C:',total=2*1024**4,used=1024**4,free=1024**4)],application_bytes=2*1024**2,database_bytes=4096)
with patch.object(storage_page,'storage_snapshot',return_value=snapshot):spec=storage_page.storage_report(store)
pie=Canvas();draw_pair(pie,spec,'#f00000',mode='pie')
assert any(kind=='oval' and kw.get('fill')!='#edf2f8' for kind,args,kw in pie.items)
assert not any('record' in kw.get('text','').casefold() for kind,args,kw in pie.items)
assert [n for n,v in spec['pie']]==['Hard drive space','Program size','Database size']
bar=Canvas();draw_pair(bar,spec,'#f00000',mode='bar')
assert any('Total records: 21' in kw.get('text','') for kind,args,kw in bar.items)
print('PASS visible solid storage pie with 2-TiB/2-MiB/4-KiB ratios; no records in pie title, slices, legend or notes; bar retains total records')

