"""
Command Input Handler - Gère le mapping des touches vers les commandes.

Ce handler transforme les événements Pygame en commandes exécutables,
découplant complètement l'input de la logique métier.
"""

from typing import Dict, List, Set
import pygame
from patterns.commands.command import ICommand


class CommandInputHandler:
    """
    Gestionnaire d'entrées basé sur le Command Pattern.

    Maintient un mapping entre les touches Pygame et les commandes à exécuter.
    Supporte les touches maintenues (get_pressed) et les événements ponctuels.
    """

    def __init__(self) -> None:
        """Initialise le handler d'entrées."""
        # Mapping touche maintenue -> commande
        self._key_to_command: Dict[int, ICommand] = {}

        # Mapping événement ponctuel -> commande
        self._event_to_command: Dict[int, ICommand] = {}

        # Commandes actives cette frame
        self._active_commands: List[ICommand] = []

    def bind_key(self, key: int, command: ICommand) -> None:
        """
        Associe une touche maintenue à une commande.

        Args:
            key: Code de touche Pygame (ex: pygame.K_UP)
            command: Commande à exécuter
        """
        self._key_to_command[key] = command

    def bind_event(self, key: int, command: ICommand) -> None:
        """
        Associe un événement ponctuel (KEYDOWN) à une commande.

        Args:
            key: Code de touche Pygame
            command: Commande à exécuter
        """
        self._event_to_command[key] = command

    def unbind_key(self, key: int) -> None:
        """
        Retire l'association d'une touche.

        Args:
            key: Code de touche à délier
        """
        if key in self._key_to_command:
            del self._key_to_command[key]

    def unbind_event(self, key: int) -> None:
        """
        Retire l'association d'un événement.

        Args:
            key: Code de touche à délier
        """
        if key in self._event_to_command:
            del self._event_to_command[key]

    def clear_bindings(self) -> None:
        """Efface toutes les associations touches/commandes."""
        self._key_to_command.clear()
        self._event_to_command.clear()

    def handle_input(self, events: List[pygame.event.Event]) -> List[ICommand]:
        """
        Traite les entrées et retourne les commandes à exécuter.

        Args:
            events: Liste des événements Pygame de cette frame

        Returns:
            Liste des commandes à exécuter
        """
        self._active_commands.clear()
        processed_keys: Set[int] = set()

        # 1. Traite les événements ponctuels (KEYDOWN)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in self._event_to_command:
                command = self._event_to_command[event.key]
                self._active_commands.append(command)
                processed_keys.add(event.key)

        # 2. Traite les touches maintenues (get_pressed)
        keys_pressed = pygame.key.get_pressed()
        for key, command in self._key_to_command.items():
            # Évite de traiter deux fois la même touche
            if keys_pressed[key] and key not in processed_keys:
                self._active_commands.append(command)

        # 3. Tri par priorité (plus haute = exécutée en premier)
        self._active_commands.sort(key=lambda cmd: cmd.priority, reverse=True)

        return self._active_commands.copy()

    def get_bound_keys(self) -> Dict[int, str]:
        """
        Retourne un dictionnaire des touches liées et leur commande.

        Returns:
            Dictionnaire {touche: nom_commande}
        """
        result = {}
        for key, command in self._key_to_command.items():
            result[key] = command.name
        for key, command in self._event_to_command.items():
            result[key] = f"{command.name} (event)"
        return result

    def __repr__(self) -> str:
        """Représentation string du handler."""
        return (
            f"CommandInputHandler("
            f"keys={len(self._key_to_command)}, "
            f"events={len(self._event_to_command)})"
        )
