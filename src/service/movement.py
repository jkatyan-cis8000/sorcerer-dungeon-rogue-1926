"""Movement service for Tower of the Sorcerer."""

from src.types.types import Map, Player, Position, Tile


class MovementService:
    """Handles player movement on the game map."""

    def can_move(self, map: Map, position: Position) -> bool:
        """Check if player can move to position.

        Args:
            map: The game map
            position: The position to move to

        Returns:
            True if position is a FLOOR tile, False otherwise
        """
        if position.x < 0 or position.x >= map.width:
            return False
        if position.y < 0 or position.y >= map.height:
            return False
        return map.tiles[position.x][position.y] == Tile.FLOOR

    def move_player(self, map: Map, player: Player, direction: str) -> Player:
        """Move player in the given direction.

        Args:
            map: The game map
            player: The player entity
            direction: Movement direction (W/A/S/D or arrow keys)

        Returns:
            Updated player with new position if move successful
        """
        directions = {
            "w": (0, -1),
            "a": (-1, 0),
            "s": (0, 1),
            "d": (1, 0),
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }

        if direction not in directions:
            return player

        dx, dy = directions[direction]
        new_pos = Position(player.position.x + dx, player.position.y + dy)

        if self.can_move(map, new_pos):
            return Player(
                position=new_pos,
                hp=player.hp,
                max_hp=player.max_hp,
                gold=player.gold,
            )

        return player
