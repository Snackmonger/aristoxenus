"""Functions used by the GUI"""

from tkinter import Widget, NORMAL, DISABLED
from typing import Any, Sequence

def enable_children(parent: Widget, enabled: bool=True):
    """Recursively en-/dis-able the dependents of the 
    given widget.

    From https://stackoverflow.com/a/77112129/22371397
    """
    for child in parent.winfo_children():
        wtype: str = child.winfo_class()
        if wtype not in ('Frame', 'Labelframe', 'TFrame', 'TLabelframe'):
            child.configure(state=NORMAL if enabled else DISABLED)
        else:
            enable_children(child, enabled)


def enable_widget(widget: Widget, enabled: bool=True):
    """En-/dis-able the given widget and recursively en-/dis-able any 
    dependents of the given widget.

    From https://stackoverflow.com/a/77112129/22371397
    """
    wtype: str = widget.winfo_class()
    if wtype not in ('Frame', 'Labelframe', 'TFrame', 'TLabelframe'):
        widget.configure(state=NORMAL if enabled else DISABLED)
    else:
        enable_children(widget, enabled)


def cycle_indices(sequence: Sequence[Any], member: Any) -> int:
    """For the given sequence, return the index that comes after the index 
    of the given member, or 0 if member is the last index.
    
    This function operates on the assumption that all members in the sequence
    will be unique."""
    i: int = sequence.index(member)
    return 0 if i == len(sequence) -1 else i + 1