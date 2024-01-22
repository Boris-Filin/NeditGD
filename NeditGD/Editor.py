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
        editor.load_level_data()
        if remove_scripted:
            editor.remove_scripted_objects()
        return editor
    

    # Load the editor, reading objects from a provided string
    # instead of the game savefile
    @classmethod
    def load_from_robtop(cls, robtop: str) -> Editor:
        editor = Editor()
        editor.load_level_data(robtop)
        return editor
    
    # @classmethod
    # def load_level_from_file(cls, path: str) -> Editor:
    #     editor = Editor()

    
    # Load the editor data
    def load_level_data(self, data: str = None) -> None:
        self.__root = read_gamesave_xml()
        self.__level_node = get_working_level_node(self.__root)
        if not self.__level_node.text:
            self.load_default_level()
            return
        level_data = get_working_level(self.__level_node)
        if data is not None:
            self.__level_string = data
        else:
            self.__level_string = get_working_level_string(level_data)
        self.head = read_level_head(self.__level_string)
        self.objects = read_level_objects(self.__level_string)
    
    # New levels aren't initialised until the player saves them for
    # the first time. This method loads the default data for a level
    # and initialises it ahead of GD.
    def load_default_level(self) -> None:
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(dir_path,"DefaultLevel")
            fr = open(file_path, "r")
            data = fr.read()
            fr.close()
        except:
            raise FileNotFoundError('Default level data missing!\n'
                                    'Reinstall the library or just'
                                    'save and exit the level in GD.')
        self.head = read_level_head(data)
        self.objects = []
        print('[Nedit]: Level initialised successfully!')

    # Remove the previously scripted objects;
    # It is assumed that they are marked with group 9999
    def remove_scripted_objects(self) -> None:
        res = []
        for obj in self.objects:
            groups = obj.groups
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
        print(f'[Nedit]: Added {len(objects)} objects to editor.')

    # Get a string representing all objects in readable format
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


    # Get the highest group from the given list of objects
    @staticmethod
    def get_max_group(objects: list[Object]=None) -> int:
        object_groups = set()
        for obj in objects:
            if obj.groups is None: continue
            print(obj.groups)
            object_groups.update(set(obj.groups))
        object_groups.discard(9999)
        if not object_groups: return 0
        return max(object_groups)
        
