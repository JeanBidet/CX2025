"""
Configuration des contrôles - Profils de touches pour le jeu.

Ce fichier centralise tous les mappings touches->commandes,
permettant un remapping facile sans modifier le code.
"""

from typing import Dict, Callable
import pygame
from patterns.commands.command import ICommand
from patterns.commands.movement_commands import (
    AccelerateCommand,
    BrakeCommand,
    TurnLeftCommand,
    TurnRightCommand,
    SprintCommand,
    ReverseCommand,
    StopCommand
)
from config.game_config import GameConfig


# Type alias pour améliorer la lisibilité
CommandFactory = Callable[[], ICommand]
KeyBindings = Dict[int, CommandFactory]


class InputProfile:
    """
    Profil de contrôle définissant un ensemble de touches.

    Chaque profil contient des bindings pour touches maintenues et événements ponctuels.
    """

    def __init__(self, name: str) -> None:
        """
        Initialise un profil de contrôle.

        Args:
            name: Nom du profil
        """
        self.name: str = name
        self.key_bindings: KeyBindings = {}
        self.event_bindings: KeyBindings = {}


def create_arrows_profile() -> InputProfile:
    """
    Crée le profil de contrôle avec les flèches directionnelles.

    Returns:
        Profil configuré avec les flèches
    """
    profile = InputProfile("Arrows")

    # Touches maintenues
    profile.key_bindings = {
        pygame.K_UP: lambda: AccelerateCommand(
            force=GameConfig.CYCLIST_ACCELERATION_FORCE
        ),
        pygame.K_DOWN: lambda: BrakeCommand(
            force=GameConfig.CYCLIST_BRAKE_FORCE
        ),
        pygame.K_LEFT: lambda: TurnLeftCommand(
            turn_speed_slow=GameConfig.CYCLIST_TURN_SPEED_SLOW,
            turn_speed_fast=GameConfig.CYCLIST_TURN_SPEED_FAST,
            speed_threshold=GameConfig.CYCLIST_SPEED_THRESHOLD
        ),
        pygame.K_RIGHT: lambda: TurnRightCommand(
            turn_speed_slow=GameConfig.CYCLIST_TURN_SPEED_SLOW,
            turn_speed_fast=GameConfig.CYCLIST_TURN_SPEED_FAST,
            speed_threshold=GameConfig.CYCLIST_SPEED_THRESHOLD
        ),
    }

    # Événements ponctuels
    profile.event_bindings = {
        pygame.K_SPACE: lambda: SprintCommand(boost_multiplier=1.5),
        pygame.K_LSHIFT: lambda: SprintCommand(boost_multiplier=1.5),
    }

    return profile


def create_wasd_profile() -> InputProfile:
    """
    Crée le profil de contrôle WASD.

    Returns:
        Profil configuré avec WASD
    """
    profile = InputProfile("WASD")

    # Touches maintenues
    profile.key_bindings = {
        pygame.K_w: lambda: AccelerateCommand(
            force=GameConfig.CYCLIST_ACCELERATION_FORCE
        ),
        pygame.K_s: lambda: BrakeCommand(
            force=GameConfig.CYCLIST_BRAKE_FORCE
        ),
        pygame.K_a: lambda: TurnLeftCommand(
            turn_speed_slow=GameConfig.CYCLIST_TURN_SPEED_SLOW,
            turn_speed_fast=GameConfig.CYCLIST_TURN_SPEED_FAST,
            speed_threshold=GameConfig.CYCLIST_SPEED_THRESHOLD
        ),
        pygame.K_d: lambda: TurnRightCommand(
            turn_speed_slow=GameConfig.CYCLIST_TURN_SPEED_SLOW,
            turn_speed_fast=GameConfig.CYCLIST_TURN_SPEED_FAST,
            speed_threshold=GameConfig.CYCLIST_SPEED_THRESHOLD
        ),
    }

    # Événements ponctuels
    profile.event_bindings = {
        pygame.K_SPACE: lambda: SprintCommand(boost_multiplier=1.5),
        pygame.K_LSHIFT: lambda: SprintCommand(boost_multiplier=1.5),
    }

    return profile


