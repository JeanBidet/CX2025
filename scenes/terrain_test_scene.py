"""
Scène de test pour le système de terrain.

Démontre l'utilisation du Factory Pattern pour créer des terrains,
la gestion d'une grille de terrain, et l'intégration avec le système physique.
"""

from typing import Optional
import pygame
from scenes.scene import Scene
from entities.entity import Entity
from components.transform_component import TransformComponent
from components.physics_component import PhysicsComponent
from components.command_input_component import CommandInputComponent
from components.sprite_renderer_component import SpriteRendererComponent
from components.terrain_physics_component import TerrainPhysicsComponent
from systems.terrain_manager import TerrainManager
from systems.terrain_data import TerrainType
from utils.terrain_map_loader import TerrainMapLoader
from utils.vector2 import Vector2
from config.game_config import GameConfig
from config.constants import Colors


class TerrainTestScene(Scene):
    """
    Scène de test pour valider le système de terrain.

    Démontre :
    - Création de terrain avec TerrainFactory
    - Gestion de grille avec TerrainManager
    - Chargement de maps depuis JSON
    - Intégration physique avec TerrainPhysicsComponent
    - Affichage du terrain actuel dans le HUD
    """

    def __init__(self) -> None:
        """Initialise la scène de test du système de terrain."""
        super().__init__("TerrainTestScene")
        self._player: Optional[Entity] = None
        self._terrain_manager: Optional[TerrainManager] = None
        self._font: Optional[pygame.font.Font] = None
        self._font_small: Optional[pygame.font.Font] = None
        self._camera_offset: Vector2 = Vector2(0, 0)

    def enter(self, data: Optional[dict] = None) -> None:
        """
        Initialise la scène lors de son activation.

        Args:
            data: Données optionnelles de la scène précédente
        """
        print("[TerrainTestScene] Entrée dans la scène de test du terrain")

        # Initialise les polices
        self._font = pygame.font.Font(None, 36)
        self._font_small = pygame.font.Font(None, 24)

        # Crée le terrain de test (circuit de cyclo-cross)
        try:
            # Essaie de charger depuis JSON
            self._terrain_manager = TerrainMapLoader.load_from_file(
                "maps/cyclocross_circuit.json"
            )
            print("[TerrainTestScene] Map chargée depuis cyclocross_circuit.json")
        except FileNotFoundError:
            # Fallback : crée une map de test procédurale
            print("[TerrainTestScene] Création d'une map de test procédurale")
            self._terrain_manager = TerrainMapLoader.create_test_map(40, 25)

        # Crée le joueur au centre
        start_pos = Vector2(100, 100)
        self._player = Entity("TerrainPlayer")
        self._player.add_tag("player")

        # Ajoute les composants
        self._player.add_component(TransformComponent, start_pos)
        self._player.add_component(
            PhysicsComponent,
            mass=GameConfig.CYCLIST_MASS,
            drag=GameConfig.CYCLIST_DRAG,
            max_speed=GameConfig.CYCLIST_MAX_SPEED
        )

        # Ajoute le CommandInputComponent
        self._player.add_component(
            CommandInputComponent,
            profile_name="hybrid"
        )

        # Ajoute le TerrainPhysicsComponent (intégration terrain)
        self._player.add_component(
            TerrainPhysicsComponent,
            terrain_manager=self._terrain_manager,
            base_max_speed=GameConfig.CYCLIST_MAX_SPEED,
            base_drag=GameConfig.CYCLIST_DRAG
        )

        # Ajoute le renderer
        self._player.add_component(
            SpriteRendererComponent,
            width=40,
            height=60,
            color=Colors.CYAN,
            use_rotation=True
        )

        # Ajoute le joueur à l'Entity Manager
        self._entity_manager.add_entity(self._player)

        print(f"[TerrainTestScene] Terrain: {self._terrain_manager}")

    def exit(self) -> None:
        """Nettoie la scène lors de sa désactivation."""
        print("[TerrainTestScene] Sortie de la scène")
        self._entity_manager.clear()
        if self._terrain_manager:
            self._terrain_manager.clear()
        self._player = None
        self._terrain_manager = None

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Gère les événements de la scène.

        Args:
            events: Liste des événements Pygame
        """
        # Transmet les événements au CommandInputComponent du joueur
        if self._player:
            input_comp = self._player.get_component(CommandInputComponent)
            if input_comp:
                input_comp.set_events(events)

        # Gère les événements de la scène
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._reset_player()

    def _reset_player(self) -> None:
        """Réinitialise la position et la vélocité du joueur."""
        if not self._player:
            return

        transform = self._player.get_component(TransformComponent)
        physics = self._player.get_component(PhysicsComponent)

        if transform and physics:
            transform.position = Vector2(100, 100)
            transform.rotation = 0
            physics.stop()
            print("[TerrainTestScene] Joueur réinitialisé")

    def update(self, delta_time: float) -> None:
        """
        Met à jour la logique de la scène.

        Args:
            delta_time: Temps écoulé depuis la dernière frame
        """
        # Met à jour toutes les entités
        self._entity_manager.update(delta_time)

        # Met à jour la caméra pour suivre le joueur
        self._update_camera()

    def _update_camera(self) -> None:
        """Met à jour la position de la caméra pour suivre le joueur."""
        if not self._player:
            return

        transform = self._player.get_component(TransformComponent)
        if not transform:
            return

        # Centre la caméra sur le joueur
        target_x = transform.position.x - GameConfig.WINDOW_WIDTH / 2
        target_y = transform.position.y - GameConfig.WINDOW_HEIGHT / 2

        # Clamp pour ne pas dépasser les limites du terrain
        if self._terrain_manager:
            max_x = max(0, self._terrain_manager.get_world_width() - GameConfig.WINDOW_WIDTH)
            max_y = max(0, self._terrain_manager.get_world_height() - GameConfig.WINDOW_HEIGHT)

            target_x = max(0, min(target_x, max_x))
            target_y = max(0, min(target_y, max_y))

        self._camera_offset = Vector2(target_x, target_y)

    def render(self, screen: pygame.Surface) -> None:
        """
        Effectue le rendu de la scène.

        Args:
            screen: Surface Pygame sur laquelle dessiner
        """
        # Fond
        screen.fill(GameConfig.BACKGROUND_COLOR)

        # Rend le terrain
        if self._terrain_manager:
            self._terrain_manager.render(screen, self._camera_offset)

        # Rend les entités (avec offset caméra)
        for entity in self._entity_manager.get_all_entities():
            renderer = entity.get_component(SpriteRendererComponent)
            if renderer and entity.active:
                # Applique l'offset caméra
                transform = entity.get_component(TransformComponent)
                if transform:
                    original_pos = transform.position.copy()
                    transform.position = transform.position - self._camera_offset
                    renderer.render(screen)
                    transform.position = original_pos

        # Affiche le HUD (pas affecté par la caméra)
        self._render_hud(screen)
        self._render_instructions(screen)

    def _render_hud(self, screen: pygame.Surface) -> None:
        """Affiche le HUD avec les stats du joueur."""
        if not self._player or not self._font_small:
            return

        transform = self._player.get_component(TransformComponent)
        physics = self._player.get_component(PhysicsComponent)
        terrain_physics = self._player.get_component(TerrainPhysicsComponent)

        if not transform or not physics or not terrain_physics:
            return

        # Récupère les infos du terrain
        terrain_name = terrain_physics.get_current_terrain_name()
        terrain_type = terrain_physics.get_current_terrain_type()
        grip = terrain_physics.get_current_grip_level()
        stamina_drain = terrain_physics.get_current_stamina_drain()

        hud_texts = [
            f"Terrain: {terrain_name}",
            f"Type: {terrain_type.name}",
            f"Position: ({transform.position.x:.0f}, {transform.position.y:.0f})",
            f"Vitesse: {physics.get_speed():.1f} / {physics.max_speed:.1f} px/s",
            f"Adherence: {grip:.2f}",
            f"Drain stamina: {stamina_drain:.1f}x",
            f"Drag: {physics.drag:.3f}",
        ]

        y_offset = 10
        for text in hud_texts:
            self._render_text_with_bg(screen, text, 10, y_offset)
            y_offset += 30

    def _render_instructions(self, screen: pygame.Surface) -> None:
        """Affiche les instructions."""
        if not self._font_small:
            return

        instructions = [
            "Fleches/WASD : Deplacer",
            "ESPACE : Sprint",
            "R : Reset position",
            "ESC : Quitter",
        ]

        y_offset = GameConfig.WINDOW_HEIGHT - 140
        for instruction in instructions:
            self._render_text_with_bg(
                screen,
                instruction,
                GameConfig.WINDOW_WIDTH - 300,
                y_offset,
                align_right=True
            )
            y_offset += 30

    def _render_text_with_bg(
        self,
        screen: pygame.Surface,
        text: str,
        x: int,
        y: int,
        align_right: bool = False
    ) -> None:
        """
        Rend du texte avec fond semi-transparent.

        Args:
            screen: Surface de rendu
            text: Texte à afficher
            x: Position x
            y: Position y
            align_right: Si vrai, aligne à droite
        """
        if not self._font_small:
            return

        text_surface = self._font_small.render(text, True, Colors.WHITE)
        text_rect = text_surface.get_rect()

        if align_right:
            text_rect.topright = (x, y)
        else:
            text_rect.topleft = (x, y)

        # Fond semi-transparent
        bg_rect = text_rect.inflate(10, 4)
        bg_surface = pygame.Surface(bg_rect.size)
        bg_surface.set_alpha(128)
        bg_surface.fill(Colors.BLACK)
        screen.blit(bg_surface, bg_rect.topleft)

        # Texte
        screen.blit(text_surface, text_rect.topleft)
