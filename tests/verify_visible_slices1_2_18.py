from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
from visuals import pie_angles
values=[2*1024**4,2*1024**2,4096]
angles=pie_angles(values,12)
assert len(angles)==3 and min(angles)>=12 and abs(sum(angles)-360)<1e-8
assert pie_angles([0,5,0],12)==[0,360,0]
assert pie_angles([1,3])==[90,270]
fixture=Path(__file__).with_name('verify_pie1_2_17.py').read_text(encoding='utf-8')
exec(compile(fixture,str(__file__),'exec'))
arcs=[kw for kind,args,kw in pie.items if kind=='arc']
assert len(arcs)==3 and len({kw['fill'] for kw in arcs})==3
assert all(abs(kw['extent'])>=12 for kw in arcs)
assert 'Small slices are enlarged' in spec['pie_note']
print('PASS all three actual storage items have visible distinct coloured slices, exact bytes retained, enlargement disclosed; regular financial pie proportions unchanged')

