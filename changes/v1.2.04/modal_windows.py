"""Keep modal dialogs above the window they block, without global pinning."""
import tkinter as tk

def keep_in_front(window):
    if not isinstance(window,tk.Toplevel) or getattr(window,'_modal_front_installed',False):return
    window._modal_front_installed=True
    parent=window.master
    owner=parent.winfo_toplevel() if parent is not None else None
    previous=window.grab_current()
    if previous is not None and previous is not window:
        candidate=previous.winfo_toplevel();ancestor=candidate
        while ancestor is not None and ancestor is not window:ancestor=getattr(ancestor,'master',None)
        if ancestor is None:owner=candidate
    if owner is not None and owner is not window:
        # Transient ownership of a withdrawn startup root can hide the dialog.
        window.transient(owner if owner.state()!='withdrawn' else '')
    def raise_dialog(event=None,focus=False):
        if event is not None and event.widget is not owner:return
        try:
            if window.winfo_exists() and window.state()!='withdrawn':
                window.lift()
                if focus:window.focus_set()
        except tk.TclError:pass
    bindings=[]
    if owner is not None and owner is not window:
        for event in ('<FocusIn>','<Map>'):
            bindings.append((event,owner.bind(event,raise_dialog,add='+')))
    def clean(event):
        if event.widget is not window:return
        if owner is not None:
            for event_name,identifier in bindings:
                try:owner.unbind(event_name,identifier)
                except tk.TclError:pass
    window.bind('<Destroy>',clean,add='+')
    window.after_idle(lambda:raise_dialog(focus=True))

def install():
    if getattr(tk.Misc,'_nestsimple_modal_front',False):return
    original_grab=tk.Misc.grab_set;original_global=tk.Misc.grab_set_global;original_wait=tk.Misc.wait_window
    def grab(window):
        keep_in_front(window)
        return original_grab(window)
    def global_grab(window):
        keep_in_front(window)
        return original_global(window)
    def wait(window,target=None):
        target=target if target is not None else window
        keep_in_front(target)
        return original_wait(window,target)
    tk.Misc.grab_set=grab;tk.Misc.grab_set_global=global_grab;tk.Misc.wait_window=wait
    # Native Open/Save/folder dialogs also need the active modal as owner.
    from tkinter import commondialog
    original_native=commondialog.Dialog.show
    def native_show(dialog,**options):
        parent=options.get('parent') or dialog.options.get('parent') or dialog.master
        if parent is None:
            root=tk._default_root
            if root is not None:
                active=root.grab_current() or root.focus_displayof() or root
                parent=active.winfo_toplevel()
        if parent is not None:options['parent']=parent
        return original_native(dialog,**options)
    commondialog.Dialog.show=native_show
    tk.Misc._nestsimple_modal_front=True
