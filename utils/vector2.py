"""
Classe Vector2 pour représenter les positions, vitesses et directions en 2D.

Cette classe fournit toutes les opérations mathématiques nécessaires pour
manipuler des vecteurs 2D dans le contexte du jeu.
"""

from __future__ import annotations
import math
from typing import Union


class Vector2:
    """Représente un vecteur 2D avec toutes les opérations mathématiques nécessaires."""

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        """
        Initialise un vecteur 2D.

        Args:
            x: Composante x du vecteur
            y: Composante y du vecteur
        """
        self.x: float = x
        self.y: float = y

    def __add__(self, other: Vector2) -> Vector2:
        """Addition de deux vecteurs."""
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2) -> Vector2:
        """Soustraction de deux vecteurs."""
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: Union[float, int]) -> Vector2:
        """Multiplication par un scalaire."""
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: Union[float, int]) -> Vector2:
        """Division par un scalaire."""
        if scalar == 0:
            raise ValueError("Division par zéro impossible")
        return Vector2(self.x / scalar, self.y / scalar)

    def __rmul__(self, scalar: Union[float, int]) -> Vector2:
        """Multiplication par un scalaire (ordre inversé)."""
        return self.__mul__(scalar)

    def __neg__(self) -> Vector2:
        """Négation du vecteur."""
        return Vector2(-self.x, -self.y)

    def __eq__(self, other: object) -> bool:
        """Comparaison d'égalité entre deux vecteurs."""
        if not isinstance(other, Vector2):
            return False
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __repr__(self) -> str:
        """Représentation string du vecteur."""
        return f"Vector2({self.x:.2f}, {self.y:.2f})"

    def length(self) -> float:
        """
        Calcule la longueur (magnitude) du vecteur.

        Returns:
            La longueur du vecteur
        """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def length_squared(self) -> float:
        """
        Calcule la longueur au carré du vecteur.
        Utile pour les comparaisons de distance sans calcul de racine carrée.

        Returns:
            La longueur au carré du vecteur
        """
        return self.x * self.x + self.y * self.y

    def normalize(self) -> Vector2:
        """
        Retourne un vecteur normalisé (longueur = 1).

        Returns:
            Un nouveau vecteur normalisé

        Raises:
            ValueError: Si le vecteur est nul
        """
        length = self.length()
        if length == 0:
            raise ValueError("Impossible de normaliser un vecteur nul")
        return Vector2(self.x / length, self.y / length)

    def normalized(self) -> Vector2:
        """
        Alias pour normalize() pour plus de clarté.

        Returns:
            Un nouveau vecteur normalisé
        """
        return self.normalize()

    def dot(self, other: Vector2) -> float:
        """
        Calcule le produit scalaire avec un autre vecteur.

        Args:
            other: L'autre vecteur

        Returns:
            Le produit scalaire
        """
        return self.x * other.x + self.y * other.y

    def cross(self, other: Vector2) -> float:
        """
        Calcule le produit vectoriel en 2D (retourne un scalaire).

        Args:
            other: L'autre vecteur

        Returns:
            Le produit vectoriel (composante z)
        """
        return self.x * other.y - self.y * other.x

    def distance_to(self, other: Vector2) -> float:
        """
        Calcule la distance jusqu'à un autre vecteur.

        Args:
            other: L'autre vecteur

        Returns:
            La distance entre les deux vecteurs
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def distance_squared_to(self, other: Vector2) -> float:
        """
        Calcule la distance au carré jusqu'à un autre vecteur.
        Utile pour les comparaisons sans calcul de racine carrée.

        Args:
            other: L'autre vecteur

        Returns:
            La distance au carré entre les deux vecteurs
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy

    def rotate(self, angle: float) -> Vector2:
        """
        Retourne un nouveau vecteur tourné d'un angle donné (en radians).

        Args:
            angle: L'angle de rotation en radians

        Returns:
            Un nouveau vecteur tourné
        """
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )

    def angle(self) -> float:
        """
        Retourne l'angle du vecteur par rapport à l'axe X (en radians).

        Returns:
            L'angle en radians
        """
        return math.atan2(self.y, self.x)

    def angle_to(self, other: Vector2) -> float:
        """
        Calcule l'angle entre ce vecteur et un autre (en radians).

        Args:
            other: L'autre vecteur

        Returns:
            L'angle entre les deux vecteurs en radians
        """
        return math.atan2(other.y - self.y, other.x - self.x)

    def lerp(self, other: Vector2, t: float) -> Vector2:
        """
        Interpolation linéaire entre ce vecteur et un autre.

        Args:
            other: Le vecteur cible
            t: Le facteur d'interpolation (0.0 à 1.0)

        Returns:
            Un nouveau vecteur interpolé
        """
        return Vector2(
            self.x + (other.x - self.x) * t,
            self.y + (other.y - self.y) * t
        )

    def copy(self) -> Vector2:
        """
        Crée une copie du vecteur.

        Returns:
            Une nouvelle instance de Vector2 avec les mêmes valeurs
        """
        return Vector2(self.x, self.y)

    @staticmethod
    def zero() -> Vector2:
        """Retourne un vecteur nul (0, 0)."""
        return Vector2(0.0, 0.0)

    @staticmethod
    def one() -> Vector2:
        """Retourne un vecteur (1, 1)."""
        return Vector2(1.0, 1.0)

    @staticmethod
    def up() -> Vector2:
        """Retourne un vecteur pointant vers le haut (0, -1)."""
        return Vector2(0.0, -1.0)

    @staticmethod
    def down() -> Vector2:
        """Retourne un vecteur pointant vers le bas (0, 1)."""
        return Vector2(0.0, 1.0)

    @staticmethod
    def left() -> Vector2:
        """Retourne un vecteur pointant vers la gauche (-1, 0)."""
        return Vector2(-1.0, 0.0)

    @staticmethod
    def right() -> Vector2:
        """Retourne un vecteur pointant vers la droite (1, 0)."""
        return Vector2(1.0, 0.0)

    def to_tuple(self) -> tuple[float, float]:
        """
        Convertit le vecteur en tuple.

        Returns:
            Un tuple (x, y)
        """
        return (self.x, self.y)

    def to_int_tuple(self) -> tuple[int, int]:
        """
        Convertit le vecteur en tuple d'entiers.
        Utile pour les positions de pixels.

        Returns:
            Un tuple (int(x), int(y))
        """
        return (int(self.x), int(self.y))
