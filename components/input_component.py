"""
Input Component - Gestion des contrôles clavier pour un cycliste.

Ce composant lit les entrées du joueur et applique les forces appropriées
au PhysicsComponent pour créer un contrôle réaliste avec inertie.
"""

import pygame
import math
from components.icomponent import IComponent
from components.physics_component import PhysicsComponent
from components.transform_component import TransformComponent
from utils.vector2 import Vector2


class InputComponent(IComponent):
    """
    Composant gérant les entrées clavier et leur conversion en forces physiques.

    Ce composant permet un contrôle progressif et réaliste du cycliste avec :
    - Accélération progressive vers l'avant
    - Freinage graduel
    - Rotation dépendante de la vitesse (rayon de braquage)
    - Interpolation douce de la rotation
    """

    def __init__(
        self,
        owner,
        acceleration_force: float = 800.0,
        brake_force: float = 1200.0,
        turn_speed_slow: float = 3.0,
        turn_speed_fast: float = 1.0,
        speed_threshold: float = 100.0
    ) -> None:
        """
        Initialise le composant d'entrée.

        Args:
            owner: L'entité propriétaire
            acceleration_force: Force d'accélération (Newtons)
            brake_force: Force de freinage (Newtons)
            turn_speed_slow: Vitesse de rotation à basse vitesse (radians/seconde)
            turn_speed_fast: Vitesse de rotation à haute vitesse (radians/seconde)
            speed_threshold: Seuil de vitesse pour transition rotation (pixels/seconde)
        """
        super().__init__(owner)

        # Paramètres de contrôle
        self.acceleration_force: float = acceleration_force
        self.brake_force: float = brake_force
        self.turn_speed_slow: float = turn_speed_slow
        self.turn_speed_fast: float = turn_speed_fast
        self.speed_threshold: float = speed_threshold

        # Mode de contrôle
        self.use_rotation_mode: bool = True  # True = rotation tank, False = rotation vers mouvement

        # Composants requis
        self._physics: PhysicsComponent | None = None
        self._transform: TransformComponent | None = None

        # État interne
        self._target_rotation: float = 0.0

    def init(self) -> None:
        """Initialise le composant et récupère les références nécessaires."""
        self._physics = self.owner.get_component(PhysicsComponent)
        self._transform = self.owner.get_component(TransformComponent)

        if self._physics is None:
            raise RuntimeError(
                f"InputComponent requiert un PhysicsComponent sur l'entité {self.owner.name}"
            )
        if self._transform is None:
            raise RuntimeError(
                f"InputComponent requiert un TransformComponent sur l'entité {self.owner.name}"
            )

        # Initialise la rotation cible
        self._target_rotation = self._transform.rotation

    def update(self, delta_time: float) -> None:
        """
        Met à jour les contrôles et applique les forces.

        Args:
            delta_time: Temps écoulé depuis la dernière frame (secondes)
        """
        if self._physics is None or self._transform is None:
            return

        # Lecture des touches
        keys = pygame.key.get_pressed()

        # Calcul de la direction de rotation demandée
        turn_input = 0.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            turn_input = -1.0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            turn_input = 1.0

        # Gestion de la rotation avec rayon de braquage variable
        self._handle_rotation(turn_input, delta_time)

        # Gestion de l'accélération et du freinage
        self._handle_acceleration(keys, delta_time)

    def _handle_rotation(self, turn_input: float, delta_time: float) -> None:
        """
        Gère la rotation du cycliste avec rayon de braquage réaliste.

        Args:
            turn_input: Input de rotation (-1 à 1)
            delta_time: Temps écoulé
        """
        if self._physics is None or self._transform is None:
            return

        # Calcule la vitesse de rotation basée sur la vitesse actuelle
        current_speed = self._physics.get_speed()
        speed_ratio = min(current_speed / self.speed_threshold, 1.0)

        # Interpolation entre vitesse de rotation lente et rapide
        # À basse vitesse : rotation rapide (manœuvrable)
        # À haute vitesse : rotation lente (rayon de braquage large)
        turn_speed = self.turn_speed_slow + (self.turn_speed_fast - self.turn_speed_slow) * speed_ratio

        # Application de la rotation
        if turn_input != 0:
            rotation_delta = turn_input * turn_speed * delta_time
            self._transform.rotate(rotation_delta)
            self._target_rotation = self._transform.rotation

        # Si en mouvement, oriente progressivement vers la direction du mouvement
        if not self.use_rotation_mode and self._physics.is_moving(threshold=10.0):
            # Calcule l'angle de la vélocité
            velocity_angle = self._physics.velocity.angle()

            # Interpolation douce vers l'angle de mouvement
            angle_diff = self._normalize_angle(velocity_angle - self._transform.rotation)

            # Limite la vitesse de rotation automatique
            max_auto_rotation = self.turn_speed_slow * delta_time
            angle_correction = max(min(angle_diff, max_auto_rotation), -max_auto_rotation)

            self._transform.rotate(angle_correction)

    def _handle_acceleration(self, keys: pygame.key.ScancodeWrapper, delta_time: float) -> None:
        """
        Gère l'accélération et le freinage du cycliste.

        Args:
            keys: État des touches du clavier
            delta_time: Temps écoulé
        """
        if self._physics is None or self._transform is None:
            return

        # Détecte l'input avant/arrière
        forward_input = 0.0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            forward_input = 1.0
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            forward_input = -1.0

        # Calcule la direction avant basée sur la rotation actuelle
        forward_direction = self._transform.get_forward_vector()

        if forward_input > 0:
            # Accélération vers l'avant
            acceleration = forward_direction * self.acceleration_force * forward_input
            self._physics.apply_force(acceleration)

        elif forward_input < 0:
            # Freinage ou marche arrière
            # Si on a de la vitesse vers l'avant, on freine
            current_speed = self._physics.get_speed()
            if current_speed > 10.0:
                # Freinage : applique une force opposée à la vélocité
                brake_direction = self._physics.velocity.normalize() * -1
                brake = brake_direction * self.brake_force
                self._physics.apply_force(brake)
            else:
                # Marche arrière lente
                backward = forward_direction * self.acceleration_force * forward_input * 0.5
                self._physics.apply_force(backward)

    def _normalize_angle(self, angle: float) -> float:
        """
        Normalise un angle entre -π et π.

        Args:
            angle: Angle en radians

        Returns:
            Angle normalisé
        """
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

    def set_control_mode_tank(self) -> None:
        """Active le mode de contrôle tank (rotation indépendante)."""
        self.use_rotation_mode = True

    def set_control_mode_auto_orient(self) -> None:
        """Active le mode de contrôle avec orientation automatique vers le mouvement."""
        self.use_rotation_mode = False

    def destroy(self) -> None:
        """Nettoie les ressources du composant."""
        self._physics = None
        self._transform = None

    def __repr__(self) -> str:
        """Représentation string du composant."""
        mode = "tank" if self.use_rotation_mode else "auto-orient"
        return f"InputComponent(mode={mode})"
