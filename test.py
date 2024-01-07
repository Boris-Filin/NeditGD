from Editor import Editor

editor = Editor.load_current_level()
editor.add_object({1:500, 2:-15, 3:45})
editor.save_changes()