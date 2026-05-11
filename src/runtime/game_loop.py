"""Game loop runtime module for Tower of the Sorcerer."""

from typing import List

from src.types.types import GameState, GameStatus, Player, Monster, Chest, Tile
from src.config.constants import PLAYER_START_HP, PLAYER_MAX_HP
from src.service.combat import CombatService
from src.service.movement import MovementService
from src.service.interaction import InteractionService
from src.ui.renderer import Renderer
from src.ui.ui_display import UIDisplay


class GameLoop:
    """Main game loop handling input, updates, and rendering."""

    def __init__(self) -> None:
        """Initialize the game loop with services."""
        self._combat_service = CombatService()
        self._movement_service = MovementService()
        self._interaction_service = InteractionService()
        self._renderer = Renderer()
        self._ui_display = UIDisplay()

    def run(self, game_state: GameState) -> None:
        """Run the main game loop.

        Args:
            game_state: The initial game state
        """
        player = game_state.player
        monsters = game_state.monsters.copy()
        map_obj = game_state.map

        while game_state.status == GameStatus.PLAYING:
            self._render_frame(map_obj, player, monsters)

            if game_state.status != GameStatus.PLAYING:
                break

            self._handle_input(map_obj, player, monsters)

            if player.hp <= 0:
                game_state.status = GameStatus.LOST
            elif self._interaction_service.handle_door(map_obj, player):
                game_state.status = GameStatus.WON

        self._render_frame(map_obj, player, monsters)

        if game_state.status == GameStatus.WON:
            print("You win! You've escaped the tower.")
        elif game_state.status == GameStatus.LOST:
            print("You lose! The tower claims another soul.")

    def _render_frame(self, map_obj: Map, player: Player, monsters: List[Monster]) -> None:
        """Render a single frame of the game.

        Args:
            map_obj: The game map
            player: The player entity
            monsters: List of monster entities
        """
        render = self._renderer.render(map_obj, player, monsters)
        stats = self._ui_display.display_stats(player, monsters)

        full_output = f"{render}\n\n{stats}"
        print(full_output)

    def _handle_input(self, map_obj: Map, player: Player, monsters: List[Monster]) -> None:
        """Handle player input for movement.

        Args:
            map_obj: The game map
            player: The player entity
            monsters: List of monster entities
        """
        try:
            move = input("Enter move (W/A/S/D): ").strip().lower()
        except EOFError:
            return

        if move not in ("w", "a", "s", "d"):
            return

        old_pos = player.position
        player = self._movement_service.move_player(map_obj, player, move)

        if old_pos != player.position:
            for monster in monsters:
                if monster.position == player.position:
                    player = self._combat_service.resolve_combat(player, monster)
                    if monster.hp <= 0:
                        monsters.remove(monster)
                    break

            entity = map_obj.entities.get(player.position)
            if isinstance(entity, Chest):
                player = self._interaction_service.handle_chest(player, entity)
                del map_obj.entities[player.position]
