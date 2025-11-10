"""
Scene Manager - Gestionnaire de scènes du jeu.

Le Scene Manager gère les transitions entre les différentes scènes du jeu
et s'assure que seule une scène est active à la fois.
"""

from typing import Dict, Optional
import pygame
from scenes.scene import Scene


class SceneManager:
    """
    Gestionnaire de scènes implémentant le pattern Singleton.

    Gère le cycle de vie des scènes et les transitions entre elles.
    """

    _instance: Optional["SceneManager"] = None

    def __new__(cls) -> "SceneManager":
        """Implémente le pattern Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialise le Scene Manager."""
        if self._initialized:
            return

        self._scenes: Dict[str, Scene] = {}
        self._current_scene: Optional[Scene] = None
        self._initialized = True

    def register_scene(self, scene_name: str, scene: Scene) -> None:
        """
        Enregistre une nouvelle scène.

        Args:
            scene_name: Nom unique de la scène
            scene: Instance de la scène

        Raises:
            ValueError: Si une scène avec ce nom existe déjà
        """
        if scene_name in self._scenes:
            raise ValueError(f"Une scène nommée '{scene_name}' existe déjà")

        self._scenes[scene_name] = scene

    def change_scene(self, scene_name: str, data: Optional[dict] = None) -> None:
        """
        Change la scène active.

        Args:
            scene_name: Nom de la scène à activer
            data: Données optionnelles à transmettre à la nouvelle scène

        Raises:
            ValueError: Si la scène demandée n'existe pas
        """
        if scene_name not in self._scenes:
            raise ValueError(f"La scène '{scene_name}' n'est pas enregistrée")

        # Sort de la scène actuelle
        if self._current_scene is not None:
            self._current_scene.exit()

        # Entre dans la nouvelle scène
        self._current_scene = self._scenes[scene_name]
        self._current_scene.enter(data)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Transmet les événements à la scène active.

        Args:
            events: Liste des événements Pygame
        """
        if self._current_scene is not None:
            self._current_scene.handle_events(events)

    def update(self, delta_time: float) -> None:
        """
        Met à jour la scène active.

        Args:
            delta_time: Temps écoulé depuis la dernière frame en secondes
        """
        if self._current_scene is not None:
            self._current_scene.update(delta_time)

            # Vérifie s'il y a une transition de scène demandée
            if self._current_scene.next_scene is not None:
                next_scene_name = self._current_scene.next_scene
                scene_data = self._current_scene.scene_data
                self.change_scene(next_scene_name, scene_data)

    def render(self, screen: pygame.Surface) -> None:
        """
        Effectue le rendu de la scène active.

        Args:
            screen: Surface Pygame sur laquelle dessiner
        """
        if self._current_scene is not None:
            self._current_scene.render(screen)

    @property
    def current_scene(self) -> Optional[Scene]:
        """Retourne la scène actuellement active."""
        return self._current_scene

    @property
    def current_scene_name(self) -> Optional[str]:
        """Retourne le nom de la scène actuellement active."""
        return self._current_scene.name if self._current_scene else None

    def has_scene(self, scene_name: str) -> bool:
        """
        Vérifie si une scène est enregistrée.

        Args:
            scene_name: Nom de la scène

        Returns:
            True si la scène existe, False sinon
        """
        return scene_name in self._scenes

    @classmethod
    def reset_instance(cls) -> None:
        """Réinitialise l'instance du Singleton (utile pour les tests)."""
        if cls._instance is not None:
            cls._instance._scenes.clear()
            cls._instance._current_scene = None
            cls._instance = None

    def __repr__(self) -> str:
        """Représentation string du Scene Manager."""
        scene_count = len(self._scenes)
        current = self.current_scene_name or "None"
        return f"SceneManager(scenes={scene_count}, current={current})"
