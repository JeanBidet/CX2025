"""
Command Input Component - Composant d'entrée utilisant le Command Pattern.

Ce composant remplace l'ancien InputComponent en utilisant le Command Pattern
pour une meilleure flexibilité et testabilité.
"""

from typing import List
import pygame
from components.icomponent import IComponent
from patterns.commands.command import ICommand
from patterns.commands.command_input_handler import CommandInputHandler
from config.input_config import InputProfile, get_profile


class CommandInputComponent(IComponent):
    """
    Composant gérant les entrées via le Command Pattern.

    Utilise un CommandInputHandler pour mapper les touches aux commandes,
    puis exécute ces commandes sur l'entité propriétaire.
    """

    def __init__(
        self,
        owner,
        profile_name: str = "hybrid",
        enabled: bool = True
    ) -> None:
        """
        Initialise le composant d'entrée basé sur des commandes.

        Args:
            owner: L'entité propriétaire
            profile_name: Nom du profil de contrôle à utiliser
            enabled: Si le composant est actif
        """
        super().__init__(owner)

        self._profile_name: str = profile_name
        self._handler: CommandInputHandler = CommandInputHandler()
        self._enabled: bool = enabled
        self._last_events: List[pygame.event.Event] = []

    def init(self) -> None:
        """Initialise le composant et charge le profil de contrôle."""
        self.load_profile(self._profile_name)

    def load_profile(self, profile_name: str) -> None:
        """
        Charge un profil de contrôle.

        Args:
            profile_name: Nom du profil à charger

        Raises:
            ValueError: Si le profil n'existe pas
        """
        profile = get_profile(profile_name)
        self._profile_name = profile_name

        # Efface les bindings existants
        self._handler.clear_bindings()

        # Charge les bindings du profil
        for key, command_factory in profile.key_bindings.items():
            command = command_factory()
            self._handler.bind_key(key, command)

        for key, command_factory in profile.event_bindings.items():
            command = command_factory()
            self._handler.bind_event(key, command)

        print(f"[CommandInputComponent] Profil '{profile_name}' chargé")

    def set_events(self, events: List[pygame.event.Event]) -> None:
        """
        Définit les événements à traiter pour cette frame.

        Cette méthode doit être appelée avant update(), généralement
        dans la scène ou le système de jeu.

        Args:
            events: Liste des événements Pygame
        """
        self._last_events = events

    def update(self, delta_time: float) -> None:
        """
        Met à jour le composant en exécutant les commandes actives.

        Args:
            delta_time: Temps écoulé depuis la dernière frame
        """
        if not self._enabled:
            return

        # Récupère les commandes à exécuter
        commands = self._handler.handle_input(self._last_events)

        # Exécute chaque commande qui peut s'exécuter
        for command in commands:
            if command.can_execute(self.owner):
                command.execute(self.owner, delta_time)

        # Efface les événements après traitement
        self._last_events.clear()

    def enable(self) -> None:
        """Active le composant d'entrée."""
        self._enabled = True

    def disable(self) -> None:
        """Désactive le composant d'entrée."""
        self._enabled = False

    def is_enabled(self) -> bool:
        """
        Vérifie si le composant est actif.

        Returns:
            True si actif, False sinon
        """
        return self._enabled

    def get_bound_keys(self) -> dict[int, str]:
        """
        Retourne les touches liées et leurs commandes.

        Returns:
            Dictionnaire {touche: nom_commande}
        """
        return self._handler.get_bound_keys()

    def get_profile_name(self) -> str:
        """
        Retourne le nom du profil actuellement chargé.

        Returns:
            Nom du profil
        """
        return self._profile_name

    def destroy(self) -> None:
        """Nettoie les ressources du composant."""
        self._handler.clear_bindings()
        self._last_events.clear()

    def __repr__(self) -> str:
        """Représentation string du composant."""
        status = "enabled" if self._enabled else "disabled"
        return (
            f"CommandInputComponent(profile={self._profile_name}, "
            f"status={status})"
        )
