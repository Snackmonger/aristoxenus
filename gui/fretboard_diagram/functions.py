from tkinter import Widget, NORMAL, DISABLED

def enable_children(parent: Widget, enabled: bool=True):
    for child in parent.winfo_children():
        wtype: str = child.winfo_class()
        if wtype not in ('Frame', 'Labelframe', 'TFrame', 'TLabelframe'):
            child.configure(state=NORMAL if enabled else DISABLED)
        else:
            enable_children(child, enabled)


def enable_widget(widget: Widget, enabled: bool=True):
    wtype = widget.winfo_class()
    if wtype not in ('Frame', 'Labelframe', 'TFrame', 'TLabelframe'):
        widget.configure(state=NORMAL if enabled else DISABLED)
    else:
        enable_children(widget, enabled)