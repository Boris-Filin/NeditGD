from Editor import Editor, Object
from Dictionaries.PropertyHSV import HSV

# This is an example of how to use the library:
#   1. Load the most recent level using Editor.load_current_level()
#   2. Make all the necessary changes (add/delete objects)
#   3. Save your changes with editor.save_changes()

emitter_id = -1

if __name__ == '__main__':
    editor = Editor.load_current_level()

    obj = Object(id=1, x=75, y=-15, groups=[12, 42], scale=5)
    obj.hsv_enabled = 1
    obj.hsv = HSV(20, 1.3, 0.7, True)
    editor.add_object(obj)

    editor.add_object(Object(
        id=1268, #Spawn trigger
        x=15,
        y=15,
        spawn_remap=[(1, 2), (3, 4)]
    ))
    
    editor.save_changes()