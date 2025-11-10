"""
Transform Component - Gestion de la position, rotation et échelle d'une entité.

Ce composant est responsable de la transformation spatiale d'une entité
dans l'espace 2D du jeu.
"""

import math
from components.icomponent import IComponent
from utils.vector2 import Vector2


class TransformComponent(IComponent):
    """
    Composant gérant la position, rotation et échelle d'une entité.

    Ce composant centralise toutes les transformations spatiales et fournit
    des méthodes utilitaires pour manipuler la position et l'orientation.
    """

    def __init__(self, owner, position: Vector2 | None = None) -> None:
        """
        Initialise le composant de transformation.

        Args:
            owner: L'entité propriétaire
            position: Position initiale (optionnel, par défaut Vector2.zero())
        """
        super().__init__(owner)
        self._position: Vector2 = position if position else Vector2.zero()
        self._rotation: float = 0.0  # Angle en radians
        self._scale: Vector2 = Vector2.one()

    @property
    def position(self) -> Vector2:
        """Retourne la position de l'entité."""
        return self._position

    @position.setter
    def position(self, value: Vector2) -> None:
        """Définit la position de l'entité."""
        self._position = value

    @property
    def rotation(self) -> float:
        """Retourne la rotation en radians."""
        return self._rotation

    @rotation.setter
    def rotation(self, value: float) -> None:
        """Définit la rotation en radians."""
        # Normalise l'angle entre -π et π
        self._rotation = math.atan2(math.sin(value), math.cos(value))

    @property
    def rotation_degrees(self) -> float:
        """Retourne la rotation en degrés."""
        return math.degrees(self._rotation)

    @rotation_degrees.setter
    def rotation_degrees(self, value: float) -> None:
        """Définit la rotation en degrés."""
        self._rotation = math.radians(value)

    @property
    def scale(self) -> Vector2:
        """Retourne l'échelle de l'entité."""
        return self._scale

    @scale.setter
    def scale(self, value: Vector2) -> None:
        """Définit l'échelle de l'entité."""
        self._scale = value

    def init(self) -> None:
        """Initialise le composant."""
        # Synchronise avec la position de l'entité si elle en a une
        if hasattr(self.owner, '_position'):
            self._position = self.owner.position.copy()

    def update(self, delta_time: float) -> None:
        """
        Met à jour le composant.

        Args:
            delta_time: Temps écoulé depuis la dernière frame
        """
        # Synchronise la position avec l'entité propriétaire
        self.owner.position = self._position.copy()
        self.owner.rotation = self._rotation

    def translate(self, delta: Vector2) -> None:
        """
        Déplace l'entité d'un vecteur delta.

        Args:
            delta: Vecteur de déplacement
        """
        self._position = self._position + delta

    def rotate(self, angle: float) -> None:
        """
        Tourne l'entité d'un angle donné.

        Args:
            angle: Angle de rotation en radians
        """
        self.rotation = self._rotation + angle

    def rotate_degrees(self, angle: float) -> None:
        """
        Tourne l'entité d'un angle donné en degrés.

        Args:
            angle: Angle de rotation en degrés
        """
        self.rotate(math.radians(angle))

    def look_at(self, target: Vector2) -> None:
        """
        Oriente l'entité vers une position cible.

        Args:
            target: Position cible à regarder
        """
        direction = target - self._position
        if direction.length() > 0:
            self._rotation = direction.angle()

    def look_in_direction(self, direction: Vector2) -> None:
        """
        Oriente l'entité dans une direction donnée.

        Args:
            direction: Direction à regarder (sera normalisée)
        """
        if direction.length() > 0:
            self._rotation = direction.angle()

    def get_forward_vector(self) -> Vector2:
        """
        Retourne le vecteur avant de l'entité basé sur sa rotation.

        Returns:
            Vecteur unitaire pointant vers l'avant
        """
        return Vector2(math.cos(self._rotation), math.sin(self._rotation))

    def get_right_vector(self) -> Vector2:
        """
        Retourne le vecteur droit de l'entité basé sur sa rotation.

        Returns:
            Vecteur unitaire pointant vers la droite
        """
        return Vector2(
            math.cos(self._rotation + math.pi / 2),
            math.sin(self._rotation + math.pi / 2)
        )

    def local_to_world(self, local_pos: Vector2) -> Vector2:
        """
        Convertit une position locale en position monde.

        Args:
            local_pos: Position en espace local

        Returns:
            Position en espace monde
        """
        # Applique rotation puis translation
        rotated = local_pos.rotate(self._rotation)
        scaled = Vector2(rotated.x * self._scale.x, rotated.y * self._scale.y)
        return self._position + scaled

    def world_to_local(self, world_pos: Vector2) -> Vector2:
        """
        Convertit une position monde en position locale.

        Args:
            world_pos: Position en espace monde

        Returns:
            Position en espace local
        """
        # Translation inverse puis rotation inverse
        translated = world_pos - self._position
        unscaled = Vector2(translated.x / self._scale.x, translated.y / self._scale.y)
        return unscaled.rotate(-self._rotation)

    def destroy(self) -> None:
        """Nettoie les ressources du composant."""
        pass

    def __repr__(self) -> str:
        """Représentation string du composant."""
        return (
            f"TransformComponent(pos={self._position}, "
            f"rot={self.rotation_degrees:.1f}°, scale={self._scale})"
        )
