"""
Interface Command - Définit le contrat pour toutes les commandes du jeu.

Le Command Pattern transforme des requêtes en objets, permettant de
paramétrer, mettre en file d'attente, logger et supporter undo/redo.
"""

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity


class ICommand(Protocol):
    """
    Interface pour toutes les commandes du jeu.

    Utilise typing.Protocol pour définir un contrat sans héritage explicite,
    permettant le duck typing statique en Python.
    """

    @property
    def name(self) -> str:
        """Retourne le nom de la commande pour identification."""
        ...

    @property
    def priority(self) -> int:
        """
        Retourne la priorité de la commande.

        Les priorités plus élevées sont exécutées en premier.
        Utile pour résoudre les conflits entre commandes.
        """
        ...

    def execute(self, entity: "Entity", delta_time: float) -> None:
        """
        Exécute la commande sur une entité.

        Args:
            entity: L'entité cible de la commande
            delta_time: Temps écoulé depuis la dernière frame (secondes)
        """
        ...

    def can_execute(self, entity: "Entity") -> bool:
        """
        Vérifie si la commande peut être exécutée sur cette entité.

        Args:
            entity: L'entité à vérifier

        Returns:
            True si la commande peut s'exécuter, False sinon
        """
        ...


class IUndoableCommand(ICommand, Protocol):
    """
    Interface pour les commandes supportant undo.

    Étend ICommand pour ajouter la capacité d'annuler une commande.
    Utile pour replay, debug et fonctionnalités avancées.
    """

    def undo(self) -> None:
        """Annule l'effet de la dernière exécution de la commande."""
        ...


class BaseCommand:
    """
    Classe de base pour implémenter des commandes.

    Fournit une implémentation par défaut de l'interface ICommand.
    Les commandes concrètes peuvent hériter de cette classe.
    """

    def __init__(self, name: str, priority: int = 0) -> None:
        """
        Initialise une commande de base.

        Args:
            name: Nom de la commande
            priority: Priorité d'exécution (défaut: 0)
        """
        self._name: str = name
        self._priority: int = priority

    @property
    def name(self) -> str:
        """Retourne le nom de la commande."""
        return self._name

    @property
    def priority(self) -> int:
        """Retourne la priorité de la commande."""
        return self._priority

    def execute(self, entity: "Entity", delta_time: float) -> None:
        """
        Exécute la commande (à implémenter dans les sous-classes).

        Args:
            entity: L'entité cible
            delta_time: Temps écoulé
        """
        raise NotImplementedError(
            f"La commande {self._name} doit implémenter execute()"
        )

    def can_execute(self, entity: "Entity") -> bool:
        """
        Vérifie si la commande peut s'exécuter.

        Par défaut, retourne True. Peut être surchargé.

        Args:
            entity: L'entité à vérifier

        Returns:
            True par défaut
        """
        return True

    def __repr__(self) -> str:
        """Représentation string de la commande."""
        return f"{self.__class__.__name__}(name={self._name}, priority={self._priority})"
