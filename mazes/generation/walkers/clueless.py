from typing import List

from generation.direction import Direction, DIR_ORIENTATION, Orientation
from generation.maze import Maze
from generation.npc import Agent
from generation.structures import Point

def find_next_direction(agent: Agent, possible_directions: list[Direction]) -> Direction:
  """The agent is facing a direction. I think it should continue in the same direction
  if possible. If not it should try right, then left. Finally, backtrack."""
  current_orientation: dict[Orientation, Direction] = DIR_ORIENTATION[agent.facing]
  if agent.facing in possible_directions:
    next_direction = agent.facing
  elif current_orientation[Orientation.RIGHT] in possible_directions: # Is there a door to the right?
    next_direction = current_orientation[Orientation.RIGHT]
  elif current_orientation[Orientation.LEFT]  in possible_directions: # Is there a door to the left?
    next_direction = current_orientation[Orientation.LEFT]
  elif current_orientation[Orientation.BEHIND] in possible_directions: # Go back the way we came?
    next_direction = current_orientation[Orientation.BEHIND]
  else:
    raise Exception("We\'re walled in! No possible doors found.")
  return next_direction

def clueless_walk(agent: Agent, maze: Maze) -> None:
  """
  Given an agent, have them randomly choose a room to go to next, then move.
  """
  # 1. Get the current room the agent is in.
  current_room = maze.cell(agent.location)

  #  If the agent is at the entrance or exit of the maze, then stop.
  if current_room is maze.starting_cell or current_room is maze.exit_cell:
    return;

  # 2. Find all the walls that have doors in that room.
  possible_directions: List[Direction] = current_room.open_sides()

  # 3. Find the next direction to go.
  next_direction = find_next_direction(agent, possible_directions)

  # 4. Find the location of the room the open door connects to.
  next_location: Point = maze.find_adjacent_neighbor(next_direction, agent.location)

  # 5. Move the agent to the next room.
  agent.face(next_direction)
  agent.move_to(next_location)