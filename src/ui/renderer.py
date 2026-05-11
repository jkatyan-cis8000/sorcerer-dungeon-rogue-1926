"""UI rendering module for Tower of the Sorcerer."""

from typing import List

from src.types.types import Map, Player, Monster, Chest, Tile
from src.config.symbols import SYMBOL_MAP
from src.config.constants import GRID_WIDTH, GRID_HEIGHT


class Renderer:
    """Renders the game state to a string grid."""

    def render(self, map: Map, player: Player, monsters: List[Monster]) -> str:
        """Render the game state to a string grid.

        Args:
            map: The game map
            player: The player entity
            monsters: List of monster entities

        Returns:
            String representation of the 80x80 grid
        """
        grid = [[" " for _ in range(map.height)] for _ in range(map.width)]

        for x in range(map.width):
            for y in range(map.height):
                tile = map.tiles[x][y]
                grid[x][y] = SYMBOL_MAP.get(tile.value, "#")

        for pos, entity in map.entities.items():
            if isinstance(entity, Chest):
                grid[pos.x][pos.y] = SYMBOL_MAP["chest"]
            elif isinstance(entity, Monster):
                grid[pos.x][pos.y] = SYMBOL_MAP["monster"]

        for monster in monsters:
            grid[monster.position.x][monster.position.y] = SYMBOL_MAP["monster"]

        grid[player.position.x][player.position.y] = SYMBOL_MAP["player"]

        output_lines = []
        for y in range(map.height):
            row = "".join(grid[x][y] for x in range(map.width))
            output_lines.append(row)

        return "\n".join(output_lines)
