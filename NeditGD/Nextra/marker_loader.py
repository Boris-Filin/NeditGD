from editor_gd import Editor
from object_gd import Object
from typing import Tuple

class MarkerLoader():
    prefixes = ['@', '#']

    def __init__(self, editor: Editor):
        self.__editor = editor
        self.__markers = []
        self.__find_markers()

    def __find_markers(self):
        from Dictionaries.IDNames import OBJECT_IDS
        for obj in self.__editor.objects:
            if obj.id != OBJECT_IDS['text']: continue
            ps, text = MarkerLoader.strip_prefixes(obj.text)
            self.__markers.append((ps, text, obj))

    @staticmethod
    def strip_prefixes(text: str) -> Tuple:
        ps = set()
        while text and text[0] in MarkerLoader.prefixes:
            ps.add(text[0])
            text = text[1:]
        return (ps, text)


    def find_marker(self, p: str, name: str) -> Object:
        for ps, marker_name, obj in self.__markers:
            if not p in ps: continue
            if marker_name == name: return obj
        return None

    def read_position(self, name: str) -> Tuple[float]:
        obj = self.find_marker('@', name)
        if obj is None: return (0, 0)
        return obj.x, obj.y
    
    def read_groups(self, name: str) -> list[int]:
        obj = self.find_marker('#', name)
        if obj is None: return []
        return obj.groups