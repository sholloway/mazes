from typing import List

from generation.direction import Direction, DIR_ORIENTATION, Orientation
from generation.maze import Maze
from generation.npc import Agent
from generation.structures import Point

def wall_follower_walk(agent: Agent, maze: Maze) -> None:
  """
  Maze traversal algorithm. Assumes that all the walls are connected.
  The agent keeps a 'hand' on the left or right wall. This means that when 
  deciding on the next move (if right dominate):
  1. Go right if possible.
  2. Else go forward if possible.
  3. Else go left if possible.
  4. Else go back if possible.
  5. Else panic.
  """
  # 1. Get the current room the agent is in.
  current_room = maze.cell(agent.location)

  # If the agent is at the entrance or exit of the maze, then stop.
  if current_room is maze.starting_cell or current_room is maze.exit_cell:
    return;

  # 2. Find the agent's current orientation.
  current_orientation: dict[Orientation, Direction] = DIR_ORIENTATION[agent.facing]

  # 3. Find all the walls that have doors in that room.
  possible_directions: List[Direction] = current_room.open_sides()

  # 4. Use the wall follower strategy to pick the next room.
  if current_orientation[Orientation.RIGHT] in possible_directions: # Is there a door to the right?
    next_direction = current_orientation[Orientation.RIGHT]
  elif agent.facing in possible_directions:
    next_direction = agent.facing
  elif current_orientation[Orientation.LEFT]  in possible_directions: # Is there a door to the left?
    next_direction = current_orientation[Orientation.LEFT]
  elif current_orientation[Orientation.BEHIND] in possible_directions: # Go back the way we came?
    next_direction = current_orientation[Orientation.BEHIND]
  else:
    # This shouldn't be possible
    raise Exception("We\'re walled in! No possible doors found.")

  # 4. Find the location of the room the open door connects to.
  next_location: Point = maze.find_adjacent_neighbor(next_direction, agent.location)

  # 5. Move the agent to the next room.
  agent.face(next_direction)
  agent.move_to(next_location)