from typing import List
from ipycanvas import Canvas, hold_canvas
from traitlets.traitlets import Int

from generation.npc import Agent
from generation.structures import Corner, Point
from generation.renderers.units import AGENT_SIZE, ROOM_SIZE_WIDTH, ROOM_SIZE_HEIGHT

def build_agent_rect(location: Point, horizontal_offset: int, vertical_offset: int, agent_offset: int) -> Corner:
  upper_left_corner = Corner(location.x * ROOM_SIZE_WIDTH, location.y * ROOM_SIZE_HEIGHT)

  # Find the middle of the room
  midpoint = Point(upper_left_corner.x + horizontal_offset, upper_left_corner.y + vertical_offset)

  # Find the upper left corner of the agent
  return Corner(midpoint.x - agent_offset, midpoint.y - agent_offset)

def draw_agents(agents: List[Agent], canvas: Canvas) -> Canvas:

  horizontal_offset = ROOM_SIZE_WIDTH/2
  vertical_offset = ROOM_SIZE_HEIGHT/2
  agent_offset = AGENT_SIZE/2

  with hold_canvas(canvas):
    # clear where agents have been.
    canvas.clear()
    # canvas.fill_style = 'white'
    # for agent in agents:
    #   agent_upper_left: Corner = build_agent_rect(agent.last_location, horizontal_offset, vertical_offset, agent_offset)
    #   canvas.fill_rect(agent_upper_left.x, agent_upper_left.y, AGENT_SIZE, AGENT_SIZE)

    # draw where the agents are now.
    for agent in agents:
      agent_upper_left: Corner = build_agent_rect(agent.location, horizontal_offset, vertical_offset, agent_offset)

      # Draw the agent
      canvas.fill_style = agent.crest
      canvas.fill_rect(agent_upper_left.x, agent_upper_left.y, AGENT_SIZE, AGENT_SIZE)