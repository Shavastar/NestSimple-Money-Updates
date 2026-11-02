"""Large shared app illustrations with clear, accessible status badges."""
from pathlib import Path
import tkinter as tk

def message_header(parent,title,icon,kind,width,artwork=None):
    background='#f1f7fc'
    hero=tk.Frame(parent,bg=background,padx=16,pady=12);hero.pack(fill='x',pady=(0,14))
    art=tk.Canvas(hero,width=140,height=128,bg=background,highlightthickness=0);art.pack(side='left',padx=(0,12))
    category='error' if icon=='error' else 'warning' if icon=='warning' else 'question' if icon=='question' or kind!='ok' else 'info'
    success=category=='info' and any(word in title.casefold() for word in ('saved','complete','created','updated','ready'))
    name='menu-chart-112.png' if artwork=='auto_populate' else 'cmd-savings-112.png' if success else 'cmd-home-112.png'
    try:
        hero._image=tk.PhotoImage(master=hero,file=str(Path(__file__).resolve().parent/'assets'/name))
        art.create_image(66,58,image=hero._image)
    except (tk.TclError,OSError):
        # Crisp built-in illustration if an older installation lacks the PNG.
        art.create_polygon(12,55,64,12,116,55,fill='#326ea9',outline='')
        art.create_rectangle(27,53,101,109,fill='#ddeefa',outline='#326ea9',width=2)
        art.create_rectangle(55,77,76,109,fill='#326ea9',outline='')
        art.create_oval(85,69,127,111,fill='#ffd36b',outline='#bd902a',width=2)
    colour={'error':'#bc4141','warning':'#c48216','question':'#2463a6','info':'#2463a6'}[category]
    symbol={'error':'!','warning':'!','question':'?','info':'i'}[category]
    if success:colour='#278452';symbol='✓'
    art.create_oval(94,80,138,124,fill=colour,outline='white',width=3)
    art.create_text(116,102,text=symbol,fill='white',font=('Segoe UI',25,'bold'))
    tk.Label(hero,text=title,bg=background,fg='#193c58',font=('Segoe UI',20,'bold'),justify='left',wraplength=max(120,width-190)).pack(side='left',fill='x',expand=True)
    return hero
