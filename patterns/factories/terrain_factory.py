"""
Terrain Factory - Crée des terrains avec des configurations prédéfinies.

Implémente le Factory Pattern pour centraliser la création de différents
types de terrain avec leurs propriétés spécifiques.
"""

from typing import Dict
from systems.terrain_data import TerrainType, TerrainData
from config.constants import Colors


class TerrainFactory:
    """
    Factory pour créer des TerrainData avec des configurations prédéfinies.

    Utilise le pattern Factory pour encapsuler la logique de création
    et garantir des configurations cohérentes pour chaque type de terrain.
    """

    # Registry des terrains disponibles (cache)
    _terrain_registry: Dict[TerrainType, TerrainData] = {}

    @classmethod
    def create(cls, terrain_type: TerrainType) -> TerrainData:
        """
        Crée un TerrainData du type spécifié.

        Args:
            terrain_type: Type de terrain à créer

        Returns:
            TerrainData configuré pour ce type

        Raises:
            ValueError: Si le type de terrain n'est pas supporté
        """
        # Utilise le cache si disponible
        if terrain_type in cls._terrain_registry:
            return cls._terrain_registry[terrain_type]

        # Crée le terrain selon son type
        if terrain_type == TerrainType.ASPHALT:
            terrain = cls._create_asphalt()
        elif terrain_type == TerrainType.GRASS:
            terrain = cls._create_grass()
        elif terrain_type == TerrainType.SAND:
            terrain = cls._create_sand()
        elif terrain_type == TerrainType.MUD:
            terrain = cls._create_mud()
        elif terrain_type == TerrainType.GRAVEL:
            terrain = cls._create_gravel()
        elif terrain_type == TerrainType.DIRT:
            terrain = cls._create_dirt()
        elif terrain_type == TerrainType.CONCRETE:
            terrain = cls._create_concrete()
        else:
            raise ValueError(f"Type de terrain non supporté: {terrain_type}")

        # Met en cache
        cls._terrain_registry[terrain_type] = terrain
        return terrain

    @staticmethod
    def _create_asphalt() -> TerrainData:
        """
        Crée un terrain asphalte.

        Propriétés:
        - Vitesse: 100% (référence)
        - Adhérence: Excellente (0.9)
        - Endurance: Drain faible (0.8)
        - Idéal pour vitesse pure
        """
        return TerrainData(
            terrain_type=TerrainType.ASPHALT,
            speed_multiplier=1.0,
            stamina_drain_multiplier=0.8,
            grip_level=0.9,
            drag_modifier=0.0,
            color=(80, 80, 80),  # Gris foncé
            name="Asphalte"
        )

    @staticmethod
    def _create_grass() -> TerrainData:
        """
        Crée un terrain herbe.

        Propriétés:
        - Vitesse: 70% (ralentissement modéré)
        - Adhérence: Bonne (0.7)
        - Endurance: Drain moyen (1.2)
        - Terrain classique de cyclo-cross
        """
        return TerrainData(
            terrain_type=TerrainType.GRASS,
            speed_multiplier=0.7,
            stamina_drain_multiplier=1.2,
            grip_level=0.7,
            drag_modifier=0.015,
            color=Colors.GRASS_GREEN,  # Vert gazon
            name="Herbe"
        )

    @staticmethod
    def _create_sand() -> TerrainData:
        """
        Crée un terrain sable.

        Propriétés:
        - Vitesse: 50% (ralentissement important)
        - Adhérence: Faible (0.4)
        - Endurance: Drain élevé (1.8)
        - Très difficile, nécessite portage parfois
        """
        return TerrainData(
            terrain_type=TerrainType.SAND,
            speed_multiplier=0.5,
            stamina_drain_multiplier=1.8,
            grip_level=0.4,
            drag_modifier=0.03,
            color=Colors.SAND_YELLOW,  # Jaune sable
            name="Sable"
        )

    @staticmethod
    def _create_mud() -> TerrainData:
        """
        Crée un terrain boue.

        Propriétés:
        - Vitesse: 40% (très lent)
        - Adhérence: Très faible (0.3)
        - Endurance: Drain très élevé (2.0)
        - Le plus difficile, risque de chute
        """
        return TerrainData(
            terrain_type=TerrainType.MUD,
            speed_multiplier=0.4,
            stamina_drain_multiplier=2.0,
            grip_level=0.3,
            drag_modifier=0.04,
            color=Colors.MUD_BROWN,  # Marron boue
            name="Boue"
        )

    @staticmethod
    def _create_gravel() -> TerrainData:
        """
        Crée un terrain gravier.

        Propriétés:
        - Vitesse: 75% (bon compromis)
        - Adhérence: Moyenne (0.6)
        - Endurance: Drain moyen (1.1)
        - Adhérence variable, technique
        """
        return TerrainData(
            terrain_type=TerrainType.GRAVEL,
            speed_multiplier=0.75,
            stamina_drain_multiplier=1.1,
            grip_level=0.6,
            drag_modifier=0.01,
            color=(150, 150, 120),  # Gris-beige
            name="Gravier"
        )

    @staticmethod
    def _create_dirt() -> TerrainData:
        """
        Crée un terrain terre battue.

        Propriétés:
        - Vitesse: 80% (rapide)
        - Adhérence: Bonne (0.75)
        - Endurance: Drain faible (0.9)
        - Bon équilibre vitesse/adhérence
        """
        return TerrainData(
            terrain_type=TerrainType.DIRT,
            speed_multiplier=0.80,
            stamina_drain_multiplier=0.9,
            grip_level=0.75,
            drag_modifier=0.005,
            color=(139, 90, 43),  # Marron terre
            name="Terre battue"
        )

    @staticmethod
    def _create_concrete() -> TerrainData:
        """
        Crée un terrain béton.

        Propriétés:
        - Vitesse: 110% (bonus de vitesse!)
        - Adhérence: Excellente (0.95)
        - Endurance: Drain très faible (0.7)
        - Le plus rapide, idéal pour sprints
        """
        return TerrainData(
            terrain_type=TerrainType.CONCRETE,
            speed_multiplier=1.1,
            stamina_drain_multiplier=0.7,
            grip_level=0.95,
            drag_modifier=-0.005,  # Bonus de vitesse!
            color=(120, 120, 120),  # Gris clair
            name="Béton"
        )

    @classmethod
    def get_all_terrain_types(cls) -> list[TerrainType]:
        """
        Retourne la liste de tous les types de terrain disponibles.

        Returns:
            Liste des TerrainType
        """
        return list(TerrainType)

    @classmethod
    def clear_cache(cls) -> None:
        """Vide le cache des terrains (utile pour tests)."""
        cls._terrain_registry.clear()
