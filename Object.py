from __future__ import annotations
from collections import UserDict
from typing import Any
from Dictionaries.PropertyID import NAME_TO_ID
import Properties


class Object(UserDict):
    def __init__(self, **kwargs):
        super().__init__({1:1, 2:0, 3:0, 155:1})
        for k, v in kwargs.items():
            self.__setitem__(k, v)



    def __setitem__(self, key: int | str, item: Any) -> None:
        if type(key) is int:
            return self.data.__setitem__(key, item)
        if (_id := NAME_TO_ID.get(key)) is not None:
            return self.data.__setitem__(_id, item)
        try:
            _id = int(key[1:])
            return self.data.__setitem__(_id, item)
        except: pass
        raise KeyError(f'Objects have no property called \'{key}\'.')
    
    def __getitem__(self, key: int | str) -> Any:
        if type(key) is int:
            return self.data.__getitem__(key)
        if (_id := NAME_TO_ID.get(key)) is not None:
            return self.data.__getitem__(_id)
        try:
            _id = int(key[1:])
            return self.data.__getitem__(_id)
        except: pass

        raise KeyError()
    


    def __setattr__(self, __name: str, __value: Any) -> None:
        if hasattr(self, __name):
            super().__setattr__(__name, __value)
        if (_id := NAME_TO_ID.get(__name)) is not None:
            return self.data.__setitem__(_id, __value)
        try:
            _id = int(__name[1:])
            return self.data.__setitem__(_id, __value)
        except ValueError:
            pass
        except AttributeError:
            raise AttributeError(
                f'Objects have no property called \'{__name}\'.')

    
    def __getattr__(self, __name):
        if (_id := NAME_TO_ID.get(__name)) is not None:
            return self.data.__getitem__(_id)
        try:
            _id = int(__name[1:])
            return self.data.__getitem__(_id)
        except:
            pass
    


    @classmethod
    def from_robtop(cls, rob: str) -> Object:
        obj = {}
        arr_obj = rob.split(',')
        encoded_pairs = [(arr_obj[i], arr_obj[i+1])
                        for i in range(0, len(arr_obj), 2)]
        for (k, v) in encoded_pairs:
            obj[f'_{k}'] = Properties.decode_property_pair(int(k), v)
        return Object(**obj)
    
    def to_robtop(self) -> str:
        res = ''
        for (k, v) in self.data.items():
            res += Properties.encode_property(k, v)
        return res[:-1]
    


    def __str__(self) -> str:
        descr = ''
        for k, v in self.data.items():
            key_str = f'_{k}'
            for name, _id in NAME_TO_ID.items():
                if _id == k:
                    key_str = name
                    break
            descr += f'{key_str}: {v}, '
        descr = f'Object({descr[:-2]})'
        return descr


    
if __name__ == '__main__':
    obj = Object(id=2, groups=[1, 2])
    # obj['id'] = 1
    obj[2] = 15
    print(obj[1], obj['x'], obj['y'], obj['groups'])
    obj._4 = 1
    print(obj.x)
    print(obj[4])
    obj._57 = []
    print(obj.to_robtop())
