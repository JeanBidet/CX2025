"""
Scène de test pour valider l'architecture du jeu.

Cette scène affiche un rectangle contrôlable pour démontrer le fonctionnement
de l'architecture Entity-Component et du système de rendu.
"""

from typing import Optional
import pygame
from scenes.scene import Scene
from entities.entity import Entity
from components.renderer_component import RendererComponent
from components.movement_component import MovementComponent
from config.game_config import GameConfig
from config.constants import Colors


class TestScene(Scene):
    """
    Scène de test affichant un rectangle contrôlable.

    Cette scène démontre :
    - L'architecture Entity-Component
    - Le système de rendu
    - La gestion des inputs
    - L'Entity Manager
    """

    def __init__(self) -> None:
        """Initialise la scène de test."""
        super().__init__("TestScene")
        self._player: Optional[Entity] = None
        self._font: Optional[pygame.font.Font] = None

    def enter(self, data: Optional[dict] = None) -> None:
        """
        Initialise la scène lors de son activation.

        Args:
            data: Données optionnelles de la scène précédente
        """
        print(f"[TestScene] Entrée dans la scène de test")

        # Initialise la police pour le texte
        self._font = pygame.font.Font(None, 36)

        # Crée le joueur (rectangle contrôlable)
        self._player = Entity("Player")
        self._player.position = Vector2(
            GameConfig.WINDOW_WIDTH / 2,
            GameConfig.WINDOW_HEIGHT / 2
        )
        self._player.add_tag("player")

        # Ajoute les composants
        self._player.add_component(RendererComponent, 50, 50, Colors.CYAN)
        self._player.add_component(MovementComponent, GameConfig.PLAYER_SPEED)

        # Ajoute le joueur à l'Entity Manager
        self._entity_manager.add_entity(self._player)

        # Crée quelques obstacles statiques pour référence visuelle
        self._create_obstacles()

        print(f"[TestScene] Scène initialisée avec {self._entity_manager.entity_count()} entités")

    def _create_obstacles(self) -> None:
        """Crée quelques obstacles statiques pour référence visuelle."""
        from utils.vector2 import Vector2

        # Obstacle en haut à gauche
        obstacle1 = Entity("Obstacle1")
        obstacle1.position = Vector2(200, 150)
        obstacle1.add_component(RendererComponent, 80, 80, Colors.RED)
        obstacle1.add_tag("obstacle")
        self._entity_manager.add_entity(obstacle1)

        # Obstacle en haut à droite
        obstacle2 = Entity("Obstacle2")
        obstacle2.position = Vector2(GameConfig.WINDOW_WIDTH - 200, 150)
        obstacle2.add_component(RendererComponent, 60, 100, Colors.GREEN)
        obstacle2.add_tag("obstacle")
        self._entity_manager.add_entity(obstacle2)

        # Obstacle en bas au centre
        obstacle3 = Entity("Obstacle3")
        obstacle3.position = Vector2(GameConfig.WINDOW_WIDTH / 2, GameConfig.WINDOW_HEIGHT - 150)
        obstacle3.add_component(RendererComponent, 120, 40, Colors.YELLOW)
        obstacle3.add_tag("obstacle")
        self._entity_manager.add_entity(obstacle3)

    def exit(self) -> None:
        """Nettoie la scène lors de sa désactivation."""
        print(f"[TestScene] Sortie de la scène de test")
        self._entity_manager.clear()
        self._player = None
        self._font = None

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Gère les événements de la scène.

        Args:
            events: Liste des événements Pygame
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # On pourrait changer de scène ici
                    print("[TestScene] Touche ESCAPE pressée")
                elif event.key == pygame.K_SPACE:
                    print(f"[TestScene] Position du joueur: {self._player.position}")

    def update(self, delta_time: float) -> None:
        """
        Met à jour la logique de la scène.

        Args:
            delta_time: Temps écoulé depuis la dernière frame en secondes
        """
        # Met à jour toutes les entités via l'Entity Manager
        self._entity_manager.update(delta_time)

    def render(self, screen: pygame.Surface) -> None:
        """
        Effectue le rendu de la scène.

        Args:
            screen: Surface Pygame sur laquelle dessiner
        """
        # Fond
        screen.fill(GameConfig.BACKGROUND_COLOR)

        # Rend toutes les entités avec un composant de rendu
        for entity in self._entity_manager.get_all_entities():
            renderer = entity.get_component(RendererComponent)
            if renderer and entity.active:
                renderer.render(screen)

        # Affiche les instructions
        self._render_instructions(screen)

    def _render_instructions(self, screen: pygame.Surface) -> None:
        """
        Affiche les instructions à l'écran.

        Args:
            screen: Surface Pygame sur laquelle dessiner
        """
        if self._font is None:
            return

        instructions = [
            "Utilisez les flèches ou WASD pour déplacer le rectangle cyan",
            "Appuyez sur ESPACE pour afficher la position",
            "Appuyez sur ECHAP pour quitter",
        ]

        y_offset = 20
        for instruction in instructions:
            text_surface = self._font.render(instruction, True, Colors.WHITE)
            screen.blit(text_surface, (20, y_offset))
            y_offset += 40


# Import nécessaire pour Vector2
from utils.vector2 import Vector2
