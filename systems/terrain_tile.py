"""
Terrain Tile - Représente une tuile de terrain individuelle.

Chaque tuile occupe une position dans la grille et affecte la physique
des entités qui la traversent.
"""

import pygame
from systems.terrain_data import TerrainData
from utils.vector2 import Vector2


class TerrainTile:
    """
    Tuile de terrain avec rendu et détection de collision.

    Une tuile représente une zone rectangulaire de terrain avec des
    propriétés physiques spécifiques (vitesse, adhérence, etc.).
    """

    # Taille par défaut d'une tuile (configurable)
    DEFAULT_TILE_SIZE = 32

    def __init__(
        self,
        terrain_data: TerrainData,
        grid_x: int,
        grid_y: int,
        tile_size: int = DEFAULT_TILE_SIZE
    ) -> None:
        """
        Initialise une tuile de terrain.

        Args:
            terrain_data: Données du terrain (type, propriétés physiques)
            grid_x: Position X dans la grille
            grid_y: Position Y dans la grille
            tile_size: Taille de la tuile en pixels
        """
        self.terrain_data = terrain_data
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tile_size = tile_size

        # Crée le rectangle de collision
        self.rect = pygame.Rect(
            grid_x * tile_size,
            grid_y * tile_size,
            tile_size,
            tile_size
        )

        # Cache la surface de rendu
        self._surface: pygame.Surface | None = None
        self._create_surface()

    def _create_surface(self) -> None:
        """Crée la surface de rendu pour cette tuile."""
        self._surface = pygame.Surface((self.tile_size, self.tile_size))
        self._surface.fill(self.terrain_data.color)

        # Ajoute une bordure subtile pour visualiser les tuiles
        border_color = tuple(max(0, c - 20) for c in self.terrain_data.color)
        pygame.draw.rect(
            self._surface,
            border_color,
            self._surface.get_rect(),
            1  # Bordure de 1 pixel
        )

    def contains(self, position: Vector2) -> bool:
        """
        Vérifie si une position est à l'intérieur de cette tuile.

        Args:
            position: Position à vérifier

        Returns:
            True si la position est dans la tuile, False sinon
        """
        return self.rect.collidepoint(position.x, position.y)

    def get_world_position(self) -> Vector2:
        """
        Retourne la position mondiale (en pixels) du coin supérieur gauche.

        Returns:
            Position Vector2
        """
        return Vector2(self.rect.x, self.rect.y)

    def get_center_position(self) -> Vector2:
        """
        Retourne la position du centre de la tuile.

        Returns:
            Position Vector2 du centre
        """
        return Vector2(self.rect.centerx, self.rect.centery)

    def render(
        self,
        screen: pygame.Surface,
        camera_offset: Vector2 = Vector2(0, 0)
    ) -> None:
        """
        Rend la tuile à l'écran.

        Args:
            screen: Surface Pygame sur laquelle dessiner
            camera_offset: Offset de la caméra pour le scrolling
        """
        if not self._surface:
            return

        # Calcule la position d'affichage avec l'offset de caméra
        draw_x = self.rect.x - camera_offset.x
        draw_y = self.rect.y - camera_offset.y

        # Dessine uniquement si visible à l'écran (culling simple)
        screen_rect = screen.get_rect()
        if (draw_x + self.tile_size >= 0 and draw_x < screen_rect.width and
            draw_y + self.tile_size >= 0 and draw_y < screen_rect.height):
            screen.blit(self._surface, (draw_x, draw_y))

    def get_terrain_type_name(self) -> str:
        """
        Retourne le nom du type de terrain.

        Returns:
            Nom du terrain
        """
        return self.terrain_data.name

    def __repr__(self) -> str:
        """Représentation string de la tuile."""
        return (
            f"TerrainTile(type={self.terrain_data.terrain_type.name}, "
            f"grid=({self.grid_x}, {self.grid_y}), "
            f"size={self.tile_size})"
        )
