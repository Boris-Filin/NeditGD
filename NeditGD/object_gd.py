from __future__ import annotations
from collections import UserDict
from typing import Any, Iterable
from numbers import Number
from copy import deepcopy
from NeditGD.Dictionaries.PropertyID import get_property_id
from NeditGD.Dictionaries.IDNames import oid_from_alias, oid_to_alias
import NeditGD.properties as properties

# A class that represents a Geometry Dash object
# as a dictionary containing all of its properties.
# Each property can be accesed either with its property id
# (decided by RobTop), or by a string alias (assigned by Nedit).
class Object(UserDict):

    _aliases = {}

    # The object can be initialised with some properties;
    # id, x, y, and _155 have to be set by default.
    def __init__(self, **kwargs):
        super().__init__({1:1, 2:0, 3:0, 155:1})
        for k, v in kwargs.items():
            self.__setitem__(k, v)

    # Sometimes you need to create multiple objects with slightly
    # different parameters. The copied object is passed, along with
    # the changed properties and their new values.
    @classmethod
    def copy(cls, original: Object, **kwargs) -> Object:
        obj = deepcopy(original)
        for k, v in kwargs.items():
            obj[k] = v
        return obj

    # When the object is accessed as a dictionary,
    # it automatically converts property aliases to integer ids
    def __setitem__(self, key: int | str, item: Any) -> None:
        if type(key) is int or \
            Object.is_tmp_key(key):
            return self.set_item_int_key(key, item)
        if (_id := get_property_id(key)) is not None:
            return self.set_item_int_key(_id, item)
        try:
            _id = int(key[1:])
            return self.set_item_int_key(_id, item)
        except: pass
        raise KeyError(f'Objects have no property called \'{key}\'.')
    

    # Set an item given an integer key;
    # Change oid aliases to int oids
    def set_item_int_key(self, key: int, item: Any) -> None:
        if key == 1 and type(item) is str:
            item = oid_from_alias(item)
        return self.data.__setitem__(key, item)

    
    # When the object is accessed as a dictionary,
    # it automatically converts property aliases to integer ids
    def __getitem__(self, key: int | str) -> Any:
        if type(key) is int or \
            Object.is_tmp_key(key):
            return self.data.__getitem__(key)
        if (_id := get_property_id(key)) is not None:
            return self.data.__getitem__(_id)
        try:
            _id = int(key[1:])
            return self.data.__getitem__(_id)
        except: pass

        raise KeyError()
    


    # When a property is accessed as a Python property, it is
    # converted to integer id and fetched from the object dictionary.
    def __setattr__(self, __name: str, __value: Any) -> None:
        if (_id := get_property_id(__name)) is not None:
            if _id == 1 and type(__value) is str:
                __value = oid_from_alias(__value)
            return self.data.__setitem__(_id, __value)
        elif Object.is_tmp_key(__name):
            return self.data.__setitem__(__name, __value)
        try:
            _id = int(__name[1:])
            return self.data.__setitem__(_id, __value)
        except:
            super().__setattr__(__name, __value)

    # When a property is accessed as a Python property, it is
    # converted to integer id and fetched from the object dictionary.
    def __getattr__(self, __name):
        if (_id := get_property_id(__name)) is not None:
            return self.data.get(_id)
        elif Object.is_tmp_key(__name):
            return self.data.get(__name)
        try:
            _id = int(__name[1:])
            return self.data.get(_id)
        except:
            return super().__getattr__(__name)


    # When loading from a game save, every object is
    # reconstructed from RobTop's string encoding.
    @classmethod
    def from_robtop(cls, rob: str) -> Object:
        obj = {}
        arr_obj = rob.split(',')
        encoded_pairs = [(arr_obj[i], arr_obj[i+1])
                        for i in range(0, len(arr_obj), 2)]
        for (k, v) in encoded_pairs:
            obj[f'_{k}'] = properties.decode_property_pair(int(k), v)
        return Object(**obj)
    
    # To save an object, it is converted to RobTop's string encoding.
    def to_robtop(self) -> str:
        res = ''
        for (k, v) in self.data.items():
            if Object.is_tmp_key(k): continue
            res += properties.encode_property(k, v)
        return res[:-1]

    @staticmethod
    def list_to_robtop(objects: Iterable[Object]):
        return ';'.join(obj.to_robtop() for obj in objects)
    

    # The string representation of the object uses property aliases,
    # which have to be deduced from property ids.
    def __str__(self, include_tmp: bool=True, oid_alias=False) -> str:
        descr = ''
        for k, v in self.data.items():
            if Object.is_tmp_key(k):
                if not include_tmp: continue
                key_str = k
            else:
                key_str = properties.get_property_name(k)
            
            if oid_alias and k == 1:
                v = oid_to_alias(v)

            if type(v) is str:
                descr += f'{key_str}=\"{v}\", '
            else:
                descr += f'{key_str}={v}, '
        descr = f'{type(self).__name__}({descr[:-2]})'
        return descr
    
    @staticmethod
    def is_tmp_key(k: str):

        return type(k) is str and \
               len(k) > 2 and \
               k[:1] + k[-1:] == '__'

    # -===============-
    # QoL functionality
    # -===============-
    
    def move(self, x: Number|Iterable, y: Number=None):
        if y is None:
            x, y = x
        self.x += x
        self.y += y
        return self
    
    def move_to(self, x: Number|Iterable, y: Number=None):
        if y is None:
            x, y = x
        self.x = x
        self.y = y
        return self
    
    def add_group(self, group):
        if self.groups is None:
            self.groups = []
        self.groups.append(group)
        return self
    
    def to_layer(self, layer: int):
        self.editor_layer_1 = layer
        return self





def get_dist(x: float, y: float=None) -> tuple[float] | float:
    if y is None:
        return x * 30
    return (x * 30, y * 30)


def get_pos(x: float, y: float=None) -> tuple[float] | float:
    if y is None:
        return x * 30 + 15
    return (x * 30 + 15, y * 30 + 15)


    
if __name__ == '__main__':
    obj = Object(id=2, groups=[1, 2])
    # obj['id'] = 1
    obj[2] = 15
    print(obj[1], obj['x'], obj['y'], obj['groups'])
    obj._4 = 1
    print(obj.x)
    print(obj._private_)
    obj._private_ = 42
    print(obj)
    print('>', obj['_private_'])
    print('>', obj._private_)
    print(obj[4])
    # print(obj[5])
    obj._57 = []
    print(obj.to_robtop())

    # obj._42 = 'trace'
    obj['_42'] = 'trace'

    print(obj)
    print(obj._aliases)
