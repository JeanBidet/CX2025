"""
Commandes de mouvement pour les cyclistes.

Ces commandes encapsulent les actions de mouvement et peuvent être
utilisées par les joueurs ou l'IA.
"""

from patterns.commands.command import BaseCommand
from components.physics_component import PhysicsComponent
from components.transform_component import TransformComponent
from entities.entity import Entity
from utils.vector2 import Vector2


class AccelerateCommand(BaseCommand):
    """Commande pour accélérer vers l'avant."""

    def __init__(self, force: float = 1200.0, priority: int = 10) -> None:
        """
        Initialise la commande d'accélération.

        Args:
            force: Force d'accélération (Newtons)
            priority: Priorité d'exécution
        """
        super().__init__("Accelerate", priority)
        self.force: float = force

    def execute(self, entity: Entity, delta_time: float) -> None:
        """
        Applique une force d'accélération vers l'avant.

        Args:
            entity: L'entité à accélérer
            delta_time: Temps écoulé
        """
        physics = entity.get_component(PhysicsComponent)
        transform = entity.get_component(TransformComponent)

        if physics and transform:
            forward = transform.get_forward_vector()
            acceleration_force = forward * self.force
            physics.apply_force(acceleration_force)

    def can_execute(self, entity: Entity) -> bool:
        """Vérifie que l'entité a les composants nécessaires."""
        return (
            entity.has_component(PhysicsComponent) and
            entity.has_component(TransformComponent)
        )


class BrakeCommand(BaseCommand):
    """Commande pour freiner."""

    def __init__(self, force: float = 1500.0, priority: int = 15) -> None:
        """
        Initialise la commande de freinage.

        Args:
            force: Force de freinage (Newtons)
            priority: Priorité d'exécution (plus haute que l'accélération)
        """
        super().__init__("Brake", priority)
        self.force: float = force

    def execute(self, entity: Entity, delta_time: float) -> None:
        """
        Applique une force de freinage opposée à la vélocité.

        Args:
            entity: L'entité à freiner
            delta_time: Temps écoulé
        """
        physics = entity.get_component(PhysicsComponent)

        if physics and physics.get_speed() > 10.0:
            # Applique une force opposée à la direction du mouvement
            brake_direction = physics.velocity.normalize() * -1
            brake_force = brake_direction * self.force
            physics.apply_force(brake_force)

    def can_execute(self, entity: Entity) -> bool:
        """Vérifie que l'entité a les composants nécessaires."""
        return entity.has_component(PhysicsComponent)


class TurnLeftCommand(BaseCommand):
    """Commande pour tourner à gauche."""

    def __init__(
        self,
        turn_speed_slow: float = 4.0,
        turn_speed_fast: float = 1.5,
        speed_threshold: float = 200.0,
        priority: int = 5
    ) -> None:
        """
        Initialise la commande de rotation à gauche.

        Args:
            turn_speed_slow: Vitesse de rotation à basse vitesse (rad/s)
            turn_speed_fast: Vitesse de rotation à haute vitesse (rad/s)
            speed_threshold: Seuil de transition
            priority: Priorité d'exécution
        """
        super().__init__("TurnLeft", priority)
        self.turn_speed_slow: float = turn_speed_slow
        self.turn_speed_fast: float = turn_speed_fast
        self.speed_threshold: float = speed_threshold

    def execute(self, entity: Entity, delta_time: float) -> None:
        """
        Applique une rotation à gauche avec rayon de braquage variable.

        Args:
            entity: L'entité à faire tourner
            delta_time: Temps écoulé
        """
        physics = entity.get_component(PhysicsComponent)
        transform = entity.get_component(TransformComponent)

        if physics and transform:
            # Calcule la vitesse de rotation basée sur la vitesse actuelle
            current_speed = physics.get_speed()
            speed_ratio = min(current_speed / self.speed_threshold, 1.0)

            # Interpolation: rotation rapide à basse vitesse, lente à haute vitesse
            turn_speed = self.turn_speed_slow + (
                self.turn_speed_fast - self.turn_speed_slow
            ) * speed_ratio

            # Applique la rotation
            rotation_delta = -turn_speed * delta_time
            transform.rotate(rotation_delta)

    def can_execute(self, entity: Entity) -> bool:
        """Vérifie que l'entité a les composants nécessaires."""
        return (
            entity.has_component(PhysicsComponent) and
            entity.has_component(TransformComponent)
        )


