"""Page-owned bottom sheets: no additional desktop windows."""
import tkinter as tk
from tkinter import ttk
import time,re

def sheet_host(parent):
    owner=parent.winfo_toplevel()
    body=getattr(owner,'body',None)
    if body is not None and body.winfo_exists() and body.winfo_viewable():return body
    return owner

def slide_offset(start,end,elapsed,duration):
    progress=max(0,min(1,elapsed/duration))
    return start+(end-start)*(1-(1-progress)**3)

def message_bindtags(tags,sheet_tag):
    tags=list(tags)
    if sheet_tag not in tags:tags.insert(min(2,len(tags)),sheet_tag)
    return tuple(tags)

class PageMessage(tk.Frame):
    def __init__(self,parent):
        self.host=sheet_host(parent)
        super().__init__(self.host,bg='white',highlightbackground='#b7ccde',highlightthickness=1)
        self._offset=0;self._target=0;self._closing=False;self._job=None
        self.canvas=tk.Canvas(self,bg='white',highlightthickness=0,width=500,height=200)
        scrollbar=ttk.Scrollbar(self,orient='vertical',command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right',fill='y');self.canvas.pack(side='left',fill='both',expand=True)
        self.content=tk.Frame(self.canvas,bg='white')
        self._window=self.canvas.create_window(0,0,window=self.content,anchor='nw')
        self.canvas.bind('<Configure>',self._layout)
        self.content.bind('<Configure>',self._layout)
        self._host_binding=self.host.bind('<Configure>',self._resize,add='+')
        self.bind('<Destroy>',self._gone,add='+')
    def _gone(self,event):
        if event.widget is not self:return
        self._closing=True
        if self._job is not None:
            try:self.after_cancel(self._job)
            except tk.TclError:pass
            self._job=None
        if self._host_binding is not None:
            try:self.host.unbind('<Configure>',self._host_binding)
            except tk.TclError:pass
            self._host_binding=None
    def _layout(self,event=None):
        if not self.winfo_exists():return
        width=max(1,self.canvas.winfo_width())
        self.canvas.itemconfigure(self._window,width=width)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    def _resize(self,event=None):
        if event is not None and event.widget is not self.host:return
        if not self.winfo_exists():return
        self._target=min(self.content.winfo_reqheight()+2,max(100,self.host.winfo_height()-16))
        self.configure(height=self._target)
        if not self._closing and self._job is None and self.winfo_manager()=='place':self._offset=self._target;self.place_configure(y=-round(self._offset))
    def withdraw(self):self.place_forget()
    def overrideredirect(self,*args):pass
    def transient(self,*args):pass
    def protocol(self,*args):pass
    def geometry(self,value):
        match=re.match(r'\d+x(\d+)',value)
        self._target=min(int(match.group(1)) if match else self.content.winfo_reqheight()+2,max(100,self.host.winfo_height()-16))
        self.configure(height=self._target);self.pack_propagate(False)
    def winfo_reqheight(self):return self.content.winfo_reqheight()+2
    def winfo_reqwidth(self):return self.content.winfo_reqwidth()+2
    def deiconify(self):
        if not self.host.winfo_toplevel().winfo_viewable():self.host.winfo_toplevel().deiconify()
        self.host.update_idletasks();self._resize()
        self.place(relx=0,rely=1,relwidth=1,y=0,anchor='nw')
        def wheel(event):
            self.canvas.yview_scroll(-int(event.delta/120)*3,'units');return 'break'
        def bind_scroll(widget):
            widget.bindtags(message_bindtags(widget.bindtags(),str(self)))
            if not isinstance(widget,(tk.Text,ttk.Treeview,ttk.Scrollbar)):
                widget.bind('<MouseWheel>',wheel,add='+')
            for child in widget.winfo_children():bind_scroll(child)
        bind_scroll(self.content)
        self.lift();self._animate(self._target,0.18)
    def _animate(self,target,duration,done=None):
        if self._job is not None:self.after_cancel(self._job)
        start=self._offset;began=time.monotonic()
        def tick():
            self._job=None
            if not self.winfo_exists():return
            elapsed=time.monotonic()-began
            self._offset=slide_offset(start,target,elapsed,duration)
            self.place_configure(y=-round(self._offset))
            if elapsed<duration:self._job=self.after(16,tick)
            elif done is not None:done()
        tick()
    def destroy(self):
        if self._closing:return
        self._closing=True
        def finish():
            if self._host_binding is not None:
                try:self.host.unbind('<Configure>',self._host_binding)
                except tk.TclError:pass
                self._host_binding=None
            tk.Frame.destroy(self)
        if self.winfo_ismapped():self._animate(0,0.14,finish)
        else:finish()
