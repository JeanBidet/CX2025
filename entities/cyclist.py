"""
Classe Cyclist - Représente un cycliste dans le jeu.

Cette classe hérite d'Entity et combine les composants nécessaires pour
créer un cycliste contrôlable avec physique réaliste.
"""

from entities.entity import Entity
from components.transform_component import TransformComponent
from components.physics_component import PhysicsComponent
from components.input_component import InputComponent
from config.game_config import GameConfig
from utils.vector2 import Vector2


class Cyclist(Entity):
    """
    Entité représentant un cycliste de cyclo-cross.

    Cette classe combine :
    - TransformComponent pour la position et rotation
    - PhysicsComponent pour le mouvement réaliste
    - InputComponent pour les contrôles (optionnel, pour le joueur)
    """

    def __init__(
        self,
        name: str = "Cyclist",
        position: Vector2 | None = None,
        is_player: bool = True
    ) -> None:
        """
        Initialise un cycliste.

        Args:
            name: Nom du cycliste
            position: Position initiale
            is_player: Si vrai, ajoute les contrôles clavier
        """
        super().__init__(name)

        # Stocke si c'est un joueur
        self.is_player: bool = is_player

        # Position initiale
        if position:
            self.position = position

        # Ajoute les composants de base
        self._setup_components()

    def _setup_components(self) -> None:
        """Configure les composants du cycliste."""
        # Transform Component
        self.add_component(
            TransformComponent,
            self.position.copy() if hasattr(self, 'position') else None
        )

        # Physics Component avec paramètres depuis GameConfig
        self.add_component(
            PhysicsComponent,
            mass=GameConfig.CYCLIST_MASS,
            drag=GameConfig.CYCLIST_DRAG,
            max_speed=GameConfig.CYCLIST_MAX_SPEED,
            use_gravity=False  # Pas de gravité en vue top-down
        )

        # Input Component seulement pour le joueur
        if self.is_player:
            self.add_component(
                InputComponent,
                acceleration_force=GameConfig.CYCLIST_ACCELERATION_FORCE,
                brake_force=GameConfig.CYCLIST_BRAKE_FORCE,
                turn_speed_slow=GameConfig.CYCLIST_TURN_SPEED_SLOW,
                turn_speed_fast=GameConfig.CYCLIST_TURN_SPEED_FAST,
                speed_threshold=GameConfig.CYCLIST_SPEED_THRESHOLD
            )

    def get_transform(self) -> TransformComponent:
        """
        Retourne le composant de transformation.

        Returns:
            Le TransformComponent du cycliste
        """
        transform = self.get_component(TransformComponent)
        if transform is None:
            raise RuntimeError(f"Cyclist {self.name} n'a pas de TransformComponent")
        return transform

    def get_physics(self) -> PhysicsComponent:
        """
        Retourne le composant de physique.

        Returns:
            Le PhysicsComponent du cycliste
        """
        physics = self.get_component(PhysicsComponent)
        if physics is None:
            raise RuntimeError(f"Cyclist {self.name} n'a pas de PhysicsComponent")
        return physics

    def get_input(self) -> InputComponent | None:
        """
        Retourne le composant d'input s'il existe.

        Returns:
            Le InputComponent du cycliste ou None si c'est un IA
        """
        return self.get_component(InputComponent)

    def get_speed(self) -> float:
        """
        Retourne la vitesse actuelle du cycliste.

        Returns:
            Vitesse en pixels/seconde
        """
        physics = self.get_physics()
        return physics.get_speed()

    def get_direction(self) -> Vector2:
        """
        Retourne la direction vers laquelle le cycliste regarde.

        Returns:
            Vecteur unitaire de direction
        """
        transform = self.get_transform()
        return transform.get_forward_vector()

    def stop(self) -> None:
        """Arrête complètement le mouvement du cycliste."""
        physics = self.get_physics()
        physics.stop()

    def apply_force(self, force: Vector2) -> None:
        """
        Applique une force externe au cycliste (vent, collision, etc.).

        Args:
            force: Force à appliquer (Newtons)
        """
        physics = self.get_physics()
        physics.apply_force(force)

    def __repr__(self) -> str:
        """Représentation string du cycliste."""
        speed = self.get_speed()
        player_str = " (Player)" if self.is_player else ""
        return f"Cyclist(name={self.name}{player_str}, speed={speed:.1f}px/s)"
