from pathlib import Path
import sys,tkinter as tk
from tkinter import ttk
sys.path.insert(0,str(Path('work/current-source').resolve()))
from icon_ui import HoverText
root=tk.Tk();root.withdraw();button=ttk.Button(root,text='Test');hover=HoverText(button,'Button hover disabled')
assert not button.bind('<Enter>') and not button.bind('<FocusIn>') and hover.pending is None
label=ttk.Label(root,text='Information');HoverText(label,'Information retained');assert label.bind('<Enter>')
root.destroy();print('PASS button hover handlers absent; informational label behavior retained')

