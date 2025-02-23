from collections.abc import Iterable

class GroupPool():
    
    def __init__(self, groups: Iterable[int]):
        self.values = list(groups)
        self.__cleanup()
        self.idx = 0

    def __cleanup(self):
        self.values = list(set(self.values))
        self.values.sort()

    # -===============-
    # POOL MANIPULATION
    # -===============-

    # Remove all groups that appear in the iterable.
    # Supports - and -= syntax.
    def remove_all(self, to_remove: Iterable[int]):
        self.values = {v for v in self.values
                       if not v in to_remove}
        
    def __isub__(self, to_remove: Iterable[int]):
        self.remove_all(to_remove)

    def __sub__(self, to_remove: Iterable[int]):
        gp = GroupPool(self.values)
        gp += to_remove
        return gp
    

    # Add all groups from an iterable.
    # Supports + and += syntax.
    def add_all(self, to_add: Iterable[int]):
        self.values.extend(to_add)
        self.__cleanup()

    def __iadd__(self, to_add: Iterable[int]):
        self.add_all(to_add)

    def __add__(self, to_add: Iterable[int]):
        gp = GroupPool(self.values)
        gp += to_add
        return gp


    def __len__(self):
        return len(self.values)


    # -==================-
    # POINTER MANIPULATION 
    # -==================-


    def is_empty(self) -> bool:
        return len(self.values)
    
    def has_free_groups(self) -> bool:
        return self.idx < len(self)

    def next(self) -> int:
        # if i 
        return self.values[idx]

