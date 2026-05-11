"""Game constants for Tower of the Sorcerer."""

from src.types.types import Position

GRID_WIDTH = 80
GRID_HEIGHT = 80
PLAYER_START_HP = 100
PLAYER_MAX_HP = 100
MONSTER_DAMAGE_MIN = 15
MONSTER_DAMAGE_MAX = 25
MONSTER_HP_MIN = 30
MONSTER_HP_MAX = 50
CHEST_HEAL_MIN = 20
CHEST_HEAL_MAX = 30

TILE_SYMBOLS = {
    "WALL": "#",
    "FLOOR": ".",
    "DOOR": "D",
    "START": "S",
}
