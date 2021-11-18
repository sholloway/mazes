from collections import deque
from typing import Optional
from generation.maze import MazeCell

class Stack:
  """
  A FILO Queue built with collections.deque (Double Linked List).
  """
  _data: deque
  def __init__(self) -> None:
    self._data = deque()

  def push(self, cell: MazeCell) -> None:
    """
    Adds a point to the top of the stack.
    """
    self._data.appendleft(cell)

  def pop(self) -> Optional[MazeCell]:
    """
    Returns and removes the last item added to the stack.
    If the stack is empty then the function returns None.
    Check with "if val is not None: ..."
    """
    return self._data.popleft() if len(self._data) > 0 else None

  def empty(self) -> bool:
    """
    Returns True if the stack is empty.
    """
    return len(self._data) == 0