"""
Entity Manager - Registre central pour gérer toutes les entités du jeu.

L'Entity Manager est responsable de la gestion du cycle de vie de toutes les
entités : création, mise à jour, destruction et recherche.
"""

from typing import List, Dict, Type, Optional
from entities.entity import Entity
from components.icomponent import IComponent


class EntityManager:
    """
    Gestionnaire central de toutes les entités du jeu.

    Cette classe implémente le pattern Singleton pour garantir une seule
    instance dans toute l'application.
    """

    _instance: Optional["EntityManager"] = None

    def __new__(cls) -> "EntityManager":
        """Implémente le pattern Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialise l'Entity Manager."""
        if self._initialized:
            return

        self._entities: List[Entity] = []
        self._entities_by_id: Dict[str, Entity] = {}
        self._entities_by_type: Dict[Type[Entity], List[Entity]] = {}
        self._entities_by_tag: Dict[str, List[Entity]] = {}
        self._initialized = True

    def add_entity(self, entity: Entity) -> None:
        """
        Ajoute une entité au gestionnaire.

        Args:
            entity: L'entité à ajouter

        Raises:
            ValueError: Si une entité avec le même ID existe déjà
        """
        if entity.id in self._entities_by_id:
            raise ValueError(f"Une entité avec l'ID {entity.id} existe déjà")

        self._entities.append(entity)
        self._entities_by_id[entity.id] = entity

        # Indexation par type
        entity_type = type(entity)
        if entity_type not in self._entities_by_type:
            self._entities_by_type[entity_type] = []
        self._entities_by_type[entity_type].append(entity)

        # Indexation par tags
        for tag in entity.tags:
            if tag not in self._entities_by_tag:
                self._entities_by_tag[tag] = []
            self._entities_by_tag[tag].append(entity)

    def remove_entity(self, entity: Entity) -> None:
        """
        Retire une entité du gestionnaire.

        Args:
            entity: L'entité à retirer
        """
        if entity.id not in self._entities_by_id:
            return

        # Retire de la liste principale
        self._entities.remove(entity)
        del self._entities_by_id[entity.id]

        # Retire de l'indexation par type
        entity_type = type(entity)
        if entity_type in self._entities_by_type:
            self._entities_by_type[entity_type].remove(entity)
            if not self._entities_by_type[entity_type]:
                del self._entities_by_type[entity_type]

        # Retire de l'indexation par tags
        for tag in entity.tags:
            if tag in self._entities_by_tag:
                self._entities_by_tag[tag].remove(entity)
                if not self._entities_by_tag[tag]:
                    del self._entities_by_tag[tag]

        # Détruit l'entité
        entity.destroy()

    def get_entity_by_id(self, entity_id: str) -> Optional[Entity]:
        """
        Récupère une entité par son ID.

        Args:
            entity_id: L'ID de l'entité recherchée

        Returns:
            L'entité correspondante ou None si elle n'existe pas
        """
        return self._entities_by_id.get(entity_id)

    def get_entities_by_type(self, entity_type: Type[Entity]) -> List[Entity]:
        """
        Récupère toutes les entités d'un type donné.

        Args:
            entity_type: Le type d'entité recherché

        Returns:
            Liste des entités du type spécifié
        """
        return self._entities_by_type.get(entity_type, []).copy()

    def get_entities_by_tag(self, tag: str) -> List[Entity]:
        """
        Récupère toutes les entités ayant un tag donné.

        Args:
            tag: Le tag recherché

        Returns:
            Liste des entités ayant ce tag
        """
        return self._entities_by_tag.get(tag, []).copy()

    def get_entities_with_component(self, component_type: Type[IComponent]) -> List[Entity]:
        """
        Récupère toutes les entités possédant un composant donné.

        Args:
            component_type: Le type de composant recherché

        Returns:
            Liste des entités possédant ce composant
        """
        return [
            entity for entity in self._entities
            if entity.has_component(component_type)
        ]

    def get_all_entities(self) -> List[Entity]:
        """
        Retourne toutes les entités gérées.

        Returns:
            Liste de toutes les entités
        """
        return self._entities.copy()

    def update(self, delta_time: float) -> None:
        """
        Met à jour toutes les entités actives.

        Args:
            delta_time: Temps écoulé depuis la dernière frame en secondes
        """
        # Met à jour toutes les entités
        for entity in self._entities[:]:  # Copie pour éviter les problèmes de modification
            if entity.active:
                entity.update(delta_time)

        # Supprime les entités marquées pour destruction
        entities_to_remove = [e for e in self._entities if e.to_destroy]
        for entity in entities_to_remove:
            self.remove_entity(entity)

    def clear(self) -> None:
        """Détruit toutes les entités et vide le gestionnaire."""
        for entity in self._entities[:]:
            self.remove_entity(entity)

        self._entities.clear()
        self._entities_by_id.clear()
        self._entities_by_type.clear()
        self._entities_by_tag.clear()

    def entity_count(self) -> int:
        """
        Retourne le nombre d'entités gérées.

        Returns:
            Le nombre d'entités
        """
        return len(self._entities)

    @classmethod
    def reset_instance(cls) -> None:
        """Réinitialise l'instance du Singleton (utile pour les tests)."""
        if cls._instance is not None:
            cls._instance.clear()
            cls._instance = None

    def __repr__(self) -> str:
        """Représentation string de l'Entity Manager."""
        return f"EntityManager(entities={self.entity_count()})"
