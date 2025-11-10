"""
Classe Entity de base pour toutes les entités du jeu.

Une entité est un objet du jeu auquel on peut attacher des composants pour
définir son comportement et ses propriétés.
"""

from typing import Dict, Type, Optional, List, TypeVar
import uuid
from utils.vector2 import Vector2
from components.icomponent import IComponent

T = TypeVar('T', bound=IComponent)


class Entity:
    """
    Classe de base pour toutes les entités du jeu.

    Une entité possède une position, rotation, scale et peut avoir
    des composants attachés qui définissent son comportement.
    """

    def __init__(self, name: str = "Entity") -> None:
        """
        Initialise une nouvelle entité.

        Args:
            name: Nom de l'entité (pour le débogage)
        """
        self._id: str = str(uuid.uuid4())
        self._name: str = name
        self._position: Vector2 = Vector2.zero()
        self._rotation: float = 0.0
        self._scale: Vector2 = Vector2.one()
        self._components: Dict[Type[IComponent], IComponent] = {}
        self._tags: List[str] = []
        self._active: bool = True
        self._to_destroy: bool = False

    @property
    def id(self) -> str:
        """Retourne l'identifiant unique de l'entité."""
        return self._id

    @property
    def name(self) -> str:
        """Retourne le nom de l'entité."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Définit le nom de l'entité."""
        self._name = value

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
        """Retourne la rotation de l'entité (en radians)."""
        return self._rotation

    @rotation.setter
    def rotation(self, value: float) -> None:
        """Définit la rotation de l'entité (en radians)."""
        self._rotation = value

    @property
    def scale(self) -> Vector2:
        """Retourne l'échelle de l'entité."""
        return self._scale

    @scale.setter
    def scale(self, value: Vector2) -> None:
        """Définit l'échelle de l'entité."""
        self._scale = value

    @property
    def active(self) -> bool:
        """Indique si l'entité est active."""
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        """Active ou désactive l'entité."""
        self._active = value

    @property
    def to_destroy(self) -> bool:
        """Indique si l'entité doit être détruite."""
        return self._to_destroy

    def add_component(self, component_class: Type[T], *args, **kwargs) -> T:
        """
        Ajoute un composant à l'entité.

        Args:
            component_class: La classe du composant à ajouter
            *args: Arguments positionnels pour le constructeur du composant
            **kwargs: Arguments nommés pour le constructeur du composant

        Returns:
            L'instance du composant ajouté

        Raises:
            ValueError: Si un composant de ce type existe déjà
        """
        if component_class in self._components:
            raise ValueError(
                f"Le composant {component_class.__name__} existe déjà sur l'entité {self._name}"
            )

        component = component_class(self, *args, **kwargs)
        self._components[component_class] = component
        component.init()
        return component

    def get_component(self, component_class: Type[T]) -> Optional[T]:
        """
        Récupère un composant de l'entité.

        Args:
            component_class: La classe du composant recherché

        Returns:
            L'instance du composant ou None s'il n'existe pas
        """
        return self._components.get(component_class)  # type: ignore

    def has_component(self, component_class: Type[IComponent]) -> bool:
        """
        Vérifie si l'entité possède un composant d'un certain type.

        Args:
            component_class: La classe du composant recherché

        Returns:
            True si le composant existe, False sinon
        """
        return component_class in self._components

    def remove_component(self, component_class: Type[IComponent]) -> None:
        """
        Retire un composant de l'entité.

        Args:
            component_class: La classe du composant à retirer

        Raises:
            ValueError: Si le composant n'existe pas
        """
        if component_class not in self._components:
            raise ValueError(
                f"Le composant {component_class.__name__} n'existe pas sur l'entité {self._name}"
            )

        component = self._components[component_class]
        component.destroy()
        del self._components[component_class]

    def get_all_components(self) -> List[IComponent]:
        """
        Retourne tous les composants de l'entité.

        Returns:
            Liste de tous les composants
        """
        return list(self._components.values())

    def add_tag(self, tag: str) -> None:
        """
        Ajoute un tag à l'entité.

        Args:
            tag: Le tag à ajouter
        """
        if tag not in self._tags:
            self._tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """
        Retire un tag de l'entité.

        Args:
            tag: Le tag à retirer
        """
        if tag in self._tags:
            self._tags.remove(tag)

    def has_tag(self, tag: str) -> bool:
        """
        Vérifie si l'entité possède un tag.

        Args:
            tag: Le tag recherché

        Returns:
            True si le tag existe, False sinon
        """
        return tag in self._tags

    @property
    def tags(self) -> List[str]:
        """Retourne la liste des tags de l'entité."""
        return self._tags.copy()

    def update(self, delta_time: float) -> None:
        """
        Met à jour l'entité et tous ses composants.

        Args:
            delta_time: Temps écoulé depuis la dernière frame en secondes
        """
        if not self._active:
            return

        for component in self._components.values():
            if component.enabled:
                component.update(delta_time)

    def destroy(self) -> None:
        """Marque l'entité pour destruction."""
        self._to_destroy = True

        # Détruit tous les composants
        for component in list(self._components.values()):
            component.destroy()
        self._components.clear()

    def __repr__(self) -> str:
        """Représentation string de l'entité."""
        return f"Entity(id={self._id[:8]}, name={self._name}, pos={self._position})"
