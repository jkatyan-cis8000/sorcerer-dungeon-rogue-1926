"""Interaction service for Tower of the Sorcerer."""

import random

from src.types.types import Player, Chest, Map


class InteractionService:
    """Handles player interactions with game entities."""

    def handle_chest(self, player: Player, chest: Chest) -> Player:
        """Handle interaction with a chest.

        Heals player by random 20-30 HP (capped at MAX_HP).

        Args:
            player: The player entity
            chest: The chest entity

        Returns:
            Updated player with healed HP
        """
        heal_amount = random.randint(20, 30)
        player.hp = min(player.hp + heal_amount, player.max_hp)
        return player

    def handle_door(self, map: Map, player: Player) -> bool:
        """Handle interaction with a door.

        Args:
            map: The game map
            player: The player entity

        Returns:
            True if player is on a door tile (level complete)
        """
        return map.tiles[player.position.x][player.position.y] == Tile.DOOR
