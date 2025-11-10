"""
Animation System - Système de gestion d'animations frame-by-frame.

Gère les animations sprite-based pour les entités du jeu.
"""

from typing import Optional
import pygame


class Animation:
    """
    Gère une animation basée sur une séquence de frames (surfaces Pygame).

    Permet de jouer des animations frame-by-frame avec contrôle de la vitesse,
    support pour boucles infinies ou animations one-shot.
    """

    def __init__(
        self,
        frames: list[pygame.Surface],
        frame_duration: float = 0.1,
        loop: bool = True
    ) -> None:
        """
        Initialise une animation.

        Args:
            frames: Liste des surfaces Pygame représentant chaque frame
            frame_duration: Durée d'une frame en secondes
            loop: Si True, l'animation boucle, sinon s'arrête à la dernière frame
        """
        if not frames:
            raise ValueError("L'animation doit avoir au moins une frame")

        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop

        self._current_frame_index: int = 0
        self._elapsed_time: float = 0.0
        self._finished: bool = False

    def update(self, delta_time: float) -> None:
        """
        Met à jour l'animation.

        Args:
            delta_time: Temps écoulé depuis la dernière frame
        """
        if self._finished and not self.loop:
            return

        self._elapsed_time += delta_time

        # Passe à la frame suivante si nécessaire
        while self._elapsed_time >= self.frame_duration:
            self._elapsed_time -= self.frame_duration
            self._current_frame_index += 1

            # Gestion de la fin de l'animation
            if self._current_frame_index >= len(self.frames):
                if self.loop:
                    self._current_frame_index = 0
                else:
                    self._current_frame_index = len(self.frames) - 1
                    self._finished = True
                    break

    def get_current_frame(self) -> pygame.Surface:
        """
        Retourne la frame actuelle de l'animation.

        Returns:
            Surface Pygame de la frame actuelle
        """
        return self.frames[self._current_frame_index]

    def reset(self) -> None:
        """Réinitialise l'animation au début."""
        self._current_frame_index = 0
        self._elapsed_time = 0.0
        self._finished = False

    def is_finished(self) -> bool:
        """
        Vérifie si l'animation est terminée.

        Returns:
            True si l'animation est finie (seulement pour animations non-loop)
        """
        return self._finished

    def get_frame_count(self) -> int:
        """
        Retourne le nombre total de frames.

        Returns:
            Nombre de frames dans l'animation
        """
        return len(self.frames)

    def set_frame(self, frame_index: int) -> None:
        """
        Définit manuellement la frame actuelle.

        Args:
            frame_index: Index de la frame (clamped aux limites)
        """
        self._current_frame_index = max(0, min(frame_index, len(self.frames) - 1))
        self._elapsed_time = 0.0

    def __repr__(self) -> str:
        """Représentation string de l'animation."""
        return (
            f"Animation(frames={len(self.frames)}, "
            f"duration={self.frame_duration:.2f}s, "
            f"loop={self.loop}, "
            f"current={self._current_frame_index})"
        )


class AnimationController:
    """
    Contrôleur gérant plusieurs animations et permettant de basculer entre elles.

    Utile pour gérer toutes les animations d'une entité (marche, course, idle, etc.)
    """

    def __init__(self) -> None:
        """Initialise le contrôleur d'animations."""
        self._animations: dict[str, Animation] = {}
        self._current_animation_name: Optional[str] = None

    def add_animation(self, name: str, animation: Animation) -> None:
        """
        Ajoute une animation au contrôleur.

        Args:
            name: Nom de l'animation (ex: "walk", "run", "idle")
            animation: Instance d'Animation
        """
        self._animations[name] = animation

    def play(self, name: str, reset: bool = True) -> None:
        """
        Joue une animation.

        Args:
            name: Nom de l'animation à jouer
            reset: Si True, réinitialise l'animation au début

        Raises:
            KeyError: Si l'animation n'existe pas
        """
        if name not in self._animations:
            raise KeyError(f"Animation '{name}' n'existe pas")

        # Si on change d'animation ou si reset est demandé
        if self._current_animation_name != name or reset:
            self._current_animation_name = name
            if reset:
                self._animations[name].reset()

    def update(self, delta_time: float) -> None:
        """
        Met à jour l'animation actuelle.

        Args:
            delta_time: Temps écoulé depuis la dernière frame
        """
        if self._current_animation_name:
            animation = self._animations[self._current_animation_name]
            animation.update(delta_time)

    def get_current_frame(self) -> Optional[pygame.Surface]:
        """
        Retourne la frame actuelle de l'animation en cours.

        Returns:
            Surface Pygame ou None si aucune animation active
        """
        if self._current_animation_name:
            return self._animations[self._current_animation_name].get_current_frame()
        return None

    def get_current_animation_name(self) -> Optional[str]:
        """
        Retourne le nom de l'animation actuelle.

        Returns:
            Nom de l'animation ou None
        """
        return self._current_animation_name

    def has_animation(self, name: str) -> bool:
        """
        Vérifie si une animation existe.

        Args:
            name: Nom de l'animation

        Returns:
            True si l'animation existe
        """
        return name in self._animations

    def is_current_animation_finished(self) -> bool:
        """
        Vérifie si l'animation actuelle est terminée.

        Returns:
            True si l'animation est finie (pour animations non-loop)
        """
        if self._current_animation_name:
            return self._animations[self._current_animation_name].is_finished()
        return False

    def __repr__(self) -> str:
        """Représentation string du contrôleur."""
        return (
            f"AnimationController(animations={len(self._animations)}, "
            f"current={self._current_animation_name})"
        )
