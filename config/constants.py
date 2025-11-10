"""
Constantes globales du jeu.

Ce fichier contient les constantes qui ne changent jamais durant l'exécution
du jeu, comme les états, les codes de couleur, etc.
"""

from enum import Enum, auto
from typing import Tuple


class GameState(Enum):
    """États possibles du jeu."""
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    RESULTS = auto()


class SceneType(Enum):
    """Types de scènes disponibles."""
    MENU = auto()
    RACE = auto()
    RESULTS = auto()
    TEST = auto()


class PerformanceZone(Enum):
    """Zones de performance selon le niveau d'endurance du cycliste."""
    OPTIMAL = auto()     # 70-100% endurance : performance normale
    MODERATE = auto()    # 40-70% endurance : -10% vitesse max
    CRITICAL = auto()    # 10-40% endurance : -30% vitesse, contrôle réduit
    EXHAUSTED = auto()   # 0-10% endurance : -50% vitesse, risque de chute


# Couleurs communes (RGB)
class Colors:
    """Couleurs utilisées dans le jeu."""
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    RED: Tuple[int, int, int] = (255, 0, 0)
    GREEN: Tuple[int, int, int] = (0, 255, 0)
    BLUE: Tuple[int, int, int] = (0, 0, 255)
    YELLOW: Tuple[int, int, int] = (255, 255, 0)
    CYAN: Tuple[int, int, int] = (0, 255, 255)
    MAGENTA: Tuple[int, int, int] = (255, 0, 255)
    GRAY: Tuple[int, int, int] = (128, 128, 128)
    DARK_GRAY: Tuple[int, int, int] = (64, 64, 64)
    LIGHT_GRAY: Tuple[int, int, int] = (192, 192, 192)

    # Couleurs thématiques cyclo-cross
    GRASS_GREEN: Tuple[int, int, int] = (34, 139, 34)
    MUD_BROWN: Tuple[int, int, int] = (101, 67, 33)
    SAND_YELLOW: Tuple[int, int, int] = (194, 178, 128)
    TRACK_GRAY: Tuple[int, int, int] = (96, 96, 96)


# Touches de contrôle (pour référence future)
class InputKeys:
    """Touches de contrôle par défaut."""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    SPACE = "space"
    ESCAPE = "escape"
    ENTER = "return"


# Layers de rendu (pour l'ordre d'affichage)
class RenderLayer(Enum):
    """Ordre des couches de rendu."""
    BACKGROUND = 0
    TERRAIN = 10
    OBSTACLES = 20
    RIDERS = 30
    EFFECTS = 40
    UI = 50
    DEBUG = 100
