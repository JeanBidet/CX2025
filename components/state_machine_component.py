"""
State Machine Component - Composant gérant la machine à états d'une entité.

Ce composant implémente le State Pattern pour gérer les différents états
d'une entité (cycliste) et les transitions entre ces états.
"""

from typing import Optional
import pygame
from components.icomponent import IComponent
from systems.cyclist_state import StateType, ICyclistState


class StateMachineComponent(IComponent):
    """
    Composant implémentant une machine à états finis (FSM).

    Gère les états d'une entité, les transitions entre états,
    et maintient un historique optionnel des transitions.
    """

    def __init__(
        self,
        owner,
        initial_state: StateType = StateType.RIDING,
        keep_history: bool = False,
        max_history_size: int = 50
    ) -> None:
        """
        Initialise le composant de machine à états.

        Args:
            owner: L'entité propriétaire
            initial_state: État initial
            keep_history: Si True, garde un historique des transitions
            max_history_size: Taille maximale de l'historique
        """
        super().__init__(owner)

        self._states: dict[StateType, ICyclistState] = {}
        self._current_state: Optional[ICyclistState] = None
        self._initial_state_type = initial_state

        # Historique des transitions
        self._keep_history = keep_history
        self._max_history_size = max_history_size
        self._history: list[tuple[StateType, float]] = []  # (state_type, timestamp)
        self._transition_time: float = 0.0

    def init(self) -> None:
        """Initialise le composant."""
        # Les états seront ajoutés par l'entité propriétaire
        pass

    def add_state(self, state_type: StateType, state: ICyclistState) -> None:
        """
        Ajoute un état à la machine.

        Args:
            state_type: Type de l'état
            state: Instance de l'état
        """
        self._states[state_type] = state

    def change_state(self, new_state_type: StateType, force: bool = False) -> bool:
        """
        Change l'état actuel.

        Args:
            new_state_type: Type du nouvel état
            force: Si True, ignore la validation can_transition_to

        Returns:
            True si la transition a réussi, False sinon
        """
        # Vérifie que le nouvel état existe
        if new_state_type not in self._states:
            print(f"[StateMachine] Erreur: État {new_state_type.name} n'existe pas")
            return False

        # Vérifie si la transition est autorisée
        if self._current_state and not force:
            if not self._current_state.can_transition_to(new_state_type):
                print(
                    f"[StateMachine] Transition {self._current_state.state_type.name} -> "
                    f"{new_state_type.name} non autorisee"
                )
                return False

        # Effectue la transition
        old_state_type = self._current_state.state_type if self._current_state else None

        # Sortie de l'état actuel
        if self._current_state:
            self._current_state.exit(self.owner)

        # Changement d'état
        self._current_state = self._states[new_state_type]

        # Entrée dans le nouvel état
        self._current_state.enter(self.owner)

        # Enregistre dans l'historique
        if self._keep_history:
            import time
            self._history.append((new_state_type, time.time()))
            # Limite la taille de l'historique
            if len(self._history) > self._max_history_size:
                self._history.pop(0)

        print(
            f"[StateMachine] Transition: {old_state_type.name if old_state_type else 'None'} -> "
            f"{new_state_type.name}"
        )

        return True

    def update(self, delta_time: float) -> None:
        """
        Met à jour l'état actuel.

        Args:
            delta_time: Temps écoulé depuis la dernière frame
        """
        if self._current_state:
            self._current_state.update(self.owner, delta_time)
            self._transition_time += delta_time

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Transmet les événements à l'état actuel.

        Args:
            events: Liste des événements Pygame
        """
        if self._current_state:
            self._current_state.handle_input(self.owner, events)

    def get_current_state_type(self) -> Optional[StateType]:
        """
        Retourne le type d'état actuel.

        Returns:
            StateType ou None si aucun état
        """
        if self._current_state:
            return self._current_state.state_type
        return None

    def get_current_state_name(self) -> str:
        """
        Retourne le nom de l'état actuel.

        Returns:
            Nom de l'état ou "None"
        """
        if self._current_state:
            return self._current_state.state_type.name
        return "None"

    def get_time_in_current_state(self) -> float:
        """
        Retourne le temps passé dans l'état actuel.

        Returns:
            Temps en secondes
        """
        return self._transition_time

    def is_in_state(self, state_type: StateType) -> bool:
        """
        Vérifie si on est dans un état donné.

        Args:
            state_type: Type d'état à vérifier

        Returns:
            True si dans cet état
        """
        return self._current_state and self._current_state.state_type == state_type

    def get_history(self) -> list[tuple[StateType, float]]:
        """
        Retourne l'historique des transitions.

        Returns:
            Liste de (StateType, timestamp)
        """
        return self._history.copy()

    def clear_history(self) -> None:
        """Efface l'historique des transitions."""
        self._history.clear()

    def get_state_count(self) -> int:
        """
        Retourne le nombre d'états disponibles.

        Returns:
            Nombre d'états
        """
        return len(self._states)

    def has_state(self, state_type: StateType) -> bool:
        """
        Vérifie si un état existe.

        Args:
            state_type: Type d'état

        Returns:
            True si l'état existe
        """
        return state_type in self._states

    def destroy(self) -> None:
        """Nettoie les ressources du composant."""
        # Sortie de l'état actuel
        if self._current_state:
            self._current_state.exit(self.owner)

        self._states.clear()
        self._history.clear()
        self._current_state = None

    def __repr__(self) -> str:
        """Représentation string du composant."""
        current = self.get_current_state_name()
        return (
            f"StateMachineComponent(states={len(self._states)}, "
            f"current={current}, "
            f"time_in_state={self._transition_time:.2f}s)"
        )
