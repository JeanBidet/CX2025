"""
Cyclist States - Implémentations concrètes des états du cycliste.

Ce module contient les 4 états :
- RidingState : En selle, pédalage normal
- CarryingState : Portage du vélo
- RemountingState : Remontée sur le vélo
- CrashedState : Chute
"""

from typing import TYPE_CHECKING
import pygame
from systems.cyclist_state import StateType, ICyclistState

if TYPE_CHECKING:
    from entities.cyclist import Cyclist


class RidingState:
    """
    État RIDING - Le cycliste est en selle et pédale normalement.

    Comportement :
    - Contrôles complets (accélération, freinage, virage)
    - Animation de pédalage
    - Consommation d'endurance active
    - Peut transitionner vers CARRYING ou CRASHED
    """

    def __init__(self) -> None:
        """Initialise l'état RIDING."""
        self._state_type = StateType.RIDING

    @property
    def state_type(self) -> StateType:
        """Retourne le type d'état."""
        return self._state_type

    def enter(self, cyclist: 'Cyclist') -> None:
        """
        Entrée dans l'état RIDING.

        Args:
            cyclist: L'entité cycliste
        """
        print("[RidingState] Entrée dans l'état RIDING")

        # Joue l'animation de pédalage
        if hasattr(cyclist, 'animation_controller'):
            if cyclist.animation_controller.has_animation('pedal'):
                cyclist.animation_controller.play('pedal', reset=True)

        # Restaure les paramètres physiques normaux
        from components.physics_component import PhysicsComponent
        physics = cyclist.get_component(PhysicsComponent)
        if physics and hasattr(cyclist, '_base_max_speed'):
            # Restaure la vitesse max de base (sera modifiée par le terrain)
            physics.max_speed = cyclist._base_max_speed

    def exit(self, cyclist: 'Cyclist') -> None:
        """
        Sortie de l'état RIDING.

        Args:
            cyclist: L'entité cycliste
        """
        print("[RidingState] Sortie de l'état RIDING")

    def update(self, cyclist: 'Cyclist', delta_time: float) -> None:
        """
        Update de l'état RIDING.

        Args:
            cyclist: L'entité cycliste
            delta_time: Temps écoulé
        """
        # L'animation est mise à jour automatiquement par l'AnimationController
        # La physique est gérée par PhysicsComponent
        # La consommation d'endurance sera gérée par StaminaComponent (Prompt 6)
        pass

    def handle_input(self, cyclist: 'Cyclist', events: list[pygame.event.Event]) -> None:
        """
        Gère les inputs en état RIDING.

        Args:
            cyclist: L'entité cycliste
            events: Événements pygame
        """
        # Tous les inputs sont gérés normalement par CommandInputComponent
        # On pourrait ajouter ici la touche pour passer en CARRYING
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # Touche 'C' pour porter le vélo
                    # Demande transition vers CARRYING
                    if hasattr(cyclist, 'state_machine'):
                        cyclist.state_machine.change_state(StateType.CARRYING)

    def can_transition_to(self, new_state: StateType) -> bool:
        """
        Vérifie si transition possible depuis RIDING.

        Args:
            new_state: État cible

        Returns:
            True si transition autorisée
        """
        # RIDING peut aller vers CARRYING ou CRASHED
        return new_state in [StateType.CARRYING, StateType.CRASHED]


