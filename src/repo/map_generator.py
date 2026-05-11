"""Map generator for Tower of the Sorcerer."""

from src.providers.rng import RandomProvider
from src.types.types import Map, Position, Tile, Entity
from src.config.constants import GRID_WIDTH, GRID_HEIGHT
from src.config.symbols import SYMBOL_MAP


class MapGenerator:
    """Generates game maps with guaranteed connectivity."""

    def __init__(self, rng: RandomProvider) -> None:
        """Initialize with RNG provider."""
        self._rng = rng

    def generate_map(self, width: int, height: int) -> Map:
        """Generate a map with guaranteed path from start to door."""
        tiles = [[Tile.WALL for _ in range(height)] for _ in range(width)]
        entities: dict[Position, Entity] = {}

        self._generate_maze(tiles, width, height)
        start_pos = Position(1, 1)
        door_pos = Position(width - 2, height - 2)

        tiles[start_pos.x][start_pos.y] = Tile.START
        tiles[door_pos.x][door_pos.y] = Tile.DOOR

        self._place_entities(tiles, width, height, start_pos, door_pos, entities)

        return Map(width=width, height=height, tiles=tiles, entities=entities)

    def _generate_maze(self, tiles: list, width: int, height: int) -> None:
        """Generate maze using randomized depth-first search."""
        for x in range(width):
            for y in range(height):
                tiles[x][y] = Tile.WALL

        stack = []
        start = Position(1, 1)
        tiles[start.x][start.y] = Tile.FLOOR
        stack.append(start)

        while stack:
            current = stack[-1]
            neighbors = self._get_unvisited_neighbors(tiles, current, width, height)

            if neighbors:
                next_pos = self._rng.choice(neighbors)
                wall_x = (current.x + next_pos.x) // 2
                wall_y = (current.y + next_pos.y) // 2
                tiles[wall_x][wall_y] = Tile.FLOOR
                tiles[next_pos.x][next_pos.y] = Tile.FLOOR
                stack.append(next_pos)
            else:
                stack.pop()

    def _get_unvisited_neighbors(self, tiles: list, pos: Position, width: int, height: int) -> list:
        """Get unvisited neighbors at distance 2."""
        neighbors = []
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]

        for dx, dy in directions:
            nx, ny = pos.x + dx, pos.y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and tiles[nx][ny] == Tile.WALL:
                neighbors.append(Position(nx, ny))

        return neighbors

    def _place_entities(
        self, tiles: list, width: int, height: int, start_pos: Position, door_pos: Position, entities: dict
    ) -> None:
        """Place random monsters and chests."""
        floor_positions = [
            Position(x, y)
            for x in range(1, width - 1)
            for y in range(1, height - 1)
            if tiles[x][y] == Tile.FLOOR
            and Position(x, y) != start_pos
            and Position(x, y) != door_pos
        ]

        floor_positions = self._rng.shuffle(floor_positions)

        for i, pos in enumerate(floor_positions[:5]):
            from src.types.types import Monster

            entities[pos] = Monster(
                position=pos,
                hp=self._rng.random_int(30, 50),
                damage=self._rng.random_int(15, 25),
            )

        for i, pos in enumerate(floor_positions[5:10]):
            from src.types.types import Chest

            entities[pos] = Chest(
                position=pos,
                gold=self._rng.random_int(10, 50),
            )
