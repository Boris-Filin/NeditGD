from __future__ import annotations
from NeditGD.saveload import *
from NeditGD import Object

import json
from websocket import create_connection
from typing import List


WATERMARK_TEXT = [
    Object(id=914, x=-165, y=-15, _155=3, scale=0.75, text="Made with Nedit"),
    Object(id=914, x=-165, y=-30, _155=3, scale=0.5, text="by Nemo2510 and Nichie"),
    Object(id=914, x=-175, y=-41, _155=3, scale=0.35, text="github.com/Boris-Filin/NeditGD"),   
    Object(id=914, x=-147, y=-56, _155=3, scale=0.2, text="(You can remove this watermark, but we'd appreciate it if you didn't)"),
]

PREFIX = '[Nedit]:'

PAD = ' ' * len(PREFIX)

# The class that stores all loaded objects and handles
# interactions with the SaveLoad system for the user
# Behaves as singleton if only one instance exists ('last')
class Editor():
    default_layer = 20
    __last: Editor = None

    def __init__(self, live_edit: bool=True):
        self.__root = None
        self.__level_node = None
        self.__level_string = None
        self.__markers = None

        self.head = None
        self.objects = []
        self.loaded_obj_count = 0
        Editor.__last = self

        self.live_edit = live_edit
        if live_edit:
            self.init_socket()


    # -==========-
    # LIVE EDITING
    # -==========-

    def init_socket(self):
        try:
            self.socket = create_connection("ws://127.0.0.1:1313")
        except ConnectionRefusedError:
            raise ConnectionRefusedError('No editor socket found!\nCheck that you have WSLiveEdit enabled and your editor is open.')    

    def socket_load_data(self):
        packet = {
            "action": "GET_LEVEL_STRING"
        }
        self.socket.send(json.dumps(packet))
        response = self.socket.recv()
        raw = json.loads(response)
        if raw['status'] != 'successful':
            raise ConnectionError('[Nedit/WSL]: Level could not be read')
        data = raw['response']
        self.objects = read_level_objects(data)

    def socket_remove_group(self, group: int=9999):
        packet = {
            "action": "REMOVE_OBJECTS",
            "group": group
        }
        self.socket.send(json.dumps(packet))

    def socket_save_objects(self):
        scripted = self.get_scripted_objects()
        data = Object.list_to_robtop(scripted)

        packet = {
            "action": "ADD_OBJECTS",
            "objects": data
        }
        self.socket.send(json.dumps(packet))
    
    @classmethod
    def load_live_editor(cls, load_existing: bool=True, remove_scripted: bool=True):
        editor = Editor(live_edit=True)
        print("[Nedit/WSL]: Using current level")
        if load_existing:
            editor.socket_load_data()
        else:
            editor.objects = []
        if remove_scripted:
            editor.socket_remove_group(9999)
            editor.remove_scripted_objects()
        return editor
    



    # -==============-
    # SAVEFILE LOADING
    # -==============-

    # Create an editor object that automatically loads
    # the contents of the current level
    @classmethod
    def load_current_level(cls, remove_scripted: bool=True) -> Editor:
        editor = Editor(live_edit=False)
        editor.load_level_data()
        if remove_scripted:
            editor.remove_scripted_objects()
        editor.refresh_markers()
        return editor

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
        self.loaded_obj_count = len(self.objects)
    
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
        print(PREFIX, 'Level initialised successfully!')

    # Load the editor, reading objects from a provided string
    # instead of the game savefile
    @classmethod
    def load_from_robtop(cls, robtop: str) -> Editor:
        editor = Editor()
        editor.load_level_data(robtop)
        return editor
    
    @classmethod
    def get_last(_):
        if Editor.__last is None:
            raise ReferenceError('[Nedit]: Trying to access Editor when Editor has not been initialised!')
        return Editor.__last
    
    # Refresh the markers in the level
    def refresh_markers(self):
        from NeditGD.Nextra.marker_loader import MarkerLoader
        self.__markers = MarkerLoader(self)
   

    # Remove the previously scripted objects;
    # It is assumed that they are marked with group 9999
    def remove_scripted_objects(self) -> None:
        res = []
        for obj in self.objects:
            groups = obj.groups
            if groups is None or not 9999 in groups:
                res.append(obj)
        self.objects = res
        self.loaded_obj_count = len(self.objects)

    def get_scripted_objects(self) -> List[Object]:
        scripted = []
        for obj in self.objects:
            groups = obj.groups
            if groups is not None and 9999 in groups:
                scripted.append(obj)
        return scripted

    # Add an object to the editor object list;
    # Mark it with group 9999
    def add_object(self, obj: dict, mark_as_scripted: bool=True):
        if mark_as_scripted:
            Editor.add_group(obj, 9999)
        if obj.editor_layer_1 is None:
            obj.editor_layer_1 = Editor.default_layer

        self.objects.append(obj)

    @staticmethod
    def add_group_to_all(objects: list[Object], group: int) -> None:
        for obj in objects: Editor.add_group(obj, group)

    @staticmethod
    def add_group(obj: Object, group: int) -> None:
        if (groups := obj.groups) is None:
            obj.groups = [9999]
        else:
            groups.append(9999)

    # Add multiple ojects to the editor
    def add_objects(self, objects: list,
                    mark_as_scripted: bool=True,
                    message: str=''):
        message = f'\n{PAD}^ {message}' if message else ''
        for obj in objects:
            self.add_object(obj, mark_as_scripted)
        print(PREFIX, f'Added {len(objects)} objects to editor.{message}')

    # Get a string representing all objects in readable format
    def read_objects(self, oid_alias: bool=False):
        res = ''
        for obj in self.objects:
            res += obj.__str__(oid_alias=oid_alias) + '\n'
        return res

    # Write the editor object list to the current level file
    def save_changes(self):
        self.add_objects(WATERMARK_TEXT,
                         message='Watermark')
        obj_delta = len(self.objects) - \
             self.loaded_obj_count
        print(PREFIX, f'Added {obj_delta} objects total.')
        save_string = self.get_robtop_string()

        if self.live_edit:
            self.save_changes_live(save_string)
        else:
            self.save_changes_to_file(save_string)
        

    def save_changes_to_file(self, save_string: str):
        encrypted = encrypt_level_string(save_string.encode())
        set_level_data(self.__level_node, encrypted)

        xml_str = ET.tostring(self.__root)
        encryptGamesave(xml_str)
        print(PREFIX, 'Changes saved!')

    def save_changes_live(self, save_string: str):
        self.socket_save_objects()
        print('[Nedit/WSL]: Changes sent successfully')



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
            object_groups.update(set(obj.groups))
        object_groups.discard(9999)
        if not object_groups: return 0
        return max(object_groups)
    

    # Get the groups used in the level;
    # Only counts groups with assigned objects. Triggers with unused
    # targets are ignored.
    @staticmethod
    def get_used_groups(objects: list[Object]) -> list[int]:
        used_groups = set() 
        for obj in objects:
            if obj.groups is None: continue
            for group in obj.groups: used_groups.add(group)
        return list(used_groups)
        
    
    # Convert a list of values (groups, IDs, etc) to intervals.
    # Slightly inefficient but works.
    @staticmethod
    def get_intervals(vals: list[int]) -> list[tuple[int]]:
        if not vals: return None

        intervals = []
        interval_start = None
            
        for i in range(min(vals), max(vals) + 1):
            used = i in vals
            if interval_start is None:
                if used:
                    interval_start = i
            else:
                if not used:
                    intervals.append((interval_start, i - 1))
                    interval_start = None
        return intervals
    

    # -===========-
    # Extra methods
    # -===========-

    # Get the used groups in an easy-to-interact way
    def get_used_group_pool(self):
        from NeditGD.Nextra.group_pool import GroupPool
        return GroupPool(Editor.get_used_groups(self.objects))
    
    # Check if a given group pool overlaps with the editor's groups
    def validate_group_pool(self, group_pool):
        group_pool = self.get_used_group_pool()
        for group in self.get_used_groups():
            if group in group_pool:
                return False
        return True
    

    # -=====-
    # Markers
    # -=====-
    
    # Get the position of the marker with the given name
    def get_marker_position(self, name):
        return self.__markers.read_position(name)

    # Get the groups of the marker with the given name
    def get_marker_groups(self, name):
        return self.__markers.read_groups(name)
    
    # Get the first group of the marker
    def get_marker_group1(self, name):
        return self.get_marker_groups(name)[0]
    
    # Get the value of the marker with this prename
    def get_marker_var(self, name):
        return self.__markers.read_var(name)
    
    # Get the int value of the marker with this prename
    def get_marker_var_int(self, name):
        return self.__markers.read_var_int(name)


if __name__ == '__main__':
    edt = Editor.load_live_editor(load_existing=False, remove_scripted=False)
    # edt = Editor.load_current_level()
    edt.add_object(Object(id='spawn_t'))
    edt.save_changes()
    