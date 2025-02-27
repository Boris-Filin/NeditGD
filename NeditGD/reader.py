from editor_gd import Editor
import sys

def read_objects(editor: Editor):
    print("[Nedit]: Objects in level:")
    print(editor.read_objects(oid_alias='alias' in sys.argv))

def read_ids(editor: Editor):
    print("[Nedit]: IDs of objects in level:")
    objects = editor.objects[:]
    objects.sort(key = lambda o : o.x)
    for obj in objects:
        print(obj.id)

def read_groups(editor: Editor):
    print("[Nedit]: Groups used in the level:")
    print(editor.get_used_group_pool())

# This script simply reads and prints the current level
if __name__ == '__main__':
    editor = Editor.load_current_level()

    # TODO: Replace with proper command line args
    if 'id' in sys.argv:
        read_ids(editor)
    elif 'groups' in sys.argv:
        read_groups(editor)
    else:
        read_objects(editor)