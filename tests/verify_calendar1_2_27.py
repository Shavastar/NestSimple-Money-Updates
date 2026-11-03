from pathlib import Path
import sys,tkinter as tk,types
sys.path.insert(0,str(Path('work/current-source').resolve()))
from income_calendar import YearCalendar
from income_skin import ReferenceButton
r=tk.Tk();r.withdraw();host=tk.Frame(r);host.place(width=900,height=700);r.update_idletasks();chosen=[]
for scope in ('Day','Month','Year'):
 p=YearCalendar(host,'2024-02-29',lambda *args:chosen.append(args),scope=scope);r.update_idletasks();p.draw()
 assert len([h for h in p.hits if h[4]=='Month'])==(12 if scope=='Year' else 1)
 assert len(p.canvas.find_withtag('selected-day'))==(1 if scope=='Day' else 0)
 p.move(1);assert (p.year.get(),p.month.get())==(('2025','02') if scope=='Year' else ('2024','03'))
 p.move(-1);assert (p.year.get(),p.month.get())==('2024','02')
 if scope=='Month':
  p.month.set('12');p.move(1);assert (p.year.get(),p.month.get())==('2025','01')
  hit=next(h for h in p.hits if h[4]=='Day');p.click(types.SimpleNamespace(x=(hit[0]+hit[2])/2,y=(hit[1]+hit[3])/2));assert chosen[-1][0]=='Month'
 else:p.destroy()
for direction in ('previous','next'):
 b=ReferenceButton(host,direction,lambda:None,text='');b.place(width=32,height=32);r.update_idletasks();b.redraw();assert not any(b.type(item)=='text' for item in b.find_all());b.destroy()
r.destroy();print('PASS Day/Month single-month views, selected leap-day highlight, Year twelve-month view, month/year arrows and December rollover, Month selection scope, icon-only navigation')

