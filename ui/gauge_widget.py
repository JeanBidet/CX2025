"""
Gauge Widget - Widget réutilisable pour afficher des jauges à l'écran.

Ce widget permet d'afficher des barres de progression avec différents styles,
couleurs, et effets visuels (clignotement, dégradés, etc.).
"""

import pygame
from typing import Tuple, Optional
from config.constants import Colors


class GaugeWidget:
    """
    Widget de jauge réutilisable.

    Affiche une barre de progression horizontale avec :
    - Fond, remplissage, bordure
    - Couleur dynamique selon la valeur
    - Label et texte de valeur
    - Effet de clignotement optionnel
    - Support de valeurs min/max personnalisées
    """

    def __init__(
        self,
        position: Tuple[int, int],
        size: Tuple[int, int],
        label: str,
        max_value: float = 100.0,
        min_value: float = 0.0,
        color: Tuple[int, int, int] = Colors.GREEN,
        background_color: Tuple[int, int, int] = Colors.DARK_GRAY,
        border_color: Tuple[int, int, int] = Colors.BLACK,
        border_width: int = 2,
        show_percentage: bool = True,
        font_size: int = 16,
    ) -> None:
        """
        Initialise le widget de jauge.

        Args:
            position: Position (x, y) du coin supérieur gauche
            size: Taille (largeur, hauteur) de la jauge
            label: Texte du label
            max_value: Valeur maximale
            min_value: Valeur minimale
            color: Couleur du remplissage
            background_color: Couleur du fond
            border_color: Couleur de la bordure
            border_width: Épaisseur de la bordure
            show_percentage: Afficher le pourcentage
            font_size: Taille de la police
        """
        self.position = position
        self.size = size
        self.label = label
        self.max_value = max_value
        self.min_value = min_value
        self.current_value = max_value

        # Couleurs
        self.color = color
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width

        # Options d'affichage
        self.show_percentage = show_percentage

        # Police (initialisée lors du premier render)
        self._font: Optional[pygame.font.Font] = None
        self._font_size = font_size

        # Cache pour le texte rendu (optimisation)
        self._cached_text_surface: Optional[pygame.Surface] = None
        self._cached_value: Optional[float] = None

        # Effet de clignotement
        self._blink_enabled = False
        self._blink_visible = True

    def render(self, screen: pygame.Surface, frame_count: int = 0) -> None:
        """
        Affiche la jauge à l'écran.

        Args:
            screen: Surface pygame où dessiner
            frame_count: Compteur de frames (pour animations)
        """
        x, y = self.position
        width, height = self.size

        # Gérer le clignotement
        if self._blink_enabled:
            # Clignotement toutes les 15 frames
            self._blink_visible = (frame_count % 30) < 15
            if not self._blink_visible:
                # Ne rien afficher pendant le clignotement "off"
                return

        # 1. Dessiner le fond
        background_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, self.background_color, background_rect)

        # 2. Dessiner le remplissage
        fill_percentage = self._get_fill_percentage()
        fill_width = int(width * fill_percentage)

        if fill_width > 0:
            fill_rect = pygame.Rect(x, y, fill_width, height)
            pygame.draw.rect(screen, self.color, fill_rect)

        # 3. Dessiner la bordure
        pygame.draw.rect(screen, self.border_color, background_rect, self.border_width)

        # 4. Afficher le label et la valeur
        self._render_text(screen)

    def _get_fill_percentage(self) -> float:
        """
        Calcule le pourcentage de remplissage.

        Returns:
            Pourcentage entre 0.0 et 1.0
        """
        value_range = self.max_value - self.min_value
        if value_range <= 0:
            return 1.0

        clamped_value = max(self.min_value, min(self.max_value, self.current_value))
        return (clamped_value - self.min_value) / value_range

    def _render_text(self, screen: pygame.Surface) -> None:
        """
        Affiche le texte du label et de la valeur.

        Args:
            screen: Surface pygame où dessiner
        """
        # Initialiser la police si nécessaire
        if self._font is None:
            self._font = pygame.font.Font(None, self._font_size)

        # Créer le texte avec mise en cache
        if self._cached_text_surface is None or self._cached_value != self.current_value:
            if self.show_percentage:
                percentage = self._get_fill_percentage() * 100.0
                text = f"{self.label}: {percentage:.0f}%"
            else:
                text = f"{self.label}: {self.current_value:.1f}"

            self._cached_text_surface = self._font.render(text, True, Colors.WHITE)
            self._cached_value = self.current_value

        # Position du texte : centré verticalement, à gauche de la jauge
        text_x = self.position[0] + 5
        text_y = self.position[1] + (self.size[1] - self._cached_text_surface.get_height()) // 2

        screen.blit(self._cached_text_surface, (text_x, text_y))

    def set_value(self, value: float) -> None:
        """
        Définit la valeur actuelle de la jauge.

        Args:
            value: Nouvelle valeur
        """
        self.current_value = max(self.min_value, min(self.max_value, value))

    def set_color(self, color: Tuple[int, int, int]) -> None:
        """
        Définit la couleur du remplissage.

        Args:
            color: Couleur RGB
        """
        self.color = color

    def set_color_by_percentage(self, percentage: float, thresholds: Optional[dict] = None) -> None:
        """
        Définit la couleur selon le pourcentage.

        Args:
            percentage: Pourcentage (0-100)
            thresholds: Dictionnaire de seuils personnalisés {valeur: couleur}
                       Par défaut : >70=vert, >40=jaune, >20=orange, <=20=rouge
        """
        if thresholds is None:
            thresholds = {
                70.0: Colors.GREEN,
                40.0: Colors.YELLOW,
                20.0: (255, 165, 0),  # Orange
                0.0: Colors.RED,
            }

        # Trouver la couleur appropriée
        for threshold in sorted(thresholds.keys(), reverse=True):
            if percentage >= threshold:
                self.color = thresholds[threshold]
                break

    def set_blink_effect(self, enabled: bool) -> None:
        """
        Active ou désactive l'effet de clignotement.

        Args:
            enabled: True pour activer le clignotement
        """
        self._blink_enabled = enabled

    def get_percentage(self) -> float:
        """
        Obtient le pourcentage de remplissage.

        Returns:
            Pourcentage (0.0 à 100.0)
        """
        return self._get_fill_percentage() * 100.0

    def __repr__(self) -> str:
        """Représentation string du widget."""
        return (
            f"GaugeWidget("
            f"label={self.label}, "
            f"value={self.current_value:.1f}/{self.max_value:.1f}, "
            f"pos={self.position})"
        )


