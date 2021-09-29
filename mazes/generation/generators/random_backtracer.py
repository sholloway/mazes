import random
from typing import List, Dict

from generation.stack import Stack
from generation.structures import Point
from generation.direction import Direction, DIR_OPPOSITES
from generation.maze import Maze, MazeCell

"""
1. Choose the initial cell, mark it as visited and push it to the stack.
2. While the stack is not empty:
  1. Pop a cell from the stack and make it a current cell.
  2. If the current cell has any neighbors which have not been visited:
    1. Push the current cell to the stack.
    2. Choose one of the unvisited neighbors at random.
    3. Remove the wall between the current cell and the chosen cell.
    4. Push the current cell back on the stack (back tracking)
    5. Mark the chosen cell as visited and push it to the stack. (Continue exploring with)
"""
def generate_maze_walls(maze: Maze) -> Maze:
  """
  Traverses the grid of cells creates a maze by opening walls in place.

  Returns:
    The modified grid.
  """
  stack = Stack()
  
  # Establish Starting Cell
  starting_cell_loc: Point = Point(random.randint(0, maze.width - 1), 0) # Randomly select a cell in the north most row.
  starting_cell = maze.cell(starting_cell_loc)
  starting_cell.remove_wall(Direction.NORTH) # Create an opening in the maze
  maze.starting_cell = starting_cell #Saving a pointer for visualization and and solving.

  # Establish Target Cell. This is the exit of the maze.
  exit_cell_loc: Point = Point(random.randint(0, maze.width - 1), maze.height-1) # Randomly select a cell in the South most row.
  exit_cell = maze.cell(exit_cell_loc)
  exit_cell.remove_wall(Direction.SOUTH) # Create an opening in the maze for the exit.
  maze.exit_cell = exit_cell #Saving a pointer for visualization and and solving.
  print(f"Exit cell: {exit_cell_loc}")

  starting_cell.visit() 
  stack.push(starting_cell)

  while not stack.empty():
    current_cell = stack.pop()
    neighbors: Dict[Direction, MazeCell]  = maze.find_neighbors(current_cell)

    # Filter out None and visited neighbors.
    unvisited_neighbors = dict(filter(lambda n : n[1] is not None and not n[1].visited, neighbors.items()))
    if len(unvisited_neighbors) > 0: 
      # Attempt 1: Grab the first non-visited MazeCell if there are any. Seems like this just goes North or South.
      # unvisited_neighbor = list(unvisited_neighbors.items())[0] # Type: List[(direction, MazeCell)]
      
      # Attempt 2. Randomize which unvisited neighbor is traversed next.
      pick_cell = random.randint(0, len(unvisited_neighbors) - 1)
      unvisited_neighbor: List[(Direction, MazeCell)] = list(unvisited_neighbors.items())[pick_cell]

      # Remove the wall between the current cell and the chosen cell.
      wall_to_remove = unvisited_neighbor[0]
      unvisited_cell = unvisited_neighbor[1]
      current_cell.remove_wall(wall_to_remove)
      unvisited_cell.remove_wall(DIR_OPPOSITES[wall_to_remove])
      unvisited_cell.visit()
      
      # Save the current cell for further exploration (backtracking...)
      stack.push(current_cell)
      
      # Save the unvisited neighbor for further exploration.
      stack.push(unvisited_cell)