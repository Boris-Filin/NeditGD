from editor_gd import Editor
import sys
from argparse import ArgumentParser


def read_objects(editor: Editor, args):
    print("[Nedit]: Objects in level:")
    objects = editor.read_objects(
        oid_alias=args.alias)
    print(objects)

def read_ids(editor: Editor, args):
    print("[Nedit]: IDs of objects in level:")
    objects = editor.objects[:]
    objects.sort(key = lambda o : o.x)
    for obj in objects:
        print(obj.id)

def read_groups(editor: Editor, args):
    print("[Nedit]: Groups used in the level:")
    print(editor.get_used_group_pool())

def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-m', '--mode', type=str,
        choices=['obj', 'id', 'groups'],
        default='obj', required=False)
    parser.add_argument(
        '-a', '--alias', type=bool,
        default=False, required=False)
    parser.add_argument(
        '-s', '--scripted', type=bool,
        default=False, required=False)
    parser.add_argument(
        '-g', '--group', type=int)
    
    
    
    args = parser.parse_args()

    edt = Editor.load_current_level(
        remove_scripted=not args.scripted)

    if args.group is not None:
        edt.objects = [o for o in edt.objects \
                       if o.groups is not None and \
                        args.group in o.groups]

    if args.mode == 'obj':
        read_objects(edt, args)
    elif args.mode == 'id':
        read_ids(edt, args)
    elif args.mode == 'groups':
        read_groups(edt, args)

    
# This script simply reads and prints the current level
if __name__ == '__main__':

    main()
