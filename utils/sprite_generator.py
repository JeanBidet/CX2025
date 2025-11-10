"""
Sprite Generator - Génération procédurale de sprites pour tests.

Génère des sprites simples (formes géométriques) pour tester
le système d'animation sans avoir besoin d'assets graphiques.
"""

import pygame
from typing import Tuple
from config.constants import Colors


class SpriteGenerator:
    """
    Génère des sprites procéduraux pour les tests.

    Crée des sprites simples basés sur des formes géométriques
    avec différentes couleurs selon l'état.
    """

    @staticmethod
    def generate_riding_frames(
        width: int = 40,
        height: int = 60,
        color: Tuple[int, int, int] = Colors.CYAN,
        frame_count: int = 4
    ) -> list[pygame.Surface]:
        """
        Génère des frames d'animation de pédalage.

        Simule le pédalage en variant légèrement la forme.

        Args:
            width: Largeur du sprite
            height: Hauteur du sprite
            color: Couleur de base
            frame_count: Nombre de frames

        Returns:
            Liste de surfaces Pygame
        """
        frames = []

        for i in range(frame_count):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)

            # Corps (rectangle principal)
            body_rect = pygame.Rect(5, 10, width - 10, height - 20)
            pygame.draw.rect(surface, color, body_rect)

            # Tête (cercle)
            head_center = (width // 2, 8)
            pygame.draw.circle(surface, color, head_center, 6)

            # Jambes (simule pédalage avec variation)
            leg_offset = int(5 * (i / frame_count))
            pygame.draw.line(
                surface,
                color,
                (width // 2, height - 10),
                (width // 2 + leg_offset, height),
                3
            )

            frames.append(surface)

        return frames

    @staticmethod
    def generate_carrying_frames(
        width: int = 40,
        height: int = 60,
        color: Tuple[int, int, int] = Colors.YELLOW,
        frame_count: int = 4
    ) -> list[pygame.Surface]:
        """
        Génère des frames d'animation de portage.

        Simule la marche avec le vélo sur l'épaule.

        Args:
            width: Largeur du sprite
            height: Hauteur du sprite
            color: Couleur (différente pour indiquer l'état)
            frame_count: Nombre de frames

        Returns:
            Liste de surfaces Pygame
        """
        frames = []

        for i in range(frame_count):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)

            # Corps (plus vertical pour marche)
            body_rect = pygame.Rect(8, 12, width - 16, height - 24)
            pygame.draw.rect(surface, color, body_rect)

            # Tête
            head_center = (width // 2, 10)
            pygame.draw.circle(surface, color, head_center, 5)

            # Vélo sur l'épaule (rectangle incliné)
            bike_points = [
                (width - 8, 15),
                (width - 5, 18),
                (width - 12, 25),
                (width - 15, 22)
            ]
            pygame.draw.polygon(surface, Colors.WHITE, bike_points)

            # Jambes marchant (variation)
            leg_offset = int(4 * ((i % 2) * 2 - 1))
            pygame.draw.line(
                surface,
                color,
                (width // 2, height - 12),
                (width // 2 + leg_offset, height),
                3
            )

            frames.append(surface)

        return frames

    @staticmethod
    def generate_remounting_frames(
        width: int = 40,
        height: int = 60,
        color: Tuple[int, int, int] = Colors.GREEN,
        frame_count: int = 3
    ) -> list[pygame.Surface]:
        """
        Génère des frames d'animation de remontée.

        Animation one-shot de la remontée sur le vélo.

        Args:
            width: Largeur du sprite
            height: Hauteur du sprite
            color: Couleur
            frame_count: Nombre de frames

        Returns:
            Liste de surfaces Pygame
        """
        frames = []

        for i in range(frame_count):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)

            progress = i / max(1, frame_count - 1)

            # Corps (transition de vertical à horizontal)
            body_width = width - 10 - int(10 * progress)
            body_height = height - 20 + int(10 * progress)
            body_rect = pygame.Rect(
                5 + int(5 * progress),
                10 - int(5 * progress),
                body_width,
                body_height
            )
            pygame.draw.rect(surface, color, body_rect)

            # Tête
            head_y = 8 + int(2 * progress)
            head_center = (width // 2, head_y)
            pygame.draw.circle(surface, color, head_center, 6)

            frames.append(surface)

        return frames

    @staticmethod
    def generate_crashed_frames(
        width: int = 40,
        height: int = 60,
        color: Tuple[int, int, int] = Colors.RED,
        frame_count: int = 4
    ) -> list[pygame.Surface]:
        """
        Génère des frames d'animation de chute.

        Simule une rotation/chute avec teinte rouge.

        Args:
            width: Largeur du sprite
            height: Hauteur du sprite
            color: Couleur rouge pour crash
            frame_count: Nombre de frames

        Returns:
            Liste de surfaces Pygame
        """
        frames = []

        for i in range(frame_count):
            surface = pygame.Surface((width, height), pygame.SRCALPHA)

            # Angle de rotation progressif
            angle = 90 * (i / max(1, frame_count - 1))

            # Crée le sprite de base
            temp_surface = pygame.Surface((width, height), pygame.SRCALPHA)

            # Corps incliné
            body_rect = pygame.Rect(5, 10, width - 10, height - 20)
            pygame.draw.rect(temp_surface, color, body_rect)

            # Tête
            head_center = (width // 2, 8)
            pygame.draw.circle(temp_surface, color, head_center, 6)

            # Rotation du sprite
            rotated = pygame.transform.rotate(temp_surface, angle)

            # Centre le sprite rotaté
            rotated_rect = rotated.get_rect(center=(width // 2, height // 2))
            surface.blit(rotated, rotated_rect)

            # Effet de flash rouge (alpha blending)
            red_overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            alpha = int(100 * (1 - i / max(1, frame_count - 1)))
            red_overlay.fill((255, 0, 0, alpha))
            surface.blit(red_overlay, (0, 0))

            frames.append(surface)

        return frames

    @staticmethod
    def generate_static_sprite(
        width: int = 40,
        height: int = 60,
        color: Tuple[int, int, int] = Colors.WHITE
    ) -> pygame.Surface:
        """
        Génère un sprite statique simple.

        Args:
            width: Largeur
            height: Hauteur
            color: Couleur

        Returns:
            Surface Pygame
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Corps
        body_rect = pygame.Rect(5, 10, width - 10, height - 20)
        pygame.draw.rect(surface, color, body_rect)

        # Tête
        head_center = (width // 2, 8)
        pygame.draw.circle(surface, color, head_center, 6)

        return surface
