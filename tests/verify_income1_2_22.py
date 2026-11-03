"""Actual hidden Tk widgets with disposable fictional Income records; no desktop windows."""
from pathlib import Path
import sys,tempfile,sqlite3,types,ast
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
import tkinter as tk
from tkinter import ttk
from app import BaseApp
from record_pages import RecordNavigation
from finance import Store,money
from income_dashboard import build_page,shift_period,period_picker,restore_chrome
from table_ui import install
from i18n import install_widget_translation
from icon_ui import install as install_icons

class Hidden(tk.Tk):
    table=BaseApp.table
    record_tree=RecordNavigation.record_tree
    def open_record(self,*args):self.opened=args
    def record_from_widget(self,*args):self.opened=args[1:]
    def income_form(self):self.opened=('add',)
    def edit_transaction(self):self.opened=('edit',)
    def delete_transaction(self):self.opened=('delete',)
    def export(self,*args):self.opened=('export',)+args
    def edit_list_record(self,*args):self.opened=args

def walk(widget):
    for child in widget.winfo_children():yield child;yield from walk(child)

errors=[]
temporary=tempfile.mkdtemp(prefix='income-qa-',dir=Path(__file__).parent)
if True:
    app=Hidden();app.withdraw() # Withdraw before any update/event processing.
    app.report_callback_exception=lambda *error:(errors.append(error),__import__('traceback').print_exception(*error))
    install();install_widget_translation();install_icons(app)
    app.store=Store(Path(temporary)/'fictional');app.profile={'household':'Fictional Income QA','data_dir':str(app.store.root)}
    app.store.db.execute("INSERT INTO accounts(name,type,opening,opening_day) VALUES('Fictional account','Chequing',0,'2025-01-01')")
    for day,description,category,amount in [('2026-11-02','Fictional salary','Salary & wages',120000),('2026-11-03','Fictional refund','Refunds',3500),('2026-10-01','Fictional pension','Pension',99000),('2025-11-01','Prior year','Other income',1000)]:
        app.store.db.execute('INSERT INTO transactions(day,kind,category,description,amount) VALUES(?,?,?,?,?)',(day,'Income',category,description,amount))
    app.store.db.commit();before=app.store.db.execute('SELECT * FROM transactions').fetchall()
    app.month=tk.StringVar(app,value='2026-11');app.current='Income';app.icons={};app.opened=None
    app.topbar=tk.Frame(app,bg='#63300d');tk.Label(app.topbar,text='NestSimple Money',font=('Segoe UI',26)).pack()
    app.body=tk.Frame(app,width=950,height=650);app.body.place(x=0,y=0,width=950,height=650)
    build_page(app);app.update_idletasks();app.update()
    assert not errors,errors
    tree=app.tx;assert len(tree.get_children())==2
    buttons=[w for w in walk(app.body) if isinstance(w,ttk.Button)]
    by_text={str(w.cget('text')):w for w in buttons}
    assert [w.cget('text') for w in buttons if str(w.cget('text')) in ('Manage','Pay Day','Pie Chart','Bar Chart','Trend Graph','Export','Add','Edit','Delete')]==['Manage','Pay Day','Pie Chart','Bar Chart','Trend Graph','Export','Add','Edit','Delete']
    assert str(by_text['Add'].cget('state'))=='normal'
    assert str(by_text['Edit'].cget('state'))=='disabled'
    key=tree.get_children()[0];tree.selection_set(key);app.update();assert str(by_text['Edit'].cget('state'))=='normal'
    tree.selection_remove(key);app.update();assert str(by_text['Delete'].cget('state'))=='disabled'
    assert tree.bind('<Double-1>') and tree.bind('<Return>')
    for col in tree['columns']:
        tree.tk.call(tree.heading(col,'command'))
        assert [tree.item(k,'tags')[-1] for k in tree.get_children()]==['income-even','income-odd']
    # Exercise actual calendar chooser and filter controls, with no Toplevel.
    picker=next(w for w in buttons if w.cget('text')=='▦');picker.invoke();app.update_idletasks()
    panel=tree._income_period_picker
    year_box=next(w for w in walk(panel) if isinstance(w,ttk.Spinbox));year_box.set('2026')
    next(w for w in walk(panel) if isinstance(w,ttk.Button) and w.cget('text')=='Show Year').invoke();app.update()
    assert len(tree.get_children())==3
    combos=[w for w in walk(tree.master) if isinstance(w,ttk.Combobox)]
    period=next(w for w in combos if 'All Dates' in w.cget('values'));period.set('All Dates');period.event_generate('<<ComboboxSelected>>');app.update();assert len(tree.get_children())==4
    query=next(w for w in walk(tree.master) if isinstance(w,ttk.Entry) and not isinstance(w,ttk.Combobox) and w.master.winfo_class()=='TFrame' and w.winfo_manager()=='grid')
    query.insert(0,'refund');by_search=next(w for w in walk(tree.master) if isinstance(w,ttk.Button) and w.cget('text')=='Search');by_search.invoke();app.update();assert len(tree.get_children())==1
    assert money(3500) in tree._income_status.cget('text')
    assert app.store.db.execute('SELECT * FROM transactions').fetchall()==before
    assert shift_period('2026-12','2026',False,1)[0]=='2027-01'
    assert shift_period('2026-01','2026',False,-1)[0]=='2025-12'
    assert shift_period('2026-11','0001',True,-1)[1]=='0001'
    assert shift_period('2026-11','9999',True,1)[1]=='9999'
    for width in (950,580,300):
        app.body.place_configure(width=width);app.update_idletasks();app.update()
        assert not errors,errors
        assert tree.winfo_width()<=width
    restore_chrome(app);assert '26' in str(app.topbar.winfo_children()[0].cget('font'))
    app.store.db.close();app.destroy()
print('PASS hidden real Tk: Income construction, compact action order, selection enable/disable, detail bindings, sortable stripes, year/all-date/search filters, totals, small widths, date boundaries and unchanged fictional ledger. No visual GUI/restart verification.')




