from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
test=Path(__file__).with_name('verify_storage1_2_14.py').read_text(encoding='utf-8')
test=test.replace("assert spec['bar']==[(n,(v,)) for n,v in spec['pie']] and len(spec['bar'])==4","assert spec['bar']==[(n,(v,)) for n,v in spec['pie']] and [n for n,v in spec['pie']]==['Hard drive space','Program size','Database size']; assert spec['_record_total']==21")
test=test.replace('(0,7,14,1)','(0,10,5)').replace("'Record numbers:' in spec['note']","'Total records: 21' in spec['note']")
test=test.replace("print('PASS two-drive/four-category storage pie and bars: identical values, order, contrasting wheel colours and matching legends; program/database/record details retained')","assert any('Total records: 21' in kw.get('text','') for kind,args,kw in bar.items); print('PASS exact three storage labels, identical bytes and colours, distinct red/green/yellow storage and purple record count, total 21 shown separately on both charts')")
exec(compile(test,str(__file__),'exec'))

