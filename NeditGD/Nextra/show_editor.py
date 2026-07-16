from __future__ import annotations
from NeditGD import *

def ifnull(var, val):
    if var is None:
        return val
    return var

def show_editor(editor: Editor, filter_group_id: int = 0) -> None:
    """
    Merely prints the objects of the given editor
    for people who would like to copy GD objects into Python syntax
    """
    print('[')
    for obj in editor.objects:
        if filter_group_id == 0 or filter_group_id in ifnull(obj.groups, []):
            print(str(obj) + ',')
    print(']')

def show_live_editor(filter_group_id: int = 0):
    """
    Prints the objects of the current opened editor
    """
    editor = Editor.load_live_editor(load_existing=True, remove_scripted=False)
    show_editor(editor, filter_group_id)



if __name__ == "__main__":
    show_live_editor()