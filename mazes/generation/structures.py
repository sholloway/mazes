# from collections import namedtuple
from typing import NamedTuple

"""
Convenience tuples for working with cell coordinates. 
"""
# Point = namedtuple('Point', ['x','y'])
class Point(NamedTuple):
  x: int
  y: int 
  
Corner = Point