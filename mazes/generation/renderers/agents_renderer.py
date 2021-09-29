from typing import List
from ipycanvas import Canvas, hold_canvas

from generation.npc import Agent
from generation.structures import Corner, Point
from generation.renderers.units import AGENT_SIZE, ROOM_SIZE_WIDTH, ROOM_SIZE_HEIGHT

def draw_agents(agents: List[Agent], canvas: Canvas) -> Canvas:

  horizontal_offset = ROOM_SIZE_WIDTH/2
  vertical_offset = ROOM_SIZE_HEIGHT/2
  agent_offset = AGENT_SIZE/2

  with hold_canvas(canvas):
    for agent in agents:
      # Find the Upper Left Corner of the Room
      upper_left_corner = Corner(agent.location.x*ROOM_SIZE_WIDTH, agent.location.y*ROOM_SIZE_HEIGHT)

      # Find the middle of the room
      midpoint = Point(upper_left_corner.x + horizontal_offset, upper_left_corner.y + vertical_offset)

      # Find the upper left corner of the agent
      agent_point = Point(midpoint.x - agent_offset, midpoint.y - agent_offset)

      # Draw the agent
      canvas.fill_style = 'red'
      canvas.fill_rect(agent_point.x, agent_point.y, AGENT_SIZE, AGENT_SIZE)