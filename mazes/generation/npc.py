from generation.structures import Point

class Agent:
  location: Point
  crest: str # The color to render the agent

  def __init__(self, crest='blue') -> None:
    self.crest = crest