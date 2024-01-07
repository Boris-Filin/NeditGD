from Editor import Editor

if __name__ == '__main__':
    editor = Editor.load_current_level()
    for obj in editor.objects:
        print(obj)
