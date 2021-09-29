from enum import Enum

class Direction(Enum):
  NORTH = 'NORTH'
  EAST = 'EAST'
  SOUTH = 'SOUTH'
  WEST = 'WEST'

DIR_OPPOSITES: dict[Direction, Direction] = {
  Direction.NORTH : Direction.SOUTH,
  Direction.SOUTH : Direction.NORTH,
  Direction.EAST : Direction.WEST,
  Direction.WEST : Direction.EAST
}