class CircularGaugeWidget:
    """
    Widget de jauge circulaire (pour variété visuelle future).

    Note: Implémentation de base, peut être étendue selon les besoins.
    """

    def __init__(
        self,
        center: Tuple[int, int],
        radius: int,
        label: str,
        max_value: float = 100.0,
        color: Tuple[int, int, int] = Colors.GREEN,
    ) -> None:
        """
        Initialise la jauge circulaire.

        Args:
            center: Centre du cercle (x, y)
            radius: Rayon du cercle
            label: Texte du label
            max_value: Valeur maximale
            color: Couleur de l'arc
        """
        self.center = center
        self.radius = radius
        self.label = label
        self.max_value = max_value
        self.current_value = max_value
        self.color = color

        self._font: Optional[pygame.font.Font] = None

    def render(self, screen: pygame.Surface, frame_count: int = 0) -> None:
        """
        Affiche la jauge circulaire.

        Args:
            screen: Surface pygame où dessiner
            frame_count: Compteur de frames
        """
        # Cercle de fond
        pygame.draw.circle(screen, Colors.DARK_GRAY, self.center, self.radius, 3)

        # Arc de progression (simplifié - pygame ne supporte pas nativement les arcs partiels)
        # Pour une vraie implémentation, utiliser pygame.gfxdraw ou dessiner pixel par pixel
        percentage = (self.current_value / self.max_value)
        if percentage > 0:
            # Cercle intérieur proportionnel
            inner_radius = int(self.radius * percentage)
            if inner_radius > 0:
                pygame.draw.circle(screen, self.color, self.center, inner_radius)

        # Texte central
        if self._font is None:
            self._font = pygame.font.Font(None, 20)

        text = f"{int(percentage * 100)}%"
        text_surface = self._font.render(text, True, Colors.WHITE)
        text_rect = text_surface.get_rect(center=self.center)
        screen.blit(text_surface, text_rect)

    def set_value(self, value: float) -> None:
        """
        Définit la valeur actuelle.

        Args:
            value: Nouvelle valeur
        """
        self.current_value = max(0.0, min(self.max_value, value))
