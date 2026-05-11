"""UI display module for Tower of the Sorcerer."""

from typing import List

from src.types.types import Player, Monster
from src.utils.string import format_stats_text


class UIDisplay:
    """Displays game statistics and UI elements."""

    def display_stats(self, player: Player, monsters: List[Monster]) -> str:
        """Display current game statistics.

        Args:
            player: The player entity
            monsters: List of monster entities

        Returns:
            Formatted string with stats
        """
        lines = [
            f"HP: {format_stats_text(str(player.hp), player.max_hp)}",
            f"Monsters: {len(monsters)}",
        ]

        return "\n".join(lines)
