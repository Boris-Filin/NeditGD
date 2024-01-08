from SaveLoad import *


GROUPS = 57

class Editor():
    __root = None
    __level_node = None
    head = None
    objects = None

    # Create an editor object that automatically loads
    # the contents of the current level
    @classmethod
    def load_current_level(cls, remove_scripted: bool=True) -> object:
        editor = Editor()
        editor.__root = read_gamesave_xml()
        editor.__level_node = get_working_level_node(editor.__root)
        level_data = get_working_level(editor.__level_node)
        level_str = get_working_level_string(level_data)
        editor.head = read_level_head(level_str)
        editor.objects = read_level_objects(level_str)
        if remove_scripted:
            editor.remove_scripted_objects()
        return editor


    # Remove the previously scripted objects;
    # It is assumed that they are marked with group 9999
    def remove_scripted_objects(self) -> None:
        res = []
        for obj in self.objects:
            groups = obj.get(GROUPS)
            if groups is None or not 9999 in groups:
                res.append(obj)
        self.objects = res

    # Add an object to the editor object list;
    # Mark it with group 9999
    def add_object(self, obj: dict, mark_as_scripted: bool=True):
        if mark_as_scripted:
            groups = obj.get(57)
            if groups is None:
                obj[GROUPS] = [9999]
            else:
                groups.append(9999)
        self.objects.append(obj)

    # Add multiple ojects to the editor
    def add_objects(self, objects: list, mark_as_scripted: bool=True):
        for obj in objects:
            self.add_object(obj, mark_as_scripted)

    def read_objects(self):
        res = ''
        for obj in self.objects:
            res += str(obj) + '\n'
        return res

    # Write the editor object list to the current level file
    def save_changes(self):
        save_string = get_level_save_string(self.objects, self.head)
        encrypted = encrypt_level_string(save_string.encode())
        set_level_data(self.__level_node, encrypted)

        dec_enc = get_working_level_string(encrypted)
        print(read_level_objects(dec_enc))

        xml_str = ET.tostring(self.__root)
        encryptGamesave(xml_str)

