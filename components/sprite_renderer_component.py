"""
Sprite Renderer Component - Rendu d'entités avec rotation et sprites.

Ce composant améliore le RendererComponent de base en ajoutant la gestion
de la rotation et la possibilité de charger des sprites.
"""

from typing import Tuple
import pygame
import math
from components.icomponent import IComponent
from components.transform_component import TransformComponent
from config.constants import Colors


class SpriteRendererComponent(IComponent):
    """
    Composant de rendu avec support de la rotation et des sprites.

    Supporte :
    - Rectangles colorés
    - Sprites chargés depuis des images
    - Rotation automatique basée sur le TransformComponent
    - Cache des sprites tournés pour optimisation
    """

    def __init__(
        self,
        owner,
        width: int = 50,
        height: int = 50,
        color: Tuple[int, int, int] = Colors.BLUE,
        sprite_path: str | None = None,
        use_rotation: bool = True,
        draw_direction_arrow: bool = True
    ) -> None:
        """
        Initialise le composant de rendu.

        Args:
            owner: L'entité propriétaire
            width: Largeur du sprite/rectangle
            height: Hauteur du sprite/rectangle
            color: Couleur si mode rectangle (RGB)
            sprite_path: Chemin vers l'image sprite (optionnel)
            use_rotation: Si vrai, applique la rotation du TransformComponent
            draw_direction_arrow: Si vrai, dessine une flèche pour indiquer la direction
        """
        super().__init__(owner)

        self.width: int = width
        self.height: int = height
        self.color: Tuple[int, int, int] = color
        self.sprite_path: str | None = sprite_path
        self.use_rotation: bool = use_rotation
        self.draw_direction_arrow: bool = draw_direction_arrow

        # Sprite original
        self._original_surface: pygame.Surface | None = None

        # Référence au TransformComponent
        self._transform: TransformComponent | None = None

        # Cache de rotation (optionnel, pour optimisation future)
        self._cached_rotation: float = 0.0
        self._cached_surface: pygame.Surface | None = None

    def init(self) -> None:
        """Initialise le composant et charge le sprite si nécessaire."""
        # Récupère le TransformComponent
        self._transform = self.owner.get_component(TransformComponent)

        # Charge ou crée le sprite
        if self.sprite_path:
            self._load_sprite()
        else:
            self._create_default_sprite()

    def _load_sprite(self) -> None:
        """Charge un sprite depuis un fichier image."""
        try:
            # Charge l'image
            loaded_image = pygame.image.load(self.sprite_path)
            # Redimensionne si nécessaire
            self._original_surface = pygame.transform.scale(
                loaded_image,
                (self.width, self.height)
            )
            # Convertit avec alpha pour la transparence
            self._original_surface = self._original_surface.convert_alpha()
        except (pygame.error, FileNotFoundError) as e:
            print(f"[Warning] Impossible de charger le sprite {self.sprite_path}: {e}")
            print("[Warning] Utilisation d'un rectangle par défaut")
            self._create_default_sprite()

    def _create_default_sprite(self) -> None:
        """Crée un sprite rectangle par défaut avec une flèche directionnelle."""
        # Crée une surface avec transparence
        self._original_surface = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA
        )

        # Dessine le rectangle principal
        pygame.draw.rect(
            self._original_surface,
            self.color,
            pygame.Rect(0, 0, self.width, self.height)
        )

        # Dessine une flèche pour indiquer l'avant du véhicule
        if self.draw_direction_arrow:
            # Triangle pointant vers la droite (direction par défaut)
            arrow_color = Colors.WHITE
            points = [
                (self.width - 5, self.height // 2),  # Pointe
                (self.width - 15, self.height // 2 - 8),  # Haut
                (self.width - 15, self.height // 2 + 8)  # Bas
            ]
            pygame.draw.polygon(self._original_surface, arrow_color, points)

        # Convertit avec alpha
        self._original_surface = self._original_surface.convert_alpha()

    def update(self, delta_time: float) -> None:
        """
        Met à jour le composant.

        Args:
            delta_time: Temps écoulé depuis la dernière frame
        """
        # Rien à faire dans update pour un rendu statique
        pass

    def render(self, screen: pygame.Surface) -> None:
        """
        Dessine le sprite à l'écran avec rotation.

        Args:
            screen: Surface Pygame sur laquelle dessiner
        """
        if self._original_surface is None or self._transform is None:
            return

        # Récupère la position et rotation
        pos = self._transform.position
        rotation_radians = self._transform.rotation

        # Convertit la rotation en degrés pour Pygame (rotation inverse car axes Y inversé)
        rotation_degrees = -math.degrees(rotation_radians)

        # Applique la rotation au sprite
        if self.use_rotation:
            rotated_surface = pygame.transform.rotate(
                self._original_surface,
                rotation_degrees
            )
        else:
            rotated_surface = self._original_surface

        # Calcule le rectangle pour centrer le sprite sur la position
        rect = rotated_surface.get_rect()
        rect.center = pos.to_int_tuple()

        # Dessine le sprite
        screen.blit(rotated_surface, rect.topleft)

        # Debug : dessine le centre
        if False:  # Active pour debug
            pygame.draw.circle(screen, Colors.RED, pos.to_int_tuple(), 3)

    def set_color(self, color: Tuple[int, int, int]) -> None:
        """
        Change la couleur du sprite (recrée le sprite par défaut).

        Args:
            color: Nouvelle couleur RGB
        """
        self.color = color
        if self.sprite_path is None:
            self._create_default_sprite()

    def set_sprite(self, sprite_path: str) -> None:
        """
        Change le sprite en chargeant une nouvelle image.

        Args:
            sprite_path: Chemin vers la nouvelle image
        """
        self.sprite_path = sprite_path
        self._load_sprite()

    def destroy(self) -> None:
        """Nettoie les ressources du composant."""
        self._original_surface = None
        self._cached_surface = None
        self._transform = None

    def __repr__(self) -> str:
        """Représentation string du composant."""
        if self.sprite_path:
            return f"SpriteRendererComponent(sprite={self.sprite_path})"
        else:
            return f"SpriteRendererComponent(color={self.color}, size={self.width}x{self.height})"
