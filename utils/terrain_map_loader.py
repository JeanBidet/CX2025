"""
Terrain Map Loader - Charge des maps de terrain depuis des fichiers JSON.

Permet de définir des layouts de terrain dans des fichiers JSON et de les
charger dans un TerrainManager.
"""

import json
from pathlib import Path
from typing import Any
from systems.terrain_data import TerrainType
from systems.terrain_manager import TerrainManager
from systems.terrain_tile import TerrainTile


class TerrainMapLoader:
    """
    Utilitaire pour charger des maps de terrain depuis JSON.

    Format JSON attendu:
    {
        "name": "Nom de la map",
        "width": 30,
        "height": 20,
        "tile_size": 32,
        "terrain_grid": [
            ["GRASS", "GRASS", "ASPHALT", ...],
            ["GRASS", "MUD", "ASPHALT", ...],
            ...
        ]
    }
    """

    @staticmethod
    def load_from_file(file_path: str | Path) -> TerrainManager:
        """
        Charge une map de terrain depuis un fichier JSON.

        Args:
            file_path: Chemin vers le fichier JSON

        Returns:
            TerrainManager configuré avec la map

        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            ValueError: Si le format JSON est invalide
            KeyError: Si des champs requis sont manquants
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Fichier de map introuvable: {file_path}")

        # Charge le JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return TerrainMapLoader.load_from_dict(data)

    @staticmethod
    def load_from_dict(data: dict[str, Any]) -> TerrainManager:
        """
        Charge une map de terrain depuis un dictionnaire.

        Args:
            data: Dictionnaire contenant les données de map

        Returns:
            TerrainManager configuré avec la map

        Raises:
            ValueError: Si le format est invalide
            KeyError: Si des champs requis sont manquants
        """
        # Valide les champs requis
        required_fields = ["width", "height", "terrain_grid"]
        for field in required_fields:
            if field not in data:
                raise KeyError(f"Champ requis manquant dans la map: {field}")

        width = data["width"]
        height = data["height"]
        tile_size = data.get("tile_size", TerrainTile.DEFAULT_TILE_SIZE)
        terrain_grid_str = data["terrain_grid"]

        # Valide les dimensions
        if len(terrain_grid_str) != height:
            raise ValueError(
                f"Hauteur de grille invalide: {len(terrain_grid_str)} != {height}"
            )

        # Convertit les strings en TerrainType
        terrain_grid: list[list[TerrainType]] = []
        for y, row in enumerate(terrain_grid_str):
            if len(row) != width:
                raise ValueError(
                    f"Largeur de grille invalide à la ligne {y}: "
                    f"{len(row)} != {width}"
                )

            terrain_row: list[TerrainType] = []
            for x, terrain_name in enumerate(row):
                try:
                    terrain_type = TerrainType[terrain_name]
                    terrain_row.append(terrain_type)
                except KeyError:
                    raise ValueError(
                        f"Type de terrain invalide '{terrain_name}' "
                        f"à la position ({x}, {y})"
                    )

            terrain_grid.append(terrain_row)

        # Crée le TerrainManager
        manager = TerrainManager(width, height, tile_size)
        manager.set_terrain_from_grid(terrain_grid)

        map_name = data.get("name", "Unnamed Map")
        print(f"[TerrainMapLoader] Map '{map_name}' chargée: {width}x{height}")

        return manager

    @staticmethod
    def save_to_file(
        terrain_manager: TerrainManager,
        file_path: str | Path,
        map_name: str = "Custom Map"
    ) -> None:
        """
        Sauvegarde un TerrainManager dans un fichier JSON.

        Args:
            terrain_manager: Manager à sauvegarder
            file_path: Chemin de destination
            map_name: Nom de la map
        """
        file_path = Path(file_path)

        # Crée la grille de strings depuis le TerrainManager
        terrain_grid: list[list[str]] = []
        for y in range(terrain_manager.height):
            row: list[str] = []
            for x in range(terrain_manager.width):
                tile = terrain_manager.get_tile_at_grid(x, y)
                if tile:
                    row.append(tile.terrain_data.terrain_type.name)
                else:
                    row.append("GRASS")  # Fallback
            terrain_grid.append(row)

        # Crée le dictionnaire de données
        data = {
            "name": map_name,
            "width": terrain_manager.width,
            "height": terrain_manager.height,
            "tile_size": terrain_manager.tile_size,
            "terrain_grid": terrain_grid
        }

        # Sauvegarde en JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"[TerrainMapLoader] Map sauvegardée: {file_path}")

    @staticmethod
    def create_test_map(width: int, height: int) -> TerrainManager:
        """
        Crée une map de test avec différents types de terrain.

        Args:
            width: Largeur de la map
            height: Hauteur de la map

        Returns:
            TerrainManager avec une map de test
        """
        # Crée une grille variée pour les tests
        terrain_grid: list[list[TerrainType]] = []

        for y in range(height):
            row: list[TerrainType] = []
            for x in range(width):
                # Crée des bandes de terrain différentes
                if x < width // 7:
                    terrain = TerrainType.ASPHALT
                elif x < 2 * width // 7:
                    terrain = TerrainType.GRASS
                elif x < 3 * width // 7:
                    terrain = TerrainType.DIRT
                elif x < 4 * width // 7:
                    terrain = TerrainType.GRAVEL
                elif x < 5 * width // 7:
                    terrain = TerrainType.SAND
                elif x < 6 * width // 7:
                    terrain = TerrainType.MUD
                else:
                    terrain = TerrainType.CONCRETE

                row.append(terrain)
            terrain_grid.append(row)

        manager = TerrainManager(width, height)
        manager.set_terrain_from_grid(terrain_grid)

        return manager
