from collections.abc import Callable
from generation.direction import Direction
from generation.structures import Point
from generation.maze import Maze

class Agent:
  """A generic, autonomous agent."""
  _location: Point # The maze coordinate of where the agent currently is.
  _last_location: Point # The last place the agent remembers it was.
  _facing: Direction # The direction the agent is facing.
  _crest: str # The color to represent the agent.

  def __init__(self, crest='blue') -> None:
    """Create a new instance of an agent."""
    self._crest = crest
    self._location = Point(0,0)
    self._last_location = Point(0,0)

  def face(self, direction: Direction) -> None:
    """Set the direction the agent is facing."""
    self._facing = direction

  @property
  def crest(self) -> str:
    return self._crest

  @property
  def facing(self) -> Direction:
    return self._facing

  def move_to(self, new_location: Point):
    """Tell the agent to walk to the new location in the maze."""
    self._last_location = self.location
    self._location = new_location

  @property
  def location(self) -> Point:
    return self._location

  @property
  def last_location(self) -> Point:
    return self._last_location

  def maze_strategy(self, strategy: Callable[..., None]) -> None:
    """Assign a maze traversal algorithm to the agent."""
    self._maze_strategy = strategy

  def explore(self, maze: Maze) -> None:
    """Perform one step of the assigned maze traversal strategy."""
    self._maze_strategy(self, maze)
