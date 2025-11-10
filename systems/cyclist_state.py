"""
Cyclist State System - Définitions des états du cycliste.

Ce module contient l'enum StateType et le Protocol ICyclistState
pour le State Pattern du cycliste.
"""

from enum import Enum, auto
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.cyclist import Cyclist


class StateType(Enum):
    """
    Énumération des différents états possibles du cycliste.

    États :
    - RIDING : En selle, pédalage normal
    - CARRYING : Portage du vélo (descente)
    - REMOUNTING : En train de remonter sur le vélo
    - CRASHED : Chute, immobilisé
    """
    RIDING = auto()
    CARRYING = auto()
    REMOUNTING = auto()
    CRASHED = auto()


class ICyclistState(Protocol):
    """
    Interface Protocol pour les états du cycliste.

    Utilise typing.Protocol pour définir l'interface sans héritage explicite.
    Chaque état doit implémenter ces méthodes.
    """

    @property
    def state_type(self) -> StateType:
        """
        Retourne le type de cet état.

        Returns:
            StateType de cet état
        """
        ...

    def enter(self, cyclist: 'Cyclist') -> None:
        """
        Appelé lors de l'entrée dans cet état.

        Configure l'état initial, modifie les propriétés du cycliste,
        démarre les animations, etc.

        Args:
            cyclist: L'entité Cyclist qui entre dans cet état
        """
        ...

    def exit(self, cyclist: 'Cyclist') -> None:
        """
        Appelé lors de la sortie de cet état.

        Nettoie les ressources, restaure les propriétés, etc.

        Args:
            cyclist: L'entité Cyclist qui sort de cet état
        """
        ...

    def update(self, cyclist: 'Cyclist', delta_time: float) -> None:
        """
        Met à jour l'état à chaque frame.

        Gère la logique spécifique à cet état, les animations,
        les timers, etc.

        Args:
            cyclist: L'entité Cyclist
            delta_time: Temps écoulé depuis la dernière frame
        """
        ...

    def handle_input(self, cyclist: 'Cyclist', events: list) -> None:
        """
        Gère les entrées spécifiques à cet état.

        Certains états peuvent ignorer certaines commandes
        (ex: CRASHED ignore les inputs de mouvement).

        Args:
            cyclist: L'entité Cyclist
            events: Liste des événements pygame
        """
        ...

    def can_transition_to(self, new_state: StateType) -> bool:
        """
        Vérifie si une transition vers un nouvel état est possible.

        Implémente les règles de transition spécifiques à chaque état.

        Args:
            new_state: Le type d'état vers lequel on veut transitionner

        Returns:
            True si la transition est autorisée, False sinon
        """
        ...
