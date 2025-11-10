"""
Terrain Physics Component - Intègre les effets du terrain sur la physique.

Ce composant interroge le TerrainManager pour déterminer le terrain actuel
et applique ses effets sur le PhysicsComponent de l'entité.
"""

from typing import Optional
from components.icomponent import IComponent
from components.transform_component import TransformComponent
from components.physics_component import PhysicsComponent
from systems.terrain_manager import TerrainManager
from systems.terrain_data import TerrainData, TerrainType


class TerrainPhysicsComponent(IComponent):
    """
    Composant qui applique les effets du terrain sur la physique.

    Modifie dynamiquement les propriétés physiques (vitesse, drag, adhérence)
    en fonction du type de terrain sous l'entité.
    """

    def __init__(
        self,
        owner,
        terrain_manager: TerrainManager,
        base_max_speed: float = 450.0,
        base_drag: float = 0.985
    ) -> None:
        """
        Initialise le composant de physique de terrain.

        Args:
            owner: L'entité propriétaire
            terrain_manager: Gestionnaire de terrain pour les requêtes
            base_max_speed: Vitesse maximale de base (sans terrain)
            base_drag: Drag de base (sans terrain)
        """
        super().__init__(owner)

        self._terrain_manager = terrain_manager
        self._base_max_speed = base_max_speed
        self._base_drag = base_drag

        # Composants requis
        self._transform: Optional[TransformComponent] = None
        self._physics: Optional[PhysicsComponent] = None

        # État actuel du terrain
        self._current_terrain: Optional[TerrainData] = None
        self._current_terrain_type: TerrainType = TerrainType.GRASS

    def init(self) -> None:
        """Initialise le composant et récupère les composants requis."""
        self._transform = self.owner.get_component(TransformComponent)
        self._physics = self.owner.get_component(PhysicsComponent)

        if not self._transform:
            raise ValueError(
                f"TerrainPhysicsComponent requiert TransformComponent "
                f"sur {self.owner.name}"
            )

        if not self._physics:
            raise ValueError(
                f"TerrainPhysicsComponent requiert PhysicsComponent "
                f"sur {self.owner.name}"
            )

    def update(self, delta_time: float) -> None:
        """
        Met à jour les effets du terrain sur la physique.

        Args:
            delta_time: Temps écoulé depuis la dernière frame
        """
        if not self._transform or not self._physics:
            return

        # Récupère le terrain à la position actuelle
        position = self._transform.position
        terrain_data = self._terrain_manager.get_terrain_data_at_position(position)

        # Si le terrain a changé, applique les nouveaux effets
        if terrain_data and terrain_data != self._current_terrain:
            self._apply_terrain_effects(terrain_data)
            self._current_terrain = terrain_data
            self._current_terrain_type = terrain_data.terrain_type

    def _apply_terrain_effects(self, terrain_data: TerrainData) -> None:
        """
        Applique les effets d'un terrain sur la physique.

        Args:
            terrain_data: Données du terrain à appliquer
        """
        if not self._physics:
            return

        # Modifie la vitesse maximale
        new_max_speed = self._base_max_speed * terrain_data.speed_multiplier
        self._physics.max_speed = new_max_speed

        # Modifie le drag (résistance)
        # drag_modifier positif = plus de résistance
        # drag_modifier négatif = moins de résistance (bonus)
        new_drag = self._base_drag - terrain_data.drag_modifier
        # Clamp entre 0.0 et 1.0 pour éviter les valeurs aberrantes
        new_drag = max(0.0, min(1.0, new_drag))
        self._physics.drag = new_drag

    def get_current_terrain_type(self) -> TerrainType:
        """
        Retourne le type de terrain actuel.

        Returns:
            TerrainType actuel
        """
        return self._current_terrain_type

    def get_current_terrain_name(self) -> str:
        """
        Retourne le nom du terrain actuel.

        Returns:
            Nom du terrain (ou "Inconnu" si aucun)
        """
        if self._current_terrain:
            return self._current_terrain.name
        return "Inconnu"

    def get_current_grip_level(self) -> float:
        """
        Retourne le niveau d'adhérence actuel.

        Utile pour les systèmes de freinage/virage qui utilisent l'adhérence.

        Returns:
            Niveau d'adhérence (0.0-1.0)
        """
        if self._current_terrain:
            return self._current_terrain.grip_level
        return 0.5  # Valeur par défaut

    def get_current_stamina_drain(self) -> float:
        """
        Retourne le multiplicateur de drain de stamina actuel.

        Sera utilisé par le système de stamina (Prompt 6).

        Returns:
            Multiplicateur de drain de stamina
        """
        if self._current_terrain:
            return self._current_terrain.stamina_drain_multiplier
        return 1.0  # Valeur par défaut

    def get_base_max_speed(self) -> float:
        """
        Retourne la vitesse maximale de base (sans terrain).

        Returns:
            Vitesse maximale de base
        """
        return self._base_max_speed

    def set_base_max_speed(self, speed: float) -> None:
        """
        Définit la vitesse maximale de base.

        Args:
            speed: Nouvelle vitesse maximale de base
        """
        self._base_max_speed = speed
        # Réapplique les effets du terrain actuel
        if self._current_terrain:
            self._apply_terrain_effects(self._current_terrain)

    def get_base_drag(self) -> float:
        """
        Retourne le drag de base (sans terrain).

        Returns:
            Drag de base
        """
        return self._base_drag

    def set_base_drag(self, drag: float) -> None:
        """
        Définit le drag de base.

        Args:
            drag: Nouveau drag de base
        """
        self._base_drag = drag
        # Réapplique les effets du terrain actuel
        if self._current_terrain:
            self._apply_terrain_effects(self._current_terrain)

    def destroy(self) -> None:
        """Nettoie les ressources du composant."""
        self._transform = None
        self._physics = None
        self._current_terrain = None

    def __repr__(self) -> str:
        """Représentation string du composant."""
        return (
            f"TerrainPhysicsComponent("
            f"terrain={self._current_terrain_type.name if self._current_terrain else 'None'}, "
            f"base_speed={self._base_max_speed:.1f}, "
            f"base_drag={self._base_drag:.3f})"
        )
