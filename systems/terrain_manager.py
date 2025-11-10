"""
Terrain Manager - Gère la grille de terrain du jeu.

Responsable de la création, du stockage et de l'accès aux tuiles de terrain.
Fournit des méthodes pour récupérer le terrain à une position donnée et
rendre toutes les tuiles visibles.
"""

from typing import Optional
import pygame
from systems.terrain_data import TerrainType, TerrainData
from systems.terrain_tile import TerrainTile
from patterns.factories.terrain_factory import TerrainFactory
from utils.vector2 import Vector2


class TerrainManager:
    """
    Gestionnaire de la grille de terrain.

    Maintient une grille 2D de TerrainTile et fournit des méthodes
    pour accéder au terrain à différentes positions.
    """

    def __init__(
        self,
        width: int,
        height: int,
        tile_size: int = TerrainTile.DEFAULT_TILE_SIZE,
        default_terrain: TerrainType = TerrainType.GRASS
    ) -> None:
        """
        Initialise le gestionnaire de terrain.

        Args:
            width: Largeur de la grille en tuiles
            height: Hauteur de la grille en tuiles
            tile_size: Taille d'une tuile en pixels
            default_terrain: Type de terrain par défaut
        """
        self.width = width
        self.height = height
        self.tile_size = tile_size

        # Crée la grille 2D de tuiles
        self._grid: list[list[TerrainTile]] = []
        self._initialize_grid(default_terrain)

    def _initialize_grid(self, default_terrain: TerrainType) -> None:
        """
        Initialise la grille avec un terrain par défaut.

        Args:
            default_terrain: Type de terrain pour toutes les tuiles
        """
        terrain_data = TerrainFactory.create(default_terrain)

        for y in range(self.height):
            row: list[TerrainTile] = []
            for x in range(self.width):
                tile = TerrainTile(terrain_data, x, y, self.tile_size)
                row.append(tile)
            self._grid.append(row)

    def set_terrain_from_grid(
        self,
        terrain_grid: list[list[TerrainType]]
    ) -> None:
        """
        Définit le terrain à partir d'une grille de TerrainType.

        Args:
            terrain_grid: Grille 2D de types de terrain

        Raises:
            ValueError: Si les dimensions ne correspondent pas
        """
        if len(terrain_grid) != self.height:
            raise ValueError(
                f"Hauteur de grille invalide: {len(terrain_grid)} != {self.height}"
            )

        for y, row in enumerate(terrain_grid):
            if len(row) != self.width:
                raise ValueError(
                    f"Largeur de grille invalide à la ligne {y}: "
                    f"{len(row)} != {self.width}"
                )

            for x, terrain_type in enumerate(row):
                terrain_data = TerrainFactory.create(terrain_type)
                self._grid[y][x] = TerrainTile(
                    terrain_data, x, y, self.tile_size
                )

    def get_tile_at_grid(self, grid_x: int, grid_y: int) -> Optional[TerrainTile]:
        """
        Récupère une tuile par ses coordonnées de grille.

        Args:
            grid_x: Position X dans la grille
            grid_y: Position Y dans la grille

        Returns:
            TerrainTile ou None si hors limites
        """
        if not self._is_valid_grid_position(grid_x, grid_y):
            return None

        return self._grid[grid_y][grid_x]

    def get_terrain_at_position(self, position: Vector2) -> Optional[TerrainTile]:
        """
        Récupère la tuile de terrain à une position mondiale.

        Args:
            position: Position en pixels (monde)

        Returns:
            TerrainTile à cette position, ou None si hors limites
        """
        # Convertit la position mondiale en coordonnées de grille
        grid_x = int(position.x // self.tile_size)
        grid_y = int(position.y // self.tile_size)

        return self.get_tile_at_grid(grid_x, grid_y)

    def get_terrain_data_at_position(
        self,
        position: Vector2
    ) -> Optional[TerrainData]:
        """
        Récupère les données de terrain à une position.

        Args:
            position: Position en pixels (monde)

        Returns:
            TerrainData à cette position, ou None si hors limites
        """
        tile = self.get_terrain_at_position(position)
        return tile.terrain_data if tile else None

    def _is_valid_grid_position(self, grid_x: int, grid_y: int) -> bool:
        """
        Vérifie si une position de grille est valide.

        Args:
            grid_x: Position X dans la grille
            grid_y: Position Y dans la grille

        Returns:
            True si la position est dans les limites
        """
        return 0 <= grid_x < self.width and 0 <= grid_y < self.height

    def get_world_width(self) -> int:
        """
        Retourne la largeur du terrain en pixels.

        Returns:
            Largeur en pixels
        """
        return self.width * self.tile_size

    def get_world_height(self) -> int:
        """
        Retourne la hauteur du terrain en pixels.

        Returns:
            Hauteur en pixels
        """
        return self.height * self.tile_size

    def render(
        self,
        screen: pygame.Surface,
        camera_offset: Vector2 = Vector2(0, 0)
    ) -> None:
        """
        Rend toutes les tuiles de terrain visibles.

        Args:
            screen: Surface Pygame sur laquelle dessiner
            camera_offset: Offset de la caméra pour le scrolling
        """
        # Calcule les limites de rendu (culling)
        screen_rect = screen.get_rect()

        # Détermine quelle portion de la grille est visible
        start_x = max(0, int(camera_offset.x // self.tile_size))
        start_y = max(0, int(camera_offset.y // self.tile_size))
        end_x = min(
            self.width,
            int((camera_offset.x + screen_rect.width) // self.tile_size) + 1
        )
        end_y = min(
            self.height,
            int((camera_offset.y + screen_rect.height) // self.tile_size) + 1
        )

        # Rend uniquement les tuiles visibles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self._grid[y][x]
                tile.render(screen, camera_offset)

    def get_all_tiles(self) -> list[TerrainTile]:
        """
        Retourne toutes les tuiles de terrain (utilisé pour debug/tests).

        Returns:
            Liste plate de toutes les tuiles
        """
        tiles = []
        for row in self._grid:
            tiles.extend(row)
        return tiles

    def clear(self) -> None:
        """Nettoie toutes les tuiles."""
        self._grid.clear()

    def __repr__(self) -> str:
        """Représentation string du gestionnaire."""
        return (
            f"TerrainManager(size={self.width}x{self.height}, "
            f"tile_size={self.tile_size}, "
            f"world_size={self.get_world_width()}x{self.get_world_height()}px)"
        )
