from __future__ import annotations
from NeditGD import *

import numpy as np
from numpy import ndarray, array
from itertools import product
from collections.abc import Iterable

from typing import Iterable


class Pos(ndarray):
    def __new__(cls, *vals, **kwargs):
        if isinstance(vals[0], Iterable):
            vals = vals[0]
        elif not vals:
            vals = (0,0)
        n = min(len(vals), 3)
        buf = array(vals[:n], dtype=float)
        return super().__new__(cls, n, float, buf)

    @property
    def x(self): return self[0]
    @x.setter
    def x(self, val): self[0] = val
    @property
    def x_int(self): return int(self.x)

    @property
    def y(self): return self[1]
    @y.setter
    def y(self, val): self[1] = val
    @property
    def y_int(self): return int(self.y)
    
    @property
    def z(self): return self[2]
    @z.setter
    def z(self, val): self[2] = val
    @property
    def z_int(self): return int(self.z)

    @property
    def tuple(self): return tuple(self)
    @property
    def tuple_int(self): return tuple(int(v) for v in self)

    def snap(self):
        for i, v in enumerate(self):
            self[i] = np.round(v)

    def __eq__(self, other):
        return super().__eq__(other).all().item()
    def __ne__(self, other):
        return super().__ne__(other).all().item()
    def __lt__(self, other):
        return super().__lt__(other).all().item()
    def __le__(self, other):
        return super().__le__(other).all().item()
    def __gt__(self, other):
        return super().__gt__(other).all().item()
    def __ge__(self, other):
        return super().__ge__(other).all().item()
    


    
    @property
    def length_squared(self):
        return (self * self).sum()
    @property
    def length(self):
        return np.sqrt(self.length_squared)
    @property
    def unit(self):
        return self / self.length
    
    def dot(self, other: Pos):
        return (self * other).sum()
    
    @property
    def volume(self):
        return self.prod().item()
    @property
    def volume_int(self):
        return int(self.volume)
    
    @classmethod
    def pos_list(cls, ps):
        return [Pos(*p) for p in ps]
    
    @classmethod
    def zero2(cls): return cls(0,0)
    @classmethod
    def zero3(cls): return cls(0,0,0)
    

    def flatten_in_volume(self, bound: Pos):
        return self.z * bound.x * bound.y + \
                self.y * bound.x + self.x
    
    def get_pos_index(self, x, y=0, z=0):
        return int(x + y * self.x + z * self.x * self.y)
    
    def range2d(self): return range2d(self)
    def range3d(self): return range3d(self)
    
def range2d(pos_a: Pos, pos_b: Pos=None):
    if pos_b is None:
        pos_b = pos_a
        pos_a = Pos(0,0)
    x_range = np.arange(pos_a.x, pos_b.x, 1, dtype=int)
    y_range = np.arange(pos_a.y, pos_b.y, 1, dtype=int)
    prod = product(y_range, x_range)
    prod = [pos[::-1] for pos in prod]
    return Pos.pos_list(prod)

def range3d(pos_a: Pos, pos_b: Pos=None):
    if pos_b is None:
        pos_b = pos_a
        pos_a = Pos(0,0,0)
    x_range = np.arange(pos_a.x, pos_b.x, 1, dtype=int)
    y_range = np.arange(pos_a.y, pos_b.y, 1, dtype=int)
    z_range = np.arange(pos_a.z, pos_b.z, 1, dtype=int)
    prod = product(z_range, y_range, x_range)
    prod = [pos[::-1] for pos in prod]
    return Pos.pos_list(prod)