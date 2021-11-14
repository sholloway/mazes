from __future__ import annotations

from heapq import heappop, heappush
from typing import Dict, List, Set, Tuple, Union
import itertools

from generation.structures import Point
from generation.maze import Maze, MazeCell
from generation.npc import Agent
from generation.direction import Direction

class Waypoint:
  """A decorator class that wraps a Point to enable chaining points."""
  def __init__(self, point: Point, predecessor: Waypoint = None):
    self._point = point
    self._predecessor = predecessor
    self._cost_from_start = 0
    self._cost_to_target = 0

  @property
  def point(self) -> Point:
    return self._point

  @property
  def predecessor(self) -> Point:
    return self._predecessor
  
  @predecessor.setter
  def predecessor(self, predecessor: Point) -> None:
    self._predecessor = predecessor

  @property 
  def cost_from_start(self) -> None:
    return self._cost_from_start
  
  @cost_from_start.setter 
  def cost_from_start(self, cost: float) -> None:
    self._cost_from_start = cost
  
  @property 
  def cost_to_target(self) -> None:
    return self._cost_to_target
  
  @cost_to_target.setter 
  def cost_to_target(self, cost: float) -> None:
    self._cost_to_target = cost
    
  def total_cost(self) -> float:
    return self.cost_from_start + self.cost_to_target

  def __str__(self):
    pred_str = f'({self._predecessor.x}, {self._predecessor.y})' if self._predecessor else 'None'
    return f'Waypoint (x = {self.point.x}, y = {self.point.y}) with predecessor {pred_str}'

  def __repr__(self) -> str:
    return self.__str__()

  def __eq__(self, other: object) -> bool:
    """For equality checks, only consider the decorated point, not the predecessor."""
    if (isinstance(other, Waypoint)):
      return self.point.x == other.point.x and self.point.y == other.point.y
    return False

  def __hash__(self) -> int:
    return self.point.__hash__()

# A point stored in a heap.
# An entry is of the form (cost, count, Waypoint). 
# Not using tuples because the point can be replaced with REMOVED_POINT
PriorityPoint = List[Union[float, int, Waypoint, str]]

# A constant that represents a point that has been removed from the queue.
# I think this could lead to subtle bugs.
REMOVED_POINT = 'REMOVED'

class PriorityQueue:
  """A priority queue implemented with a min heap."""
  def __init__(self):
    self._items: List[PriorityPoint] = [] # A min heap.
    self._index: Dict[Point, PriorityPoint] = {} # An index of the points in the heap.
    self._counter = itertools.count() # A counter for tracking the sequence of points.

  def __str__(self) -> str:
    return self._items.__str__()

  def push(self, point: Waypoint, cost: float) -> PriorityQueue:
    """
    Add a point to the priority queue. Points are arranged in the queue 
    by their associated cost. The item with the smallest cost is listed first.
    If a point is already in the queue, it is removed first before adding it.

    Returns
    The instance of the priority queue.
    """

    if point in self._items:
      self.remove(point)

    count = next(self._counter)
    entry = [cost, count, point]
    self._index[point] = entry
    heappush(self._items, entry) 
    return self

  def pop(self) -> Tuple[float, Waypoint]:
    """
    Removes the point in the queue with the smallest cost.

    Returns
    A tuple of the cost and point.

    Throws
    Raises a KeyError if called on an empty queue.
    """

    # There could be removed points, so keep popping until a point is found.
    while len(self._items) > 0:
      cost,_ignore,point = heappop(self._items)
      if point is not REMOVED_POINT:
        return (cost, point)
    # If the queue is exhausted, then throw an exception.
    raise KeyError('Cannot pop from an empty priority queue.')

  def __contains__(self, point: Waypoint) -> bool:
    """
    Determines if a point is already in the queue.

    Example
    p in queue
    """
    return point in self._index

  def __len__(self) -> int:
    """
    Supports using the len() with the priority queue.
    
    Returns
    The length of the queue.
    """
    return len(self._items)

  def remove(self, point: Waypoint) -> PriorityQueue:
    """
    Removes a point from the queue if it exists. Does nothing if the point 
    doesn't exist in the queue.

    Returns
    The instance of the priority queue.
    """
    if point in self._index:
      entry = self._index.pop(point)
      entry[2] = REMOVED_POINT

def find_distance(a: Point, b: Point) -> float:
  """Finds the Manhattan distance between two locations."""
  return abs(a.x - b.x) + abs(a.y - b.y)

Path = List[Point]

def build_path(endpoint: Waypoint) -> Path:
  """
  Given a Waypoint, builds a path following the waypoint's parent pointers.
  Note: Will fail if there is a loop.

  Returns
  A path instance.
  """
  points : Path = []

  current = endpoint
  while current != None:
    points.append(current.point)
    current = current.predecessor

  points.reverse()
  return points

def find_path(agent: Agent, maze: Maze, target: Point) -> Tuple[bool,Union[None,Path]]:
  """
  Finds a path from the agents current location to the target cell.

  Returns
  A tuple of the form (success:bool, Path)
  """
  visited_locations: Set[Point] = set()
  possible_steps: PriorityQueue = PriorityQueue()

  starting_point = Waypoint(agent.location, None)
  starting_point.cost_from_start = 0
  starting_point.cost_to_target = find_distance(starting_point.point, target)
  possible_steps.push(starting_point, starting_point.total_cost())

  while len(possible_steps) > 0:
    _ignore_cost, current_location = possible_steps.pop() # pop returns Tuple[float, Waypoint]
    if current_location.point == target:
      return (True, build_path(current_location))
    else:
      visited_locations.add(current_location.point)
      current_cell: MazeCell = maze.cell(current_location.point)
      
      if(current_cell is None):
        print(f'The target is ({target.x},{target.y}). Current location is ({current_location.point.x},{current_location.point.y})')
        raise Exception(f'{current_location.point.x},{current_location.point.y} has no location.')

      open_directions: list[Direction] = current_cell.open_sides()
      for direction in open_directions:
        # Find the "room" in the open direction
        neighbor_location: Point = maze.find_adjacent_neighbor(direction, current_location.point)
        if maze.out_of_bounds(neighbor_location):
          continue
        
        neighbor = Waypoint(neighbor_location, current_location)

        # Ignore the connected room if that's where we just came from
        if (current_location.predecessor is not None) and (neighbor.point == current_location.predecessor.point) :
          continue

        cost_to_add_step_to_path = current_location.total_cost() + find_distance(current_location.point, neighbor.point)
        neighbor.cost_from_start = cost_to_add_step_to_path
        neighbor.cost_to_target = find_distance(neighbor.point, target)

        # We could have visited this room before from a different path. 
        # If that's the case, then remove it from the visited set or possible queue.
        if (neighbor.point in visited_locations) and (cost_to_add_step_to_path < find_distance(starting_point.point, neighbor.point)) :
          visited_locations.remove(neighbor.point)

        if (neighbor in possible_steps) and (cost_to_add_step_to_path < find_distance(starting_point.point, neighbor.point)):
          possible_steps.remove(neighbor) 
        
        if (neighbor not in possible_steps) and (neighbor.point not in visited_locations):
          possible_steps.push(neighbor, neighbor.total_cost())
  
  return (False, None)

def build_path_walker(path_to_walk: Path):
  """A closure that enables an agent to traverse a list of points."""
  path = path_to_walk
  current_step_index = -1

  def walk_path(agent: Agent, maze: Maze) -> None:
    nonlocal current_step_index, path

    if current_step_index < (len(path) - 1):
      current_step_index += 1
      agent.move_to(path[current_step_index])

  return walk_path