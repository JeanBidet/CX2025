"""
Scène de test pour le système de physique.

Cette scène démontre le système de physique complet avec un cycliste contrôlable,
montrant l'inertie, l'accélération progressive et la rotation réaliste.
"""

from typing import Optional
import pygame
from scenes.scene import Scene
from entities.cyclist import Cyclist
from components.sprite_renderer_component import SpriteRendererComponent
from components.physics_component import PhysicsComponent
from components.transform_component import TransformComponent
from config.game_config import GameConfig
from config.constants import Colors
from utils.vector2 import Vector2


class PhysicsTestScene(Scene):
    """
    Scène de test pour valider le système de physique.

    Cette scène affiche :
    - Un cycliste contrôlable avec physique réaliste
    - Indicateurs visuels de vitesse et rotation
    - Informations de debug détaillées
    - Instructions pour tester les contrôles
    """

    def __init__(self) -> None:
        """Initialise la scène de test physique."""
        super().__init__("PhysicsTestScene")
        self._player: Optional[Cyclist] = None
        self._font: Optional[pygame.font.Font] = None
        self._font_small: Optional[pygame.font.Font] = None

    def enter(self, data: Optional[dict] = None) -> None:
        """
        Initialise la scène lors de son activation.

        Args:
            data: Données optionnelles de la scène précédente
        """
        print("[PhysicsTestScene] Entrée dans la scène de test physique")

        # Initialise les polices
        self._font = pygame.font.Font(None, 36)
        self._font_small = pygame.font.Font(None, 24)

        # Crée le joueur au centre de l'écran
        center_pos = Vector2(
            GameConfig.WINDOW_WIDTH / 2,
            GameConfig.WINDOW_HEIGHT / 2
        )
        self._player = Cyclist(
            name="Player",
            position=center_pos,
            is_player=True
        )
        self._player.add_tag("player")

        # Ajoute le renderer avec une couleur distinctive
        self._player.add_component(
            SpriteRendererComponent,
            width=40,
            height=60,
            color=Colors.CYAN,
            use_rotation=True,
            draw_direction_arrow=True
        )

        # Ajoute le joueur à l'Entity Manager
        self._entity_manager.add_entity(self._player)

        # Crée quelques obstacles statiques pour référence
        self._create_track_bounds()

        print(f"[PhysicsTestScene] Scène initialisée avec {self._entity_manager.entity_count()} entités")

    def _create_track_bounds(self) -> None:
        """Crée des marqueurs visuels pour les limites de la piste."""
        from entities.entity import Entity

        # Marqueurs aux coins
        corners = [
            (100, 100),
            (GameConfig.WINDOW_WIDTH - 100, 100),
            (100, GameConfig.WINDOW_HEIGHT - 100),
            (GameConfig.WINDOW_WIDTH - 100, GameConfig.WINDOW_HEIGHT - 100)
        ]

        for i, (x, y) in enumerate(corners):
            marker = Entity(f"Corner{i+1}")
            marker.add_component(TransformComponent, Vector2(x, y))
            marker.add_component(
                SpriteRendererComponent,
                width=30,
                height=30,
                color=Colors.YELLOW,
                use_rotation=False
            )
            marker.add_tag("marker")
            self._entity_manager.add_entity(marker)

        # Ligne de départ au centre en haut
        start_line = Entity("StartLine")
        start_line.add_component(
            TransformComponent,
            Vector2(GameConfig.WINDOW_WIDTH / 2, 150)
        )
        start_line.add_component(
            SpriteRendererComponent,
            width=200,
            height=10,
            color=Colors.WHITE,
            use_rotation=False
        )
        start_line.add_tag("marker")
        self._entity_manager.add_entity(start_line)

    def exit(self) -> None:
        """Nettoie la scène lors de sa désactivation."""
        print("[PhysicsTestScene] Sortie de la scène de test physique")
        self._entity_manager.clear()
        self._player = None
        self._font = None
        self._font_small = None

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Gère les événements de la scène.

        Args:
            events: Liste des événements Pygame
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset la position du joueur
                    if self._player:
                        transform = self._player.get_transform()
                        physics = self._player.get_physics()
                        transform.position = Vector2(
                            GameConfig.WINDOW_WIDTH / 2,
                            GameConfig.WINDOW_HEIGHT / 2
                        )
                        transform.rotation = 0
                        physics.stop()
                        print("[PhysicsTestScene] Position réinitialisée")

                elif event.key == pygame.K_SPACE:
                    # Affiche les stats du joueur
                    if self._player:
                        print(f"[PhysicsTestScene] Player stats: {self._player}")
                        print(f"  Transform: {self._player.get_transform()}")
                        print(f"  Physics: {self._player.get_physics()}")

    def update(self, delta_time: float) -> None:
        """
        Met à jour la logique de la scène.

        Args:
            delta_time: Temps écoulé depuis la dernière frame en secondes
        """
        # Met à jour toutes les entités
        self._entity_manager.update(delta_time)

        # Garde le joueur dans les limites de l'écran (avec marge)
        if self._player:
            self._clamp_player_to_bounds()

    def _clamp_player_to_bounds(self) -> None:
        """Garde le joueur dans les limites de l'écran."""
        if not self._player:
            return

        transform = self._player.get_transform()
        pos = transform.position

        margin = 50
        clamped = False

        # Vérifie les limites
        if pos.x < margin:
            pos.x = margin
            clamped = True
        elif pos.x > GameConfig.WINDOW_WIDTH - margin:
            pos.x = GameConfig.WINDOW_WIDTH - margin
            clamped = True

        if pos.y < margin:
            pos.y = margin
            clamped = True
        elif pos.y > GameConfig.WINDOW_HEIGHT - margin:
            pos.y = GameConfig.WINDOW_HEIGHT - margin
            clamped = True

        # Si on a touché un bord, réduit la vitesse
        if clamped:
            transform.position = pos
            physics = self._player.get_physics()
            physics.velocity = physics.velocity * 0.5

    def render(self, screen: pygame.Surface) -> None:
        """
        Effectue le rendu de la scène.

        Args:
            screen: Surface Pygame sur laquelle dessiner
        """
        # Fond vert gazon
        screen.fill(GameConfig.BACKGROUND_COLOR)

        # Rend toutes les entités avec sprite renderer
        for entity in self._entity_manager.get_all_entities():
            renderer = entity.get_component(SpriteRendererComponent)
            if renderer and entity.active:
                renderer.render(screen)

        # Affiche les informations
        self._render_hud(screen)
        self._render_instructions(screen)

    def _render_hud(self, screen: pygame.Surface) -> None:
        """
        Affiche le HUD avec les informations du joueur.

        Args:
            screen: Surface Pygame sur laquelle dessiner
        """
        if not self._player or not self._font_small:
            return

        # Récupère les stats du joueur
        transform = self._player.get_transform()
        physics = self._player.get_physics()
        speed = physics.get_speed()
        pos = transform.position
        rotation_deg = transform.rotation_degrees

        # Prépare les textes
        hud_texts = [
            f"Position: ({pos.x:.0f}, {pos.y:.0f})",
            f"Vitesse: {speed:.1f} px/s ({speed / physics.max_speed * 100:.0f}%)",
            f"Rotation: {rotation_deg:.1f}°",
            f"Velocite: ({physics.velocity.x:.1f}, {physics.velocity.y:.1f})",
        ]

        # Affiche le HUD en haut à gauche
        y_offset = 10
        for text in hud_texts:
            surface = self._font_small.render(text, True, Colors.WHITE)
            # Fond semi-transparent
            bg_rect = surface.get_rect()
            bg_rect.topleft = (10, y_offset)
            bg_rect.inflate_ip(10, 4)
            bg_surface = pygame.Surface(bg_rect.size)
            bg_surface.set_alpha(128)
            bg_surface.fill(Colors.BLACK)
            screen.blit(bg_surface, bg_rect.topleft)
            # Texte
            screen.blit(surface, (10, y_offset))
            y_offset += 30

        # Jauge de vitesse visuelle
        self._render_speed_gauge(screen, speed, physics.max_speed)

    def _render_speed_gauge(
        self,
        screen: pygame.Surface,
        speed: float,
        max_speed: float
    ) -> None:
        """
        Dessine une jauge de vitesse.

        Args:
            screen: Surface Pygame
            speed: Vitesse actuelle
            max_speed: Vitesse maximale
        """
        gauge_x = 10
        gauge_y = GameConfig.WINDOW_HEIGHT - 40
        gauge_width = 200
        gauge_height = 20

        # Fond de la jauge
        pygame.draw.rect(
            screen,
            Colors.DARK_GRAY,
            pygame.Rect(gauge_x, gauge_y, gauge_width, gauge_height)
        )

        # Remplissage proportionnel
        fill_width = int((speed / max_speed) * gauge_width)
        if fill_width > 0:
            # Couleur varie selon la vitesse
            if speed < max_speed * 0.3:
                color = Colors.GREEN
            elif speed < max_speed * 0.7:
                color = Colors.YELLOW
            else:
                color = Colors.RED

            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(gauge_x, gauge_y, fill_width, gauge_height)
            )

        # Bordure
        pygame.draw.rect(
            screen,
            Colors.WHITE,
            pygame.Rect(gauge_x, gauge_y, gauge_width, gauge_height),
            2
        )

    def _render_instructions(self, screen: pygame.Surface) -> None:
        """
        Affiche les instructions à l'écran.

        Args:
            screen: Surface Pygame sur laquelle dessiner
        """
        if not self._font_small:
            return

        instructions = [
            "Fleches / WASD : Accelerer et tourner",
            "R : Reset position",
            "ESPACE : Afficher stats",
            "ESC : Quitter",
        ]

        y_offset = GameConfig.WINDOW_HEIGHT - 150
        for instruction in instructions:
            text_surface = self._font_small.render(
                instruction,
                True,
                Colors.WHITE
            )
            # Fond semi-transparent
            bg_rect = text_surface.get_rect()
            bg_rect.topright = (GameConfig.WINDOW_WIDTH - 10, y_offset)
            bg_rect.inflate_ip(10, 4)
            bg_surface = pygame.Surface(bg_rect.size)
            bg_surface.set_alpha(128)
            bg_surface.fill(Colors.BLACK)
            screen.blit(bg_surface, bg_rect.topleft)
            # Texte
            screen.blit(text_surface, bg_rect.topleft)
            y_offset += 30
