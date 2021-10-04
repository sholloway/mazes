from generation.direction import Direction
from generation.structures import Point

class Agent:
  _location: Point
  _last_location: Point 
  _facing: Direction
  crest: str # The color to render the agent

  def __init__(self, crest='blue') -> None:
    self.crest = crest
    self._location = Point(0,0)
    self._last_location = Point(0,0)

  def face(self, direction: Direction) -> None:
    self._facing = direction

  @property
  def facing(self) -> Direction:
    return self._facing

  def move_to(self, new_location: Point):
    self._last_location = self.location
    self._location = new_location

  @property
  def location(self) -> Point:
    return self._location

  @property
  def last_location(self) -> Point:
    return self._last_location

  """
  TODO: Make the agent remember the last place it's been. 
  Want to record the last rectangle, so we can rapidly draw over it. 
  Also consider tracking the direction it came so we can avoid back tracing. 
  """