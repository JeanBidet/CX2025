"""
Données de terrain - Structures de données pour les types de terrain.

Définit les propriétés physiques et visuelles de chaque type de terrain
utilisé dans le jeu de cyclo-cross.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple


class TerrainType(Enum):
    """Types de terrain disponibles dans le jeu."""
    ASPHALT = auto()    # Asphalte - rapide, bonne adhérence
    GRASS = auto()      # Herbe - moyen, adhérence moyenne
    SAND = auto()       # Sable - lent, faible adhérence
    MUD = auto()        # Boue - très lent, très faible adhérence
    GRAVEL = auto()     # Gravier - moyen-rapide, adhérence variable
    DIRT = auto()       # Terre battue - moyen
    CONCRETE = auto()   # Béton - très rapide


@dataclass(frozen=True)
class TerrainData:
    """
    Données définissant les propriétés d'un type de terrain.

    Attributs:
        terrain_type: Type de terrain
        speed_multiplier: Multiplicateur de vitesse max (0.0-2.0)
        stamina_drain_multiplier: Multiplicateur de drain d'endurance
        grip_level: Niveau d'adhérence (0.0-1.0)
        drag_modifier: Modificateur de traînée additionnelle
        color: Couleur RGB pour le rendu
        name: Nom lisible du terrain
        slope: Angle de pente en degrés (pour futurs ajouts)
        camber: Dévers latéral (pour futurs ajouts)
    """

    terrain_type: TerrainType
    speed_multiplier: float
    stamina_drain_multiplier: float
    grip_level: float
    drag_modifier: float
    color: Tuple[int, int, int]
    name: str
    slope: float = 0.0
    camber: float = 0.0

    def __post_init__(self) -> None:
        """Valide les données après initialisation."""
        if not 0.0 <= self.speed_multiplier <= 2.0:
            raise ValueError(f"speed_multiplier doit être entre 0.0 et 2.0, reçu {self.speed_multiplier}")
        if not 0.0 <= self.grip_level <= 1.0:
            raise ValueError(f"grip_level doit être entre 0.0 et 1.0, reçu {self.grip_level}")
        if self.stamina_drain_multiplier < 0.0:
            raise ValueError(f"stamina_drain_multiplier doit être >= 0.0, reçu {self.stamina_drain_multiplier}")
