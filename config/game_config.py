"""
Configuration du jeu - Paramètres centralisés pour le jeu de cyclo-cross.

Ce fichier contient tous les paramètres configurables du jeu, permettant
un ajustement facile sans modifier le code métier.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class GameConfig:
    """Configuration principale du jeu."""

    # Configuration de la fenêtre
    WINDOW_WIDTH: int = 1280
    WINDOW_HEIGHT: int = 720
    WINDOW_TITLE: str = "Cyclo-Cross Racing Game"
    FULLSCREEN: bool = False

    # Configuration du jeu
    TARGET_FPS: int = 60
    DELTA_TIME_MAX: float = 0.1  # Maximum delta time pour éviter les gros sauts

    # Configuration du rendu
    BACKGROUND_COLOR: Tuple[int, int, int] = (34, 139, 34)  # Vert gazon
    SHOW_FPS: bool = True
    SHOW_DEBUG_INFO: bool = True

    # Configuration du joueur (pour les prompts futurs)
    PLAYER_SPEED: float = 200.0  # pixels par seconde
    PLAYER_SIZE: int = 20

    # Configuration physique (Prompt 2)
    GRAVITY: float = 9.81  # Gravité (m/s²) - pour sauts futurs
    FRICTION: float = 0.95

    # Paramètres physiques du cycliste
    CYCLIST_MASS: float = 70.0  # Masse cycliste + vélo (kg)
    CYCLIST_DRAG: float = 0.985  # Coefficient de traînée (0-1, plus proche de 1 = moins de résistance)
    CYCLIST_MAX_SPEED: float = 450.0  # Vitesse max (pixels/seconde)

    # Paramètres de contrôle
    CYCLIST_ACCELERATION_FORCE: float = 50000.0  # Force d'accélération (N)
    CYCLIST_BRAKE_FORCE: float = 30000.0  # Force de freinage (N)
    CYCLIST_TURN_SPEED_SLOW: float = 4.0  # Rotation à basse vitesse (rad/s)
    CYCLIST_TURN_SPEED_FAST: float = 1.5  # Rotation à haute vitesse (rad/s)
    CYCLIST_SPEED_THRESHOLD: float = 200.0  # Seuil vitesse pour rotation (px/s)

    @classmethod
    def get_window_size(cls) -> Tuple[int, int]:
        """Retourne la taille de la fenêtre."""
        return (cls.WINDOW_WIDTH, cls.WINDOW_HEIGHT)

    @classmethod
    def get_window_center(cls) -> Tuple[int, int]:
        """Retourne le centre de la fenêtre."""
        return (cls.WINDOW_WIDTH // 2, cls.WINDOW_HEIGHT // 2)
