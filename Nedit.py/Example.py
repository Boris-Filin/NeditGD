from Editor import Editor, Object

# This is an example of how to use the library:
#   1. Load the most recent level using Editor.load_current_level()
#   2. Make all the necessary changes (add/delete objects)
#   3. Save your changes with editor.save_changes()

if __name__ == '__main__':
    editor = Editor.load_current_level()
    editor.add_object(Object(id=1, x=75, y=-15, groups=[12, 42], scale=5))
    editor.save_changes()