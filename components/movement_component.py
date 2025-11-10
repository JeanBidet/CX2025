"""
Composant de mouvement pour contrôler le déplacement d'une entité.

Ce composant gère les déplacements au clavier et applique la vélocité
à la position de l'entité.
"""

import pygame
from components.icomponent import IComponent
from utils.vector2 import Vector2


class MovementComponent(IComponent):
    """
    Composant gérant le déplacement d'une entité via le clavier.

    Ce composant sera étendu dans les futurs prompts pour gérer
    l'inertie, la friction, etc.
    """

    def __init__(self, owner, speed: float = 200.0) -> None:
        """
        Initialise le composant de mouvement.

        Args:
            owner: L'entité propriétaire
            speed: Vitesse de déplacement en pixels par seconde
        """
        super().__init__(owner)
        self.speed: float = speed
        self.velocity: Vector2 = Vector2.zero()

    def init(self) -> None:
        """Initialise le composant."""
        pass

    def update(self, delta_time: float) -> None:
        """
        Met à jour le mouvement en fonction des touches pressées.

        Args:
            delta_time: Temps écoulé depuis la dernière frame en secondes
        """
        # Récupère l'état des touches
        keys = pygame.key.get_pressed()

        # Calcule la direction de mouvement
        direction = Vector2.zero()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y += 1

        # Normalise la direction pour éviter des déplacements plus rapides en diagonale
        if direction.length() > 0:
            direction = direction.normalize()

        # Calcule la vélocité
        self.velocity = direction * self.speed

        # Applique le mouvement à la position de l'entité
        self.owner.position = self.owner.position + self.velocity * delta_time

    def destroy(self) -> None:
        """Nettoie les ressources du composant."""
        pass

    def __repr__(self) -> str:
        """Représentation string du composant."""
        return f"MovementComponent(speed={self.speed}, velocity={self.velocity})"
