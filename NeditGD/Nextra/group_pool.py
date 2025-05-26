from __future__ import annotations
from collections.abc import Iterable, Callable
from bisect import bisect_left


class GroupPool():
    left = 1
    right = 9999
    
    def __init__(self, groups: Iterable[int]):
        self.values = list(groups)
        self.__cleanup()
        self.idx = 0

    def __cleanup(self):
        self.values = list(set(self.values))
        self.values.sort()

    def get_ranges(self):
        start = self.values[0]
        last = start
        rs = []
        for v in self.values:
            if v - last > 1:
                rs.append((start, last))
                start = v
            last = v
        rs.append((start, last))
        return rs
    
    def __str__(self):
        prettify = lambda p : f' {p[0]} - {p[1]}' \
                    if p[1] != p[0] else f' {p[0]}'
        pairs = map(prettify, self.get_ranges())
        current = 'END' if not self.has_free_groups()\
                        else f'{self.current()}'
        return '\n'.join(pairs) + f'\nnext: {current}'


    # -===============-
    # POOL MANIPULATION
    # -===============-

    def filter(self, func: Callable):
        current = self.values[self.idx]
        self.values = [v for v in self.values
                       if func(v)]
        self.idx = bisect_left(self.values, current)

    # Remove all groups that appear in the iterable.
    # Supports - and -= syntax.
    # Decrements idx to point to the same value.
    def remove_all(self, to_remove: Iterable[int]):
        self.filter(lambda v : v not in to_remove)
        
    def __isub__(self, to_remove: Iterable[int]):
        self.remove_all(to_remove)
        return self

    def __sub__(self, to_remove: Iterable[int]):
        gp = GroupPool(self.values)
        gp -= to_remove
        return gp
    
    def remove(self, to_remove: int):
        self.add_all([to_remove])
    

    # Add all groups from an iterable.
    # Supports + and += syntax.
    # Increments idx to point to the same value.
    def add_all(self, to_add: Iterable[int]):
        current = self.values[self.idx]
        self.values.extend(to_add)
        self.__cleanup()
        self.idx = bisect_left(self.values, current)

    def __iadd__(self, to_add: Iterable[int]):
        self.add_all(to_add)
        return self

    def __add__(self, to_add: Iterable[int]):
        gp = GroupPool(self.values)
        gp += to_add
        return gp
    
    def add(self, to_add: int):
        self.add_all([to_add])
    

    def get_min(self) -> int:
        return self.values[0]
    
    def get_max(self) -> int:
        return self.values[-1]

    # Filter based on the minimum value (inclusive)
    def cull_min(self, m: int):
        self.filter(lambda v : v >= m)

    # Filter based on the maximum value (inclusive)
    def cull_max(self, m: int):
        self.filter(lambda v : v <= m)


    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    # -==================-
    # POINTER MANIPULATION 
    # -==================-


    def is_empty(self) -> bool:
        return len(self.values) == 0
    
    def has_free_groups(self) -> bool:
        return self.idx < len(self)

    def next(self, safe: bool=False, incr: bool=True) -> int:
        if not self.has_free_groups():
            if safe: return None
            raise StopIteration()
        if not incr:
            return self.values[self.idx]
        self.idx += 1
        return self.values[self.idx-1]

    def current(self, safe: bool=False) -> int:
        return self.next(safe=safe, incr=False)
    
    def reset(self):
        self.idx = 0

    # -===========-
    # CUSTOM POOLS
    # -===========-

    @classmethod
    def since(cls, start: int) -> GroupPool:
        vals = range(start, GroupPool.right)
        return cls(vals)

    @classmethod    
    def reverse(cls, start: int) -> GroupPool:
        vals = range(start, GroupPool.left, -1)
        return cls(vals)




if __name__ == '__main__':
    groups = range(10, 20)
    gp = GroupPool(groups)

    gp += [2, 42]
    gp = gp - [15]

    print(1)
    print(gp.values)
    print(gp)

    print(2)
    for i in range(len(gp) // 2):
        print(gp.next())

    print(3)
    print(gp.values)
    print(gp[-1])

    print(4)
    gp -= [12, 16, 17]
    print(gp.values)

    print(5)
    gp += [5, 13, 18]
    print(gp.values)
    print(gp)

    print(6)
    gp.cull_min(18)
    print(gp.values)
    print(type(gp.values))
    print(gp.idx)
    print(gp.values[gp.idx])
    print(gp)

    print(7)
    print(12 in gp)
    print(42 in gp)
