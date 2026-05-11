"""Type definitions for Tower of the Sorcerer."""

from enum import Enum
from typing import Dict, List, NamedTuple


class Position(NamedTuple):
    """A position in the game map."""

    x: int
    y: int


class Tile(Enum):
    """Type of tile in the game map."""

    WALL = "wall"
    FLOOR = "floor"
    DOOR = "door"
    START = "start"


class Player:
    """Player entity."""

    def __init__(self, position: Position, hp: int, max_hp: int, gold: int) -> None:
        self.position = position
        self.hp = hp
        self.max_hp = max_hp
        self.gold = gold


class Monster:
    """Monster entity."""

    def __init__(self, position: Position, hp: int, damage: int) -> None:
        self.position = position
        self.hp = hp
        self.damage = damage


class Chest:
    """Chest entity."""

    def __init__(self, position: Position, gold: int) -> None:
        self.position = position
        self.gold = gold


Entity = Player | Monster | Chest


class Map:
    """Game map."""

    def __init__(
        self, width: int, height: int, tiles: List[List["Tile"]], entities: Dict[Position, Entity]
    ) -> None:
        self.width = width
        self.height = height
        self.tiles = tiles
        self.entities = entities


class GameStatus(Enum):
    """Current game state."""

    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


class GameState:
    """Complete game state."""

    def __init__(
        self,
        player: Player,
        map: Map,
        monsters: List[Monster],
        status: GameStatus = GameStatus.PLAYING,
    ) -> None:
        self.player = player
        self.map = map
        self.monsters = monsters
        self.status = status
