# TODO: Restructure as a class or functions designed to be passed in.
from ipycanvas import Canvas, hold_canvas

from generation.maze import Maze, MazeCell
from generation.structures import Corner, Point
from generation.renderers.units import ROOM_SIZE_WIDTH, ROOM_SIZE_HEIGHT

def draw_wall(canvas: Canvas, start: Corner, stop: Corner) -> None:
  canvas.move_to(start.x, start.y)
  canvas.line_to(stop.x, stop.y)
  canvas.stroke()

def draw_cell_walls(cell: MazeCell, canvas: Canvas, room_size_width: int, room_size_height: int, color='black') -> None:
  canvas.begin_path()
  canvas.stroke_style = color

  cell_index,row_index =  cell.location.x, cell.location.y 
  upper_left_corner = Corner(cell_index*room_size_width, row_index*room_size_height)
  upper_right_corner = Corner(upper_left_corner.x + room_size_width, upper_left_corner.y)
  lower_right_corner = Corner(upper_right_corner.x, upper_right_corner.y + room_size_height)
  lower_left_corner = Corner(lower_right_corner.x - room_size_width, lower_right_corner.y)

  if cell.north: draw_wall(canvas, upper_left_corner, upper_right_corner)
  if cell.east: draw_wall(canvas, upper_right_corner, lower_right_corner)
  if cell.south: draw_wall(canvas, lower_right_corner, lower_left_corner)
  if cell.west: draw_wall(canvas, lower_left_corner, upper_left_corner)
  
  return

def draw_maze(maze: Maze, canvas: Canvas) -> Canvas:
  """Draws the maze in a single batch by visiting all rooms."""  
  with hold_canvas(canvas):
    canvas.line_width = 5
    for row_index in range(maze.height):
      for cell_index in range(maze.width):
        cell = maze.cell(Point(cell_index, row_index))
        draw_cell_walls(cell, canvas, ROOM_SIZE_WIDTH, ROOM_SIZE_HEIGHT)
    # Draw the first cell, for debugging
    draw_cell_walls(maze.starting_cell, canvas, ROOM_SIZE_WIDTH, ROOM_SIZE_HEIGHT, 'red')
  return canvas

def animate_drawing_by_rooms(maze, canvas):
  """
  Animates drawing a maze by visiting  each room. 
  1 Room per frame.

  This approach is very slow because it's sending a rendering call to the kernel 
  for each line. To speed it up, might be able to do a with_holding per room
  or per row. Either way, I don't like the scan line approach of drawing.
  """
  # Paint the background
  canvas.fill_style = 'white'
  canvas.fill_rect(0, 0, canvas.width,  canvas.height)

  # Visit each room, one room at a time.
  canvas.line_width = 5
  room_size_width: int =  20
  room_size_height: int = 20
  for row_index in range(maze.height):
      for cell_index in range(maze.width):
        cell = maze.cell(Point(cell_index, row_index))
        draw_cell_walls(cell, canvas, room_size_width, room_size_height)
  return canvas