class CarryingState:
    """
    État CARRYING - Le cycliste porte son vélo à pied.

    Comportement :
    - Vitesse réduite (marche)
    - Animation de marche
    - Récupération partielle d'endurance
    - Peut remonter sur le vélo (REMOUNTING)
    """

    def __init__(self) -> None:
        """Initialise l'état CARRYING."""
        self._state_type = StateType.CARRYING
        self._carrying_speed_multiplier = 0.3  # 30% de la vitesse normale

    @property
    def state_type(self) -> StateType:
        """Retourne le type d'état."""
        return self._state_type

    def enter(self, cyclist: 'Cyclist') -> None:
        """
        Entrée dans l'état CARRYING.

        Args:
            cyclist: L'entité cycliste
        """
        print("[CarryingState] Entrée dans l'état CARRYING")

        # Joue l'animation de marche
        if hasattr(cyclist, 'animation_controller'):
            if cyclist.animation_controller.has_animation('walk'):
                cyclist.animation_controller.play('walk', reset=True)

        # Réduit la vitesse maximale
        from components.physics_component import PhysicsComponent
        physics = cyclist.get_component(PhysicsComponent)
        if physics and hasattr(cyclist, '_base_max_speed'):
            physics.max_speed = cyclist._base_max_speed * self._carrying_speed_multiplier

    def exit(self, cyclist: 'Cyclist') -> None:
        """
        Sortie de l'état CARRYING.

        Args:
            cyclist: L'entité cycliste
        """
        print("[CarryingState] Sortie de l'état CARRYING")

        # Restaure la vitesse normale
        from components.physics_component import PhysicsComponent
        physics = cyclist.get_component(PhysicsComponent)
        if physics and hasattr(cyclist, '_base_max_speed'):
            physics.max_speed = cyclist._base_max_speed

    def update(self, cyclist: 'Cyclist', delta_time: float) -> None:
        """
        Update de l'état CARRYING.

        Args:
            cyclist: L'entité cycliste
            delta_time: Temps écoulé
        """
        # Récupération partielle d'endurance (futur Prompt 6)
        pass

    def handle_input(self, cyclist: 'Cyclist', events: list[pygame.event.Event]) -> None:
        """
        Gère les inputs en état CARRYING.

        Args:
            cyclist: L'entité cycliste
            events: Événements pygame
        """
        # Touche pour remonter sur le vélo
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # Touche 'C' pour remonter
                    # Demande transition vers REMOUNTING
                    if hasattr(cyclist, 'state_machine'):
                        cyclist.state_machine.change_state(StateType.REMOUNTING)

    def can_transition_to(self, new_state: StateType) -> bool:
        """
        Vérifie si transition possible depuis CARRYING.

        Args:
            new_state: État cible

        Returns:
            True si transition autorisée
        """
        # CARRYING peut aller vers REMOUNTING ou CRASHED
        return new_state in [StateType.REMOUNTING, StateType.CRASHED]


class RemountingState:
    """
    État REMOUNTING - Le cycliste remonte sur son vélo.

    Comportement :
    - État transitoire avec timer
    - Sprite de transition
    - Bloque les inputs
    - Transition automatique vers RIDING
    """

    def __init__(self, duration: float = 1.0) -> None:
        """
        Initialise l'état REMOUNTING.

        Args:
            duration: Durée de la remontée en secondes
        """
        self._state_type = StateType.REMOUNTING
        self._duration = duration
        self._elapsed_time = 0.0

    @property
    def state_type(self) -> StateType:
        """Retourne le type d'état."""
        return self._state_type

    def enter(self, cyclist: 'Cyclist') -> None:
        """
        Entrée dans l'état REMOUNTING.

        Args:
            cyclist: L'entité cycliste
        """
        print("[RemountingState] Entrée dans l'état REMOUNTING")

        # Reset le timer
        self._elapsed_time = 0.0

        # Joue l'animation de remontée (one-shot)
        if hasattr(cyclist, 'animation_controller'):
            if cyclist.animation_controller.has_animation('mount'):
                cyclist.animation_controller.play('mount', reset=True)

        # Ralentit légèrement
        from components.physics_component import PhysicsComponent
        physics = cyclist.get_component(PhysicsComponent)
        if physics:
            physics.velocity = physics.velocity * 0.5

    def exit(self, cyclist: 'Cyclist') -> None:
        """
        Sortie de l'état REMOUNTING.

        Args:
            cyclist: L'entité cycliste
        """
        print("[RemountingState] Sortie de l'état REMOUNTING")

    def update(self, cyclist: 'Cyclist', delta_time: float) -> None:
        """
        Update de l'état REMOUNTING.

        Args:
            cyclist: L'entité cycliste
            delta_time: Temps écoulé
        """
        self._elapsed_time += delta_time

        # Transition automatique vers RIDING après la durée
        if self._elapsed_time >= self._duration:
            if hasattr(cyclist, 'state_machine'):
                cyclist.state_machine.change_state(StateType.RIDING)

    def handle_input(self, cyclist: 'Cyclist', events: list[pygame.event.Event]) -> None:
        """
        Gère les inputs en état REMOUNTING.

        Args:
            cyclist: L'entité cycliste
            events: Événements pygame
        """
        # Bloque tous les inputs pendant la remontée
        pass

    def can_transition_to(self, new_state: StateType) -> bool:
        """
        Vérifie si transition possible depuis REMOUNTING.

        Args:
            new_state: État cible

        Returns:
            True si transition autorisée
        """
        # REMOUNTING peut uniquement aller vers RIDING ou CRASHED
        return new_state in [StateType.RIDING, StateType.CRASHED]


