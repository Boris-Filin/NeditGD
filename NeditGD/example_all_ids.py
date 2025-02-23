from NeditGD import Editor, Object, HSV


# This example creates a board of all available objects in the
# game along with their IDs.

if __name__ == '__main__':
    editor = Editor.load_current_level()

    row_width = 500

    for i in range(1, 4000):
        # Add the object
        editor.add_object(Object(
            id = i,
            x = 300 + 60 * (i % row_width),
            y = 300 + 60 * (i // row_width)
        ))
        # Add the id text
        editor.add_object(Object(
            id = 914,
            x = 300 + 60
             * (i % row_width),
            y = 300 + 60 * (i // row_width) - 20,
            scale = 0.5,
            text = str(i)
        ))

    editor.save_changes()