class TurnRightCommand(BaseCommand):
    """Commande pour tourner à droite."""

    def __init__(
        self,
        turn_speed_slow: float = 4.0,
        turn_speed_fast: float = 1.5,
        speed_threshold: float = 200.0,
        priority: int = 5
    ) -> None:
        """
        Initialise la commande de rotation à droite.

        Args:
            turn_speed_slow: Vitesse de rotation à basse vitesse (rad/s)
            turn_speed_fast: Vitesse de rotation à haute vitesse (rad/s)
            speed_threshold: Seuil de transition
            priority: Priorité d'exécution
        """
        super().__init__("TurnRight", priority)
        self.turn_speed_slow: float = turn_speed_slow
        self.turn_speed_fast: float = turn_speed_fast
        self.speed_threshold: float = speed_threshold

    def execute(self, entity: Entity, delta_time: float) -> None:
        """
        Applique une rotation à droite avec rayon de braquage variable.

        Args:
            entity: L'entité à faire tourner
            delta_time: Temps écoulé
        """
        physics = entity.get_component(PhysicsComponent)
        transform = entity.get_component(TransformComponent)

        if physics and transform:
            # Calcule la vitesse de rotation basée sur la vitesse actuelle
            current_speed = physics.get_speed()
            speed_ratio = min(current_speed / self.speed_threshold, 1.0)

            # Interpolation
            turn_speed = self.turn_speed_slow + (
                self.turn_speed_fast - self.turn_speed_slow
            ) * speed_ratio

            # Applique la rotation (positive = droite)
            rotation_delta = turn_speed * delta_time
            transform.rotate(rotation_delta)

    def can_execute(self, entity: Entity) -> bool:
        """Vérifie que l'entité a les composants nécessaires."""
        return (
            entity.has_component(PhysicsComponent) and
            entity.has_component(TransformComponent)
        )


class SprintCommand(BaseCommand):
    """Commande pour sprinter (boost de vitesse temporaire)."""

    def __init__(self, boost_multiplier: float = 1.5, priority: int = 20) -> None:
        """
        Initialise la commande de sprint.

        Args:
            boost_multiplier: Multiplicateur de force pendant le sprint
            priority: Priorité d'exécution (très haute)
        """
        super().__init__("Sprint", priority)
        self.boost_multiplier: float = boost_multiplier

    def execute(self, entity: Entity, delta_time: float) -> None:
        """
        Applique un boost d'accélération temporaire.

        Args:
            entity: L'entité qui sprinte
            delta_time: Temps écoulé
        """
        physics = entity.get_component(PhysicsComponent)
        transform = entity.get_component(TransformComponent)

        if physics and transform:
            # Force de sprint plus élevée
            forward = transform.get_forward_vector()
            sprint_force = forward * (1200.0 * self.boost_multiplier)
            physics.apply_force(sprint_force)

    def can_execute(self, entity: Entity) -> bool:
        """Vérifie que l'entité a les composants nécessaires."""
        # TODO: Ajouter vérification de stamina dans les prompts futurs
        return (
            entity.has_component(PhysicsComponent) and
            entity.has_component(TransformComponent)
        )


class StopCommand(BaseCommand):
    """Commande pour arrêter complètement le mouvement."""

    def __init__(self, priority: int = 50) -> None:
        """
        Initialise la commande d'arrêt.

        Args:
            priority: Priorité d'exécution (très haute pour arrêt d'urgence)
        """
        super().__init__("Stop", priority)

    def execute(self, entity: Entity, delta_time: float) -> None:
        """
        Arrête tout mouvement de l'entité.

        Args:
            entity: L'entité à arrêter
            delta_time: Temps écoulé
        """
        physics = entity.get_component(PhysicsComponent)

        if physics:
            physics.stop()

    def can_execute(self, entity: Entity) -> bool:
        """Vérifie que l'entité a les composants nécessaires."""
        return entity.has_component(PhysicsComponent)


class ReverseCommand(BaseCommand):
    """Commande pour reculer."""

    def __init__(self, force: float = 600.0, priority: int = 12) -> None:
        """
        Initialise la commande de marche arrière.

        Args:
            force: Force de recul (Newtons)
            priority: Priorité d'exécution
        """
        super().__init__("Reverse", priority)
        self.force: float = force

    def execute(self, entity: Entity, delta_time: float) -> None:
        """
        Applique une force vers l'arrière.

        Args:
            entity: L'entité à faire reculer
            delta_time: Temps écoulé
        """
        physics = entity.get_component(PhysicsComponent)
        transform = entity.get_component(TransformComponent)

        if physics and transform:
            # Force vers l'arrière (50% de la force normale)
            backward = transform.get_forward_vector() * -1
            reverse_force = backward * (self.force * 0.5)
            physics.apply_force(reverse_force)

    def can_execute(self, entity: Entity) -> bool:
        """Vérifie que l'entité a les composants nécessaires."""
        return (
            entity.has_component(PhysicsComponent) and
            entity.has_component(TransformComponent)
        )