def create_hybrid_profile() -> InputProfile:
    """
    Crée un profil hybride combinant flèches et WASD.

    Returns:
        Profil configuré avec flèches ET WASD
    """
    profile = InputProfile("Hybrid")

    # Touches maintenues - combine les deux schémas
    profile.key_bindings = {
        # Flèches
        pygame.K_UP: lambda: AccelerateCommand(
            force=GameConfig.CYCLIST_ACCELERATION_FORCE
        ),
        pygame.K_DOWN: lambda: BrakeCommand(
            force=GameConfig.CYCLIST_BRAKE_FORCE
        ),
        pygame.K_LEFT: lambda: TurnLeftCommand(
            turn_speed_slow=GameConfig.CYCLIST_TURN_SPEED_SLOW,
            turn_speed_fast=GameConfig.CYCLIST_TURN_SPEED_FAST,
            speed_threshold=GameConfig.CYCLIST_SPEED_THRESHOLD
        ),
        pygame.K_RIGHT: lambda: TurnRightCommand(
            turn_speed_slow=GameConfig.CYCLIST_TURN_SPEED_SLOW,
            turn_speed_fast=GameConfig.CYCLIST_TURN_SPEED_FAST,
            speed_threshold=GameConfig.CYCLIST_SPEED_THRESHOLD
        ),
        # WASD
        pygame.K_w: lambda: AccelerateCommand(
            force=GameConfig.CYCLIST_ACCELERATION_FORCE
        ),
        pygame.K_s: lambda: BrakeCommand(
            force=GameConfig.CYCLIST_BRAKE_FORCE
        ),
        pygame.K_a: lambda: TurnLeftCommand(
            turn_speed_slow=GameConfig.CYCLIST_TURN_SPEED_SLOW,
            turn_speed_fast=GameConfig.CYCLIST_TURN_SPEED_FAST,
            speed_threshold=GameConfig.CYCLIST_SPEED_THRESHOLD
        ),
        pygame.K_d: lambda: TurnRightCommand(
            turn_speed_slow=GameConfig.CYCLIST_TURN_SPEED_SLOW,
            turn_speed_fast=GameConfig.CYCLIST_TURN_SPEED_FAST,
            speed_threshold=GameConfig.CYCLIST_SPEED_THRESHOLD
        ),
    }

    # Événements ponctuels
    profile.event_bindings = {
        pygame.K_SPACE: lambda: SprintCommand(boost_multiplier=1.5),
        pygame.K_LSHIFT: lambda: SprintCommand(boost_multiplier=1.5),
    }

    return profile


# Profil par défaut
DEFAULT_PROFILE = create_hybrid_profile()


# Dictionnaire des profils disponibles
AVAILABLE_PROFILES: Dict[str, Callable[[], InputProfile]] = {
    "arrows": create_arrows_profile,
    "wasd": create_wasd_profile,
    "hybrid": create_hybrid_profile,
}


def get_profile(profile_name: str = "hybrid") -> InputProfile:
    """
    Récupère un profil de contrôle par son nom.

    Args:
        profile_name: Nom du profil ("arrows", "wasd", "hybrid")

    Returns:
        Le profil de contrôle

    Raises:
        ValueError: Si le profil n'existe pas
    """
    if profile_name not in AVAILABLE_PROFILES:
        raise ValueError(
            f"Profil '{profile_name}' inconnu. "
            f"Profils disponibles: {list(AVAILABLE_PROFILES.keys())}"
        )

    return AVAILABLE_PROFILES[profile_name]()


def list_available_profiles() -> list[str]:
    """
    Liste tous les profils de contrôle disponibles.

    Returns:
        Liste des noms de profils
    """
    return list(AVAILABLE_PROFILES.keys())
