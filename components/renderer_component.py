"""
Composant de rendu pour afficher une entité à l'écran.

Ce composant sépare la logique de rendu de la logique métier,
permettant une architecture plus modulaire.
"""

from typing import Tuple
import pygame
from components.icomponent import IComponent
from config.constants import Colors


class RendererComponent(IComponent):
    """
    Composant de rendu basique affichant un rectangle coloré.

    Ce composant sera étendu dans les futurs prompts pour gérer
    des sprites, des animations, etc.
    """

    def __init__(
        self,
        owner,
        width: int = 50,
        height: int = 50,
        color: Tuple[int, int, int] = Colors.BLUE
    ) -> None:
        """
        Initialise le composant de rendu.

        Args:
            owner: L'entité propriétaire
            width: Largeur du rectangle
            height: Hauteur du rectangle
            color: Couleur du rectangle (RGB)
        """
        super().__init__(owner)
        self.width: int = width
        self.height: int = height
        self.color: Tuple[int, int, int] = color

    def init(self) -> None:
        """Initialise le composant."""
        pass

    def update(self, delta_time: float) -> None:
        """
        Met à jour le composant (rien à faire pour le rendu basique).

        Args:
            delta_time: Temps écoulé depuis la dernière frame
        """
        pass

    def render(self, screen: pygame.Surface) -> None:
        """
        Dessine le rectangle à l'écran.

        Args:
            screen: Surface Pygame sur laquelle dessiner
        """
        # Récupère la position de l'entité
        pos = self.owner.position
        scale = self.owner.scale

        # Calcule les dimensions avec le scale
        scaled_width = self.width * scale.x
        scaled_height = self.height * scale.y

        # Crée le rectangle centré sur la position de l'entité
        rect = pygame.Rect(
            pos.x - scaled_width / 2,
            pos.y - scaled_height / 2,
            scaled_width,
            scaled_height
        )

        # Dessine le rectangle
        pygame.draw.rect(screen, self.color, rect)

    def destroy(self) -> None:
        """Nettoie les ressources du composant."""
        pass

    def __repr__(self) -> str:
        """Représentation string du composant."""
        return f"RendererComponent(color={self.color}, size={self.width}x{self.height})"
