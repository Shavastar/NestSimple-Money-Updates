"""Real Tk regression for chart expansion, inclusive ranges and series colours."""
from pathlib import Path
import sys, re, tkinter as tk
from tkinter import ttk
from types import SimpleNamespace
from unittest.mock import patch
sys.path.insert(0,str(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'current-source'))
import visuals

root=tk.Tk();root.withdraw()
errors=[]
root.report_callback_exception=lambda *args:errors.append(args)
spec=dict(_budget_chart=True,pie_title='Budget',pie=[('Savings',100),('Housing',300)],bar_title='Budget',bar=[('Savings',(100,75)),('Housing',(300,200))],unit='money',series=('Planned','Actual'),date_from='2026-01-01',date_to='2026-10-31',trend=([('2026-09',100,75),('2026-10',300,200)],('Planned','Actual')),budget_records=[])
def ranged(start,end):
    if start>end:raise ValueError('From must precede To')
    return dict(spec,date_from=start,date_to=end,pie=[('Savings',200),('Housing',600)],bar=[('Savings',(200,150)),('Housing',(600,400))])
spec.update(_range_factory=ranged,_range_changed=lambda chosen:None)
with patch('budget_chart.configure_budget_chart'):
    panel=visuals.chart_panel(root,spec,'#2463d3')
panel.pack();root.update()
start,end,apply=panel.date_ranges['pie']
start.set('2026-03-02');end.set('2026-08-17');apply();root.update()
def texts(canvas):
    return {canvas.itemcget(i,'text'):i for i in canvas.find_all() if canvas.type(i)=='text'}
for mode,canvas in panel.canvases.items():
    assert tuple(v.get() for v in panel.date_ranges[mode][:2])==('2026-03-02','2026-08-17')
    assert panel.range_states[mode]['spec']['date_from']=='2026-03-02'
    windows=[i for i in canvas.find_all() if canvas.type(i)=='window']
    assert len(windows)==1,(mode,windows)
    controls=root.nametowidget(canvas.itemcget(windows[0],'window'))
    entries=[w for w in controls.winfo_children() if isinstance(w,tk.Entry)]
    assert len(entries)==2
    assert all(int(e.cget('borderwidth'))==0 and int(e.cget('highlightthickness'))==0 for e in entries)
    if mode=='trend':continue
    # Invoke the actual Tcl tag binding used by a category click.
    before=canvas.coords(windows[0])
    for attempt in range(2):
        item=next(i for label,i in texts(canvas).items() if label=='Banking' or label.startswith('Banking ·'))
        tag=next(t for t in canvas.gettags(item) if t.startswith('budget-pie-'))
        command=canvas.tag_bind(tag,'<Button-1>')
        callback=re.search(r'\[([^ ]+)',command).group(1)
        canvas.tk.call(callback)
        root.update()
        windows=[i for i in canvas.find_all() if canvas.type(i)=='window']
        assert len(windows)==1 and canvas.coords(windows[0])==before
        assert panel.range_states[mode]['spec']['bar'][0][1]==(200,150)
        if mode=='bar' and attempt==0:
            labels=texts(canvas)
            assert canvas.coords(labels['Savings'])[0]-canvas.coords(labels['Banking'])[0]==24
    if mode=='bar':
        fills={canvas.itemcget(i,'fill') for i in canvas.find_all() if canvas.type(i)=='rectangle'}
        assert fills<={'#edf2f8','#2463d3','#91b7e6'},fills
previous=panel.range_states['pie']['spec']
start.set('2027-01-01');end.set('2026-01-01');apply();root.update()
assert panel.range_states['pie']['spec'] is previous
assert not errors,errors
root.destroy()
print('PASS real Tk: shared From/To, invalid range, expand/collapse controls, borderless entries, 24px indentation, legend/bar colours, no callback errors')
