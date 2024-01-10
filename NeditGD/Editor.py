from __future__ import annotations
from SaveLoad import *
from Object import Object


WATERMARK_TEXT = [
    Object(id=914, x=-165, y=-15, scale=0.75,
           text="Made with Nedit"),
    Object(id=914, x=-213, y=-33, scale=0.5,
           text="by Nemo2510"),
    Object(id=914, x=-135, y=-45, scale=0.2,
           text="(You can remove this watermark, "
           "but we'd appreciate it if you didn't)")
]

# The class that stores all loaded objects and handles
# interactions with the SaveLoad system for the user
class Editor():
    __root = None
    __level_node = None
    __level_string = None
    head = None
    objects = None

    # Create an editor object that automatically loads
    # the contents of the current level
    @classmethod
    def load_current_level(cls, remove_scripted: bool=True) -> Editor:
        editor = Editor()
        editor.__root = read_gamesave_xml()
        editor.__level_node = get_working_level_node(editor.__root)
        level_data = get_working_level(editor.__level_node)
        editor.__level_string = get_working_level_string(level_data)
        editor.head = read_level_head(editor.__level_string)
        editor.objects = read_level_objects(editor.__level_string)
        if remove_scripted:
            editor.remove_scripted_objects()
        return editor
    

    # Load the editor, reading objects from a provided string
    # instead of the game savefile
    @classmethod
    def load_from_robtop(cls, robtop: str) -> Editor:
        editor = Editor()
        editor.__root = read_gamesave_xml()
        editor.__level_node = get_working_level_node(editor.__root)
        editor.__level_string = robtop
        editor.head = read_level_head(editor.__level_string)
        editor.objects = read_level_objects(editor.__level_string)
        return editor


    # Remove the previously scripted objects;
    # It is assumed that they are marked with group 9999
    def remove_scripted_objects(self) -> None:
        res = []
        for obj in self.objects:
            groups = obj.get('groups')
            if groups is None or not 9999 in groups:
                res.append(obj)
        self.objects = res

    # Add an object to the editor object list;
    # Mark it with group 9999
    def add_object(self, obj: dict, mark_as_scripted: bool=True):
        if mark_as_scripted:
            groups = obj.groups
            if groups is None:
                obj.groups = [9999]
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
        self.add_objects(WATERMARK_TEXT)

        save_string = self.get_robtop_string()
        encrypted = encrypt_level_string(save_string.encode())
        set_level_data(self.__level_node, encrypted)

        xml_str = ET.tostring(self.__root)
        encryptGamesave(xml_str)
        print('[Nedit]: Changes saved!')


    # Get the string representation of the current level
    # with RobTop's encoding
    def get_robtop_string(self) -> str:
        return get_level_save_string(self.objects, self.head)

