from dataclasses import dataclass


@dataclass
class Point:
    """
        Simple abstract class for representing a point (x; y) in a 2D space
    """
    x: float
    y: float

    def __repr__(self):
        return f"({self.x}; {self.y})"
