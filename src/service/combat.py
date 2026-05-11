"""Combat service for Tower of the Sorcerer."""

import random

from src.types.types import Player, Monster


class CombatService:
    """Handles combat between player and monsters."""

    def resolve_combat(self, player: Player, monster: Monster) -> Player:
        """Resolve combat between player and monster.

        Player attacks first, then monster counter-attacks.
        Player damage: random 15-25
        Monster damage: random 10-20

        Args:
            player: The player entity
            monster: The monster entity

        Returns:
            Updated player with HP adjusted
        """
        player_damage = random.randint(15, 25)
        monster.hp -= player_damage

        if monster.hp > 0:
            monster_damage = random.randint(10, 20)
            player.hp -= monster_damage

        return player
