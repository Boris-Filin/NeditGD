from NeditGD.editor_gd import Editor
from NeditGD.object_gd import Object
from typing import Tuple

class MarkerLoader():
    prefixes = ['@', '#', '$']
    assign_op = '='

    def __init__(self, editor: Editor):
        self.__editor = editor
        self.__markers = []
        self.__find_markers()

    def __find_markers(self):
        from NeditGD.Dictionaries.IDNames import OBJECT_IDS
        for obj in self.__editor.objects:
            if obj.id != OBJECT_IDS['text']: continue
            ps, text = MarkerLoader.strip_prefixes(obj.text)
            self.__markers.append((ps, text, obj))

    @staticmethod
    def strip_prefixes(text: str) -> Tuple[str]:
        ps = set()
        while text and text[0] in MarkerLoader.prefixes:
            ps.add(text[0])
            text = text[1:]
        return (ps, text)
    
    @staticmethod
    def parse_marker_value(text: str) -> Tuple:
        vals = text.split(MarkerLoader.assign_op)
        vals = [v.strip() for v in vals]
        if len(vals) < 2:
            raise ValueError("Var marker missing \'=\'!")
        return (vals[0], vals[1:])


    def find_marker(self, p: str, name: str) -> Object:
        for ps, marker_name, obj in self.__markers:
            if not p in ps: continue
            if marker_name == name: return obj
        return None
    
    def find_marker_values(self, p: str, name: str) -> str:
        for ps, marker_name, obj in self.__markers:
            if not p in ps: continue
            prename, vals = MarkerLoader.parse_marker_value(marker_name)
            if prename == name: return vals
        return []

    def read_position(self, name: str) -> Tuple[float]:
        obj = self.find_marker('@', name)
        if obj is None: return (0, 0)
        return obj.x, obj.y
    
    def read_groups(self, name: str) -> list[int]:
        obj = self.find_marker('#', name)
        if obj is None: return []
        return obj.groups
    
    def read_var(self, name: str) -> str:
        vals = self.find_marker_values('$', name)
        return vals[0]

    def read_var_int(self, name: str) -> int:
        return int(self.read_var(name))