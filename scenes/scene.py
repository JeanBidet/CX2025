"""
Classe de base Scene pour toutes les scènes du jeu.

Une scène représente un état du jeu (menu, course, résultats, etc.) avec
son propre cycle de vie et sa propre logique.
"""

from abc import ABC, abstractmethod
from typing import Optional
import pygame
from systems.entity_manager import EntityManager


class Scene(ABC):
    """
    Classe abstraite de base pour toutes les scènes.

    Chaque scène a son propre cycle de vie : enter, exit, update, render.
    """

    def __init__(self, name: str) -> None:
        """
        Initialise une scène.

        Args:
            name: Nom de la scène
        """
        self._name: str = name
        self._entity_manager: EntityManager = EntityManager()
        self._next_scene: Optional[str] = None
        self._scene_data: dict = {}

    @property
    def name(self) -> str:
        """Retourne le nom de la scène."""
        return self._name

    @property
    def entity_manager(self) -> EntityManager:
        """Retourne l'Entity Manager de la scène."""
        return self._entity_manager

    @property
    def next_scene(self) -> Optional[str]:
        """Retourne le nom de la prochaine scène à charger."""
        return self._next_scene

    @property
    def scene_data(self) -> dict:
        """Retourne les données partagées de la scène."""
        return self._scene_data

    def set_next_scene(self, scene_name: str, data: Optional[dict] = None) -> None:
        """
        Définit la prochaine scène à charger.

        Args:
            scene_name: Nom de la scène à charger
            data: Données optionnelles à transmettre à la prochaine scène
        """
        self._next_scene = scene_name
        if data:
            self._scene_data = data

    @abstractmethod
    def enter(self, data: Optional[dict] = None) -> None:
        """
        Appelé lorsque la scène devient active.

        Args:
            data: Données optionnelles transmises par la scène précédente
        """
        pass

    @abstractmethod
    def exit(self) -> None:
        """Appelé lorsque la scène devient inactive."""
        pass

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Gère les événements Pygame.

        Args:
            events: Liste des événements à traiter
        """
        pass

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """
        Met à jour la logique de la scène.

        Args:
            delta_time: Temps écoulé depuis la dernière frame en secondes
        """
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """
        Effectue le rendu de la scène.

        Args:
            screen: Surface Pygame sur laquelle dessiner
        """
        pass

    def __repr__(self) -> str:
        """Représentation string de la scène."""
        return f"Scene(name={self._name})"
