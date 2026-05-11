"""Math utility functions for Tower of the Sorcerer."""

from src.types.types import Position


def manhattan_distance(pos1: Position, pos2: Position) -> int:
    """Calculate Manhattan distance between two positions."""
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)


def clamp(value: int, min_val: int, max_val: int) -> int:
    """Clamp a value between min and max."""
    return max(min_val, min(value, max_val))
