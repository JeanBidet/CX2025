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

    # Paramètres d'endurance (Stamina)
    STAMINA_MAX: float = 100.0  # Endurance maximale
    STAMINA_BASE_DRAIN_RATE: float = 2.0  # Drain de base par seconde (au repos)
    STAMINA_RECOVERY_RATE: float = 8.0  # Récupération par seconde en mode portage
    STAMINA_VELOCITY_MULTIPLIER: float = 0.015  # Facteur de drain basé sur la vitesse
    STAMINA_SLOPE_MULTIPLIER: float = 2.5  # Multiplicateur pour les montées
    STAMINA_FATIGUE_RECOVERY_PENALTY: float = 0.7  # Réduction récupération par fatigue

    # Seuils des zones de performance (pourcentages de stamina)
    STAMINA_OPTIMAL_THRESHOLD: float = 70.0  # Au-dessus : zone OPTIMAL
    STAMINA_MODERATE_THRESHOLD: float = 40.0  # Au-dessus : zone MODERATE
    STAMINA_CRITICAL_THRESHOLD: float = 10.0  # Au-dessus : zone CRITICAL, en dessous : EXHAUSTED

    # Modificateurs de performance par zone
    PERFORMANCE_OPTIMAL_SPEED_MULT: float = 1.0  # Vitesse normale
    PERFORMANCE_MODERATE_SPEED_MULT: float = 0.9  # -10% vitesse
    PERFORMANCE_CRITICAL_SPEED_MULT: float = 0.7  # -30% vitesse
    PERFORMANCE_EXHAUSTED_SPEED_MULT: float = 0.5  # -50% vitesse

    # Paramètres d'équilibre (Balance)
    BALANCE_MAX: float = 100.0  # Équilibre maximal (totalement stable)
    BALANCE_RECOVERY_RATE: float = 25.0  # Récupération par seconde en conditions optimales
    BALANCE_CRITICAL_THRESHOLD: float = 20.0  # En dessous : risque de chute
    BALANCE_CRASH_THRESHOLD: float = 5.0  # En dessous : chute garantie

    # Facteurs d'instabilité
    BALANCE_CAMBER_MULTIPLIER: float = 1.5  # Impact de l'inclinaison latérale
    BALANCE_SPEED_MULTIPLIER: float = 0.8  # Impact de la vitesse sur l'instabilité
    BALANCE_LOW_STAMINA_MULTIPLIER: float = 1.8  # Plus d'instabilité si épuisé
    BALANCE_TERRAIN_GRIP_FACTOR: float = 2.0  # Multiplicateur basé sur le grip

    # Paramètres de fatigue cumulative
    FATIGUE_ACCUMULATION_RATE: float = 0.5  # Taux d'accumulation par seconde d'effort
    FATIGUE_MAX: float = 100.0  # Fatigue maximale
    FATIGUE_RECOVERY_IN_CARRYING: float = 2.0  # Récupération de fatigue en portage

    @classmethod
    def get_window_size(cls) -> Tuple[int, int]:
        """Retourne la taille de la fenêtre."""
        return (cls.WINDOW_WIDTH, cls.WINDOW_HEIGHT)

    @classmethod
    def get_window_center(cls) -> Tuple[int, int]:
        """Retourne le centre de la fenêtre."""
        return (cls.WINDOW_WIDTH // 2, cls.WINDOW_HEIGHT // 2)