class CrashedState:
    """
    État CRASHED - Le cycliste est tombé.

    Comportement :
    - Immobilisation totale
    - Sprite de chute avec rotation
    - Timer avant REMOUNTING
    - Effet visuel (teinte rouge)
    """

    def __init__(self, recovery_duration: float = 2.0) -> None:
        """
        Initialise l'état CRASHED.

        Args:
            recovery_duration: Durée avant de pouvoir remonter
        """
        self._state_type = StateType.CRASHED
        self._recovery_duration = recovery_duration
        self._elapsed_time = 0.0

    @property
    def state_type(self) -> StateType:
        """Retourne le type d'état."""
        return self._state_type

    def enter(self, cyclist: 'Cyclist') -> None:
        """
        Entrée dans l'état CRASHED.

        Args:
            cyclist: L'entité cycliste
        """
        print("[CrashedState] Entrée dans l'état CRASHED - CHUTE!")

        # Reset le timer
        self._elapsed_time = 0.0

        # Joue l'animation de chute
        if hasattr(cyclist, 'animation_controller'):
            if cyclist.animation_controller.has_animation('fall'):
                cyclist.animation_controller.play('fall', reset=True)

        # Immobilise le cycliste
        from components.physics_component import PhysicsComponent
        physics = cyclist.get_component(PhysicsComponent)
        if physics:
            physics.velocity = physics.velocity * 0.0  # Stop complet
            physics.stop()

        # Active l'effet visuel rouge (sera géré par le renderer)
        if hasattr(cyclist, '_crashed_effect_active'):
            cyclist._crashed_effect_active = True

    def exit(self, cyclist: 'Cyclist') -> None:
        """
        Sortie de l'état CRASHED.

        Args:
            cyclist: L'entité cycliste
        """
        print("[CrashedState] Sortie de l'état CRASHED")

        # Désactive l'effet visuel
        if hasattr(cyclist, '_crashed_effect_active'):
            cyclist._crashed_effect_active = False

    def update(self, cyclist: 'Cyclist', delta_time: float) -> None:
        """
        Update de l'état CRASHED.

        Args:
            cyclist: L'entité cycliste
            delta_time: Temps écoulé
        """
        self._elapsed_time += delta_time

        # Transition automatique vers REMOUNTING après recovery
        if self._elapsed_time >= self._recovery_duration:
            if hasattr(cyclist, 'state_machine'):
                cyclist.state_machine.change_state(StateType.REMOUNTING)

    def handle_input(self, cyclist: 'Cyclist', events: list[pygame.event.Event]) -> None:
        """
        Gère les inputs en état CRASHED.

        Args:
            cyclist: L'entité cycliste
            events: Événements pygame
        """
        # Bloque tous les inputs pendant la chute
        pass

    def can_transition_to(self, new_state: StateType) -> bool:
        """
        Vérifie si transition possible depuis CRASHED.

        Args:
            new_state: État cible

        Returns:
            True si transition autorisée
        """
        # CRASHED peut uniquement aller vers REMOUNTING
        return new_state == StateType.REMOUNTING
