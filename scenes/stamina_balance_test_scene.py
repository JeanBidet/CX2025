"""
Scène de test pour le système d'endurance et d'équilibre.

Démontre l'utilisation des composants StaminaComponent et BalanceComponent
avec affichage des jauges et indicateurs contextuels.
"""

from typing import Optional
import pygame
from scenes.scene import Scene
from entities.cyclist_with_states import CyclistWithStates
from components.transform_component import TransformComponent
from components.physics_component import PhysicsComponent
from components.command_input_component import CommandInputComponent
from components.state_machine_component import StateMachineComponent
from components.stamina_component import StaminaComponent
from components.balance_component import BalanceComponent
from systems.cyclist_state import StateType
from systems.terrain_manager import TerrainManager
from systems.terrain_data import TerrainType, TerrainData
from patterns.factories.terrain_factory import TerrainFactory
from ui.stamina_balance_ui import StaminaBalanceUI
from utils.vector2 import Vector2
from config.game_config import GameConfig
from config.constants import Colors


class StaminaBalanceTestScene(Scene):
    """
    Scène de test pour valider le système d'endurance et d'équilibre.

    Démontre :
    - Drain dynamique de l'endurance selon le contexte
    - Zones de performance et modificateurs de vitesse
    - Système d'équilibre et détection de chute
    - Récupération en mode portage
    - Interface utilisateur avec jauges et indicateurs
    - Interaction avec différents types de terrain
    """

    def __init__(self) -> None:
        """Initialise la scène de test."""
        super().__init__("StaminaBalanceTestScene")
        self._player: Optional[CyclistWithStates] = None
        self._font: Optional[pygame.font.Font] = None
        self._font_small: Optional[pygame.font.Font] = None
        self._ui: Optional[StaminaBalanceUI] = None

        # Terrain de test
        self._current_terrain_index = 0
        self._test_terrains = [
            TerrainType.ASPHALT,
            TerrainType.GRASS,
            TerrainType.SAND,
            TerrainType.MUD,
            TerrainType.GRAVEL,
            TerrainType.DIRT,
        ]

    def enter(self, data: Optional[dict] = None) -> None:
        """
        Initialise la scène lors de son activation.

        Args:
            data: Données optionnelles
        """
        print("[StaminaBalanceTestScene] Entrée dans la scène de test Stamina/Balance")

        # Initialise les polices
        self._font = pygame.font.Font(None, 48)
        self._font_small = pygame.font.Font(None, 20)

        # Initialise l'UI
        self._ui = StaminaBalanceUI()

        # Crée le cycliste au centre
        center_pos = Vector2(
            GameConfig.WINDOW_WIDTH / 2,
            GameConfig.WINDOW_HEIGHT / 2
        )

        self._player = CyclistWithStates(
            name="StaminaTestPlayer",
            position=center_pos,
            is_player=True
        )
        self._player.add_tag("player")

        # Ajoute le joueur à l'Entity Manager
        self._entity_manager.add_entity(self._player)

        # Configure le terrain de test
        self._setup_test_terrain()

        print(f"[StaminaBalanceTestScene] Joueur créé: {self._player}")
        print("[StaminaBalanceTestScene] Contrôles:")
        print("  - Flèches: Déplacement")
        print("  - C: Porter/Remonter sur le vélo")
        print("  - T: Changer de type de terrain")
        print("  - S: Modifier la pente (+10°)")
        print("  - D: Modifier la pente (-10°)")
        print("  - B: Appliquer déséquilibre (test)")
        print("  - F: Drainer endurance (test)")
        print("  - R: Reset endurance et équilibre")
        print("  - ESC: Retour au menu")

    def _setup_test_terrain(self) -> None:
        """Configure le terrain de test."""
        terrain_manager = TerrainManager.get_instance()
        if terrain_manager is None:
            print("[StaminaBalanceTestScene] AVERTISSEMENT: TerrainManager non disponible")
            return

        # Crée une grille de terrain simple (5x5)
        grid_size = 5
        terrain_type = self._test_terrains[self._current_terrain_index]

        # Crée la grille avec le terrain actuel
        terrain_grid = []
        for row in range(grid_size):
            terrain_row = []
            for col in range(grid_size):
                # Varie légèrement la pente et le camber pour tester
                slope = (row - grid_size // 2) * 5.0  # -10 à +10 degrés
                camber = (col - grid_size // 2) * 3.0  # -6 à +6 degrés

                terrain_data = TerrainFactory.create_terrain(
                    terrain_type=terrain_type,
                    slope=slope,
                    camber=camber
                )
                terrain_row.append(terrain_data)
            terrain_grid.append(terrain_row)

        # Configure le terrain manager
        tile_size = 200  # Taille des tuiles en pixels
        terrain_manager.set_terrain_from_grid(terrain_grid, tile_size)

        print(f"[StaminaBalanceTestScene] Terrain configuré: {terrain_type.name}")

    def exit(self) -> None:
        """Nettoie la scène lors de sa désactivation."""
        print("[StaminaBalanceTestScene] Sortie de la scène")
        self._entity_manager.clear()
        self._player = None
        self._ui = None

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Gère les événements de la scène.

        Args:
            events: Liste des événements Pygame
        """
        if not self._player:
            return

        # Transmet les événements au CommandInputComponent
        input_comp = self._player.get_component(CommandInputComponent)
        if input_comp:
            input_comp.set_events(events)

        # Transmet aussi à la State Machine
        state_machine = self._player.get_component(StateMachineComponent)
        if state_machine:
            state_machine.handle_events(events)

        # Gère les événements de test
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Changer de terrain
                if event.key == pygame.K_t:
                    self._current_terrain_index = (self._current_terrain_index + 1) % len(self._test_terrains)
                    self._setup_test_terrain()

                # Modifier la pente
                elif event.key == pygame.K_s:
                    self._modify_terrain_slope(10.0)
                elif event.key == pygame.K_d:
                    self._modify_terrain_slope(-10.0)

                # Tests de déséquilibre
                elif event.key == pygame.K_b:
                    balance = self._player.get_component(BalanceComponent)
                    if balance:
                        balance.apply_imbalance(30.0, "test_manual")
                        print("[Test] Déséquilibre appliqué: -30 balance")

                # Test de drain d'endurance
                elif event.key == pygame.K_f:
                    stamina = self._player.get_component(StaminaComponent)
                    if stamina:
                        stamina.drain(20.0)
                        print("[Test] Endurance drainée: -20 stamina")

                # Reset stamina et balance
                elif event.key == pygame.K_r:
                    stamina = self._player.get_component(StaminaComponent)
                    balance = self._player.get_component(BalanceComponent)
                    if stamina:
                        stamina.current_stamina = stamina.max_stamina
                        stamina.fatigue_level = 0.0
                        print("[Test] Endurance et fatigue réinitialisées")
                    if balance:
                        balance.reset_balance()
                        print("[Test] Équilibre réinitialisé")

    def _modify_terrain_slope(self, delta_slope: float) -> None:
        """
        Modifie la pente du terrain actuel.

        Args:
            delta_slope: Changement de pente en degrés
        """
        terrain_manager = TerrainManager.get_instance()
        if terrain_manager is None or self._player is None:
            return

        transform = self._player.get_component(TransformComponent)
        if transform is None:
            return

        # Récupère le terrain actuel
        terrain_tile = terrain_manager.get_terrain_at_position(transform.position)
        if terrain_tile and terrain_tile.data:
            # Crée un nouveau terrain avec la nouvelle pente
            old_data = terrain_tile.data
            new_slope = max(-45.0, min(45.0, old_data.slope + delta_slope))

            new_terrain = TerrainFactory.create_terrain(
                terrain_type=old_data.terrain_type,
                slope=new_slope,
                camber=old_data.camber
            )

            # Met à jour le terrain (simplifié - normalement on modifierait la grille)
            terrain_tile.data = new_terrain
            print(f"[Test] Pente modifiée: {new_slope:.1f}°")

    def update(self, delta_time: float) -> None:
        """
        Met à jour la scène.

        Args:
            delta_time: Temps écoulé depuis la dernière frame
        """
        # Update les entités via l'Entity Manager
        self._entity_manager.update(delta_time)

        # Met à jour l'UI avec les composants du joueur
        if self._player and self._ui:
            stamina = self._player.get_component(StaminaComponent)
            balance = self._player.get_component(BalanceComponent)
            self._ui.update(stamina, balance)

    def render(self, screen: pygame.Surface) -> None:
        """
        Affiche la scène.

        Args:
            screen: Surface Pygame où dessiner
        """
        # Fond
        screen.fill(Colors.GRASS_GREEN)

        # Affiche le terrain
        terrain_manager = TerrainManager.get_instance()
        if terrain_manager:
            terrain_manager.render(screen, Vector2.zero())

        # Affiche les entités
        self._entity_manager.render(screen)

        # Affiche l'UI des jauges
        if self._ui and self._player:
            transform = self._player.get_component(TransformComponent)
            current_terrain = None

            if transform:
                terrain_tile = terrain_manager.get_terrain_at_position(transform.position) if terrain_manager else None
                current_terrain = terrain_tile.data if terrain_tile else None

            self._ui.render(screen, current_terrain, show_context_info=True)

        # Affiche les informations de debug
        self._render_debug_info(screen)

    def _render_debug_info(self, screen: pygame.Surface) -> None:
        """
        Affiche les informations de debug.

        Args:
            screen: Surface Pygame où dessiner
        """
        if not self._player or not self._font_small:
            return

        # Récupère les composants
        stamina = self._player.get_component(StaminaComponent)
        balance = self._player.get_component(BalanceComponent)
        physics = self._player.get_component(PhysicsComponent)
        state_machine = self._player.get_component(StateMachineComponent)

        y_offset = GameConfig.WINDOW_HEIGHT - 180

        # État actuel
        if state_machine:
            state_text = f"État: {self._player.get_current_state_name()}"
            state_surface = self._font_small.render(state_text, True, Colors.WHITE)
            screen.blit(state_surface, (20, y_offset))
            y_offset += 25

        # Vitesse actuelle
        if physics:
            speed = physics.get_speed()
            max_speed = physics.max_speed
            speed_text = f"Vitesse: {speed:.1f} / {max_speed:.1f} px/s"
            speed_surface = self._font_small.render(speed_text, True, Colors.WHITE)
            screen.blit(speed_surface, (20, y_offset))
            y_offset += 25

        # Zone de performance
        if stamina:
            zone = stamina.get_performance_zone()
            multiplier = stamina.get_speed_multiplier()
            zone_text = f"Zone: {zone.name} (x{multiplier:.2f})"
            zone_color = self._get_zone_color(zone)
            zone_surface = self._font_small.render(zone_text, True, zone_color)
            screen.blit(zone_surface, (20, y_offset))
            y_offset += 25

        # Niveau de stabilité
        if balance:
            stability = balance.get_stability_level()
            source = balance.get_last_imbalance_source()
            stability_text = f"Stabilité: {stability}"
            if source:
                stability_text += f" (source: {source})"

            stability_color = Colors.GREEN if stability == "STABLE" else Colors.YELLOW if stability == "UNSTABLE" else Colors.RED
            stability_surface = self._font_small.render(stability_text, True, stability_color)
            screen.blit(stability_surface, (20, y_offset))
            y_offset += 25

        # Instructions simplifiées
        y_offset += 10
        instructions = [
            "T: Changer terrain | C: Porter vélo",
            "S/D: Pente +/- | B: Déséquilibre",
            "F: Drain stamina | R: Reset"
        ]
        for instruction in instructions:
            inst_surface = self._font_small.render(instruction, True, Colors.LIGHT_GRAY)
            screen.blit(inst_surface, (20, y_offset))
            y_offset += 20

    def _get_zone_color(self, zone) -> tuple:
        """
        Retourne la couleur associée à une zone de performance.

        Args:
            zone: Zone de performance

        Returns:
            Couleur RGB
        """
        from config.constants import PerformanceZone

        zone_colors = {
            PerformanceZone.OPTIMAL: Colors.GREEN,
            PerformanceZone.MODERATE: Colors.YELLOW,
            PerformanceZone.CRITICAL: (255, 165, 0),  # Orange
            PerformanceZone.EXHAUSTED: Colors.RED,
        }
        return zone_colors.get(zone, Colors.WHITE)
