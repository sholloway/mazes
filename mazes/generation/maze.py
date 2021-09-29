from enum import Enum
from typing import List, Dict, Optional

from generation.direction import Direction
from generation.structures import Point

class MazeCell:
  """
  Represents a traversable room in a maze.
  """
  _location: Point
  _walls: dict[Enum, bool]
  _visited:bool
  
  def __init__(self, x: int, y: int) -> None:
    self._location = Point(x,y)
    self._walls = {
      Direction.NORTH: True,
      Direction.EAST: True,
      Direction.SOUTH: True,
      Direction.WEST: True
    }
    self._visited:bool = False

  @property
  def location(self) -> Point: return self._location

  @property
  def north(self) -> bool: return self._walls[Direction.NORTH]
  
  @property
  def south(self) -> bool: return self._walls[Direction.SOUTH]
  
  @property
  def east(self) -> bool: return self._walls[Direction.EAST]
  
  @property
  def west(self) -> bool: return self._walls[Direction.WEST]

  def visit(self) -> None:
    self._visited = True

  @property
  def visited(self) -> bool:
    return self._visited

  def remove_wall(self, wall: Direction) -> None:
    self._walls[wall] = False

class Maze:
  """
  Represents a maze of connected cells. A "cell" is simple a space a person could occupy.
  """
  _grid: List[List[MazeCell]]
  _width: int
  _height: int
  starting_cell: MazeCell
  exit_cell: MazeCell

  def __init__(self, width: int, height: int) -> None:
    self._grid = []
    self._width = width
    self._height = height
    self._populate()

  @property 
  def width(self) -> int:
    return self._width 

  @property
  def height(self) -> int:
    return self._height

  def _populate(self) -> None:
    """
    Builds a rectangular grid of cells in which all the walls are intially closed.
    """
    for y in range(self.height):
      row: list[MazeCell] = []
      for x in range(self.width):
        row.append(MazeCell(x,y))
      self._grid.append(row)

  def cell(self, location: Point) -> Optional[MazeCell]:
    """
    Finds a cell in the maze by its x,y coordinate.
    The origin of the 2D grid (0,0) is the upper left corner.

    Returns:
      Returns an instance of a MazeCell if it exists, otherwise None.
    """
    found: Optional[MazeCell]
    if (location.x < 0 or location.x >= self.width) or (location.y < 0 or location.y >= self.height):
      found = None
    else:  
      found = self._grid[location.y][location.x]
    return found 

  def find_neighbors(self, cell: MazeCell) -> Dict[Direction, MazeCell]:
    """
    Finds a given cell's neighbors.
    """
    cell_loc = cell.location
    north = Point(cell_loc.x, cell_loc.y - 1)
    east = Point(cell_loc.x + 1, cell_loc.y)
    south = Point(cell_loc.x, cell_loc.y + 1)
    west = Point(cell_loc.x - 1, cell_loc.y)

    # Note: For cells on the border, some neighbors will return None.
    neighbors: dict[Direction, MazeCell] = {
      Direction.NORTH : self.cell(north), 
      Direction.EAST : self.cell(east), 
      Direction.SOUTH : self.cell(south), 
      Direction.WEST : self.cell(west)
    }
    return neighbors