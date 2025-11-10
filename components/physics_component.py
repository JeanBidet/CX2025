"""
Physics Component - Gestion de la physique newtonienne pour une entité.

Ce composant implémente un moteur physique simple mais réaliste basé sur
les lois de Newton, avec gestion des forces, vélocité, accélération et drag.
"""

from components.icomponent import IComponent
from components.transform_component import TransformComponent
from utils.vector2 import Vector2


class PhysicsComponent(IComponent):
    """
    Composant gérant la physique d'une entité.

    Implémente les équations newtoniennes :
    - F = ma (Force = masse × accélération)
    - v = v0 + at (Vélocité = vélocité initiale + accélération × temps)
    - p = p0 + vt (Position = position initiale + vélocité × temps)

    Utilise l'intégration d'Euler pour la simplicité.
    """

    def __init__(
        self,
        owner,
        mass: float = 1.0,
        drag: float = 0.98,
        max_speed: float = 500.0,
        use_gravity: bool = False
    ) -> None:
        """
        Initialise le composant de physique.

        Args:
            owner: L'entité propriétaire
            mass: Masse de l'entité (kg)
            drag: Coefficient de traînée (0-1, plus proche de 1 = moins de résistance)
            max_speed: Vitesse maximale (pixels/seconde)
            use_gravity: Si vrai, applique la gravité
        """
        super().__init__(owner)

        # Propriétés physiques
        self.mass: float = mass
        self.drag: float = drag
        self.max_speed: float = max_speed
        self.use_gravity: bool = use_gravity

        # État dynamique
        self.velocity: Vector2 = Vector2.zero()
        self.acceleration: Vector2 = Vector2.zero()
        self._accumulated_forces: Vector2 = Vector2.zero()

        # Référence au TransformComponent
        self._transform: TransformComponent | None = None

    def init(self) -> None:
        """Initialise le composant et récupère les références nécessaires."""
        # Récupère le TransformComponent de l'entité
        self._transform = self.owner.get_component(TransformComponent)
        if self._transform is None:
            raise RuntimeError(
                f"PhysicsComponent requiert un TransformComponent sur l'entité {self.owner.name}"
            )

    def apply_force(self, force: Vector2) -> None:
        """
        Applique une force à l'entité.

        La force sera accumulée et appliquée lors du prochain update.

        Args:
            force: Force à appliquer (Newtons)
        """
        self._accumulated_forces = self._accumulated_forces + force

    def apply_impulse(self, impulse: Vector2) -> None:
        """
        Applique une impulsion instantanée à l'entité.

        Une impulsion modifie directement la vélocité sans passer par l'accélération.

        Args:
            impulse: Impulsion à appliquer (kg⋅m/s)
        """
        self.velocity = self.velocity + impulse / self.mass

    def set_velocity(self, velocity: Vector2) -> None:
        """
        Définit directement la vélocité de l'entité.

        Args:
            velocity: Nouvelle vélocité (pixels/seconde)
        """
        self.velocity = velocity

    def add_velocity(self, delta_velocity: Vector2) -> None:
        """
        Ajoute une vélocité à la vélocité actuelle.

        Args:
            delta_velocity: Changement de vélocité (pixels/seconde)
        """
        self.velocity = self.velocity + delta_velocity

    def update(self, delta_time: float) -> None:
        """
        Met à jour la physique de l'entité.

        Applique les forces, calcule l'accélération, met à jour la vélocité
        et la position selon l'intégration d'Euler.

        Args:
            delta_time: Temps écoulé depuis la dernière frame (secondes)
        """
        if self._transform is None:
            return

        # 1. Calcul de l'accélération selon F = ma → a = F/m
        self.acceleration = self._accumulated_forces / self.mass

        # 2. Application de la gravité si activée
        if self.use_gravity:
            from config.game_config import GameConfig
            gravity_force = Vector2(0, GameConfig.GRAVITY * self.mass)
            self.acceleration = self.acceleration + gravity_force / self.mass

        # 3. Mise à jour de la vélocité : v = v0 + at
        self.velocity = self.velocity + self.acceleration * delta_time

        # 4. Application du drag (résistance de l'air/friction)
        # Utilise une décroissance exponentielle pour un effet naturel
        drag_factor = pow(self.drag, delta_time * 60)  # Normalise pour 60 FPS
        self.velocity = self.velocity * drag_factor

        # 5. Limitation de la vitesse maximale
        speed = self.velocity.length()
        if speed > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        # 6. Mise à jour de la position : p = p0 + vt
        displacement = self.velocity * delta_time
        self._transform.translate(displacement)

        # 7. Réinitialisation des forces accumulées pour la prochaine frame
        self._accumulated_forces = Vector2.zero()

    def stop(self) -> None:
        """Arrête complètement le mouvement de l'entité."""
        self.velocity = Vector2.zero()
        self.acceleration = Vector2.zero()
        self._accumulated_forces = Vector2.zero()

    def get_kinetic_energy(self) -> float:
        """
        Calcule l'énergie cinétique de l'entité.

        Formule : E = 1/2 × m × v²

        Returns:
            Énergie cinétique (Joules)
        """
        speed_squared = self.velocity.length_squared()
        return 0.5 * self.mass * speed_squared

    def get_momentum(self) -> Vector2:
        """
        Calcule le momentum (quantité de mouvement) de l'entité.

        Formule : p = m × v

        Returns:
            Momentum (kg⋅m/s)
        """
        return self.velocity * self.mass

    def is_moving(self, threshold: float = 0.1) -> bool:
        """
        Vérifie si l'entité est en mouvement.

        Args:
            threshold: Seuil de vitesse en dessous duquel on considère l'entité immobile

        Returns:
            True si l'entité bouge, False sinon
        """
        return self.velocity.length() > threshold

    def get_speed(self) -> float:
        """
        Retourne la vitesse actuelle (magnitude de la vélocité).

        Returns:
            Vitesse en pixels/seconde
        """
        return self.velocity.length()

    def destroy(self) -> None:
        """Nettoie les ressources du composant."""
        self._transform = None

    def __repr__(self) -> str:
        """Représentation string du composant."""
        return (
            f"PhysicsComponent(mass={self.mass}kg, "
            f"velocity={self.velocity}, speed={self.get_speed():.1f}px/s)"
        )
