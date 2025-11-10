"""
Interface IComponent définissant le contrat que tous les composants doivent respecter.

Le pattern Component permet d'attacher des comportements aux entités de manière
modulaire et dynamique, favorisant la composition sur l'héritage.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity


class IComponent(ABC):
    """
    Interface de base pour tous les composants du jeu.

    Les composants représentent des comportements ou des données qui peuvent
    être attachés aux entités. Chaque composant ne connaît que l'entité
    à laquelle il est attaché.
    """

    def __init__(self, owner: "Entity") -> None:
        """
        Initialise le composant.

        Args:
            owner: L'entité propriétaire de ce composant
        """
        self._owner: "Entity" = owner
        self._enabled: bool = True

    @property
    def owner(self) -> "Entity":
        """Retourne l'entité propriétaire de ce composant."""
        return self._owner

    @property
    def enabled(self) -> bool:
        """Indique si le composant est actif."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Active ou désactive le composant."""
        self._enabled = value

    @abstractmethod
    def init(self) -> None:
        """
        Initialise le composant après qu'il ait été attaché à une entité.
        Appelé automatiquement par l'entité lors de l'ajout du composant.
        """
        pass

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """
        Met à jour le composant.

        Args:
            delta_time: Temps écoulé depuis la dernière frame en secondes
        """
        pass

    @abstractmethod
    def destroy(self) -> None:
        """
        Nettoie les ressources du composant avant sa destruction.
        Appelé automatiquement lors du retrait du composant.
        """
        pass

    def __repr__(self) -> str:
        """Représentation string du composant."""
        return f"{self.__class__.__name__}(owner={self._owner})"
