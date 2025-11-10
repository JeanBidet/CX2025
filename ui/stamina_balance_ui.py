"""
Stamina Balance UI - Gestionnaire d'interface pour l'endurance et l'équilibre.

Ce module gère l'affichage des jauges d'endurance, d'équilibre et de fatigue,
ainsi que les indicateurs contextuels (terrain, pente, etc.).
"""

import pygame
from typing import Optional, Tuple
from ui.gauge_widget import GaugeWidget
from components.stamina_component import StaminaComponent
from components.balance_component import BalanceComponent
from config.constants import Colors, PerformanceZone
from config.game_config import GameConfig
from systems.terrain_data import TerrainData, TerrainType


class StaminaBalanceUI:
    """
    Gestionnaire d'interface pour les jauges d'endurance et d'équilibre.

    Affiche :
    - Barre d'endurance avec couleur selon zone de performance
    - Barre d'équilibre avec effet de clignotement si critique
    - Indicateur de fatigue cumulative
    - Indicateurs contextuels (terrain, pente, grip)
    """

    def __init__(self) -> None:
        """Initialise le gestionnaire d'UI."""
        # Position et dimensions des jauges
        self._stamina_gauge = GaugeWidget(
            position=(20, 20),
            size=(200, 20),
            label="Endurance",
            max_value=GameConfig.STAMINA_MAX,
            color=Colors.GREEN,
        )

        self._balance_gauge = GaugeWidget(
            position=(20, 50),
            size=(200, 15),
            label="Équilibre",
            max_value=GameConfig.BALANCE_MAX,
            color=(0, 100, 255),  # Bleu
        )

        self._fatigue_gauge = GaugeWidget(
            position=(20, 75),
            size=(150, 10),
            label="Fatigue",
            max_value=GameConfig.FATIGUE_MAX,
            color=Colors.GREEN,
            show_percentage=True,
            font_size=14,
        )

        # Police pour les indicateurs contextuels
        self._context_font: Optional[pygame.font.Font] = None
        self._small_font: Optional[pygame.font.Font] = None

        # Frame counter pour animations
        self._frame_count = 0

    def update(
        self,
        stamina_component: Optional[StaminaComponent],
        balance_component: Optional[BalanceComponent],
    ) -> None:
        """
        Met à jour les valeurs des jauges.

        Args:
            stamina_component: Composant d'endurance à afficher
            balance_component: Composant d'équilibre à afficher
        """
        # Mise à jour de la jauge d'endurance
        if stamina_component is not None:
            self._stamina_gauge.set_value(stamina_component.current_stamina)

            # Couleur selon la zone de performance
            zone = stamina_component.get_performance_zone()
            self._stamina_gauge.set_color(self._get_zone_color(zone))

            # Clignotement en zone critique/épuisée
            should_blink = zone in [PerformanceZone.CRITICAL, PerformanceZone.EXHAUSTED]
            self._stamina_gauge.set_blink_effect(should_blink)

            # Mise à jour de la jauge de fatigue
            self._fatigue_gauge.set_value(stamina_component.fatigue_level)
            fatigue_percentage = stamina_component.get_fatigue_percentage()
            self._fatigue_gauge.set_color_by_percentage(
                100.0 - fatigue_percentage,  # Inverser : plus de fatigue = rouge
                thresholds={
                    70.0: Colors.GREEN,
                    50.0: Colors.YELLOW,
                    30.0: (255, 165, 0),  # Orange
                    0.0: Colors.RED,
                }
            )

        # Mise à jour de la jauge d'équilibre
        if balance_component is not None:
            self._balance_gauge.set_value(balance_component.current_balance)

            # Couleur selon le niveau de stabilité
            balance_percentage = balance_component.get_percentage()
            if balance_percentage > 60.0:
                self._balance_gauge.set_color((0, 100, 255))  # Bleu
            elif balance_percentage > balance_component.critical_threshold:
                self._balance_gauge.set_color(Colors.YELLOW)
            else:
                self._balance_gauge.set_color(Colors.RED)

            # Clignotement rapide si critique
            self._balance_gauge.set_blink_effect(balance_component.is_critical())

    def render(
        self,
        screen: pygame.Surface,
        current_terrain: Optional[TerrainData] = None,
        show_context_info: bool = True,
    ) -> None:
        """
        Affiche les jauges et indicateurs à l'écran.

        Args:
            screen: Surface pygame où dessiner
            current_terrain: Données du terrain actuel (pour contexte)
            show_context_info: Afficher les infos contextuelles
        """
        self._frame_count += 1

        # Afficher les jauges
        self._stamina_gauge.render(screen, self._frame_count)
        self._balance_gauge.render(screen, self._frame_count)
        self._fatigue_gauge.render(screen, self._frame_count)

        # Afficher les indicateurs contextuels
        if show_context_info and current_terrain is not None:
            self._render_context_indicators(screen, current_terrain)

    def _render_context_indicators(
        self, screen: pygame.Surface, terrain: TerrainData
    ) -> None:
        """
        Affiche les indicateurs de contexte (terrain, pente, grip).

        Args:
            screen: Surface pygame où dessiner
            terrain: Données du terrain actuel
        """
        # Initialiser les polices si nécessaire
        if self._context_font is None:
            self._context_font = pygame.font.Font(None, 20)
        if self._small_font is None:
            self._small_font = pygame.font.Font(None, 16)

        # Position de départ dans le coin supérieur droit
        x_start = GameConfig.WINDOW_WIDTH - 220
        y_start = 20

        # Fond semi-transparent pour les indicateurs
        info_rect = pygame.Rect(x_start - 10, y_start - 5, 210, 100)
        surface = pygame.Surface((info_rect.width, info_rect.height))
        surface.set_alpha(180)
        surface.fill(Colors.DARK_GRAY)
        screen.blit(surface, info_rect.topleft)

        # Bordure
        pygame.draw.rect(screen, Colors.WHITE, info_rect, 2)

        # 1. Type de terrain avec couleur
        terrain_text = f"Terrain: {terrain.name}"
        terrain_surface = self._context_font.render(terrain_text, True, Colors.WHITE)
        screen.blit(terrain_surface, (x_start, y_start))

        # Petite pastille de couleur du terrain
        pygame.draw.circle(screen, terrain.color, (x_start - 15, y_start + 8), 6)

        # 2. Grip (adhérence)
        y_start += 25
        grip_percentage = terrain.grip_level * 100.0
        grip_text = f"Grip: {grip_percentage:.0f}%"
        grip_color = Colors.GREEN if terrain.grip_level > 0.7 else Colors.YELLOW if terrain.grip_level > 0.4 else Colors.RED
        grip_surface = self._small_font.render(grip_text, True, grip_color)
        screen.blit(grip_surface, (x_start, y_start))

        # 3. Pente (slope)
        y_start += 20
        slope_text = f"Pente: {terrain.slope:+.1f}°"
        slope_color = Colors.RED if terrain.slope > 10 else Colors.YELLOW if terrain.slope > 5 else Colors.GREEN
        slope_surface = self._small_font.render(slope_text, True, slope_color)
        screen.blit(slope_surface, (x_start, y_start))

        # Flèche indicatrice de pente
        if abs(terrain.slope) > 1.0:
            arrow_x = x_start + 120
            arrow_y = y_start + 10
            if terrain.slope > 0:
                # Montée : flèche vers le haut
                self._draw_arrow_up(screen, arrow_x, arrow_y, Colors.RED)
            else:
                # Descente : flèche vers le bas
                self._draw_arrow_down(screen, arrow_x, arrow_y, Colors.GREEN)

        # 4. Camber (inclinaison latérale)
        y_start += 20
        if abs(terrain.camber) > 0.5:
            camber_text = f"Dévers: {terrain.camber:+.1f}°"
            camber_color = Colors.YELLOW if abs(terrain.camber) > 5 else Colors.WHITE
            camber_surface = self._small_font.render(camber_text, True, camber_color)
            screen.blit(camber_surface, (x_start, y_start))

            # Triangle d'avertissement si fort dévers
            if abs(terrain.camber) > 5:
                self._draw_warning_icon(screen, x_start + 120, y_start + 8)

    def _draw_arrow_up(self, screen: pygame.Surface, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """Dessine une flèche vers le haut."""
        points = [
            (x, y - 8),       # Sommet
            (x - 6, y + 2),   # Bas gauche
            (x + 6, y + 2),   # Bas droit
        ]
        pygame.draw.polygon(screen, color, points)

    def _draw_arrow_down(self, screen: pygame.Surface, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """Dessine une flèche vers le bas."""
        points = [
            (x, y + 8),       # Sommet
            (x - 6, y - 2),   # Haut gauche
            (x + 6, y - 2),   # Haut droit
        ]
        pygame.draw.polygon(screen, color, points)

    def _draw_warning_icon(self, screen: pygame.Surface, x: int, y: int) -> None:
        """Dessine une icône d'avertissement (triangle avec !)."""
        # Triangle
        points = [
            (x, y - 6),           # Sommet
            (x - 6, y + 6),       # Bas gauche
            (x + 6, y + 6),       # Bas droit
        ]
        pygame.draw.polygon(screen, Colors.YELLOW, points)
        pygame.draw.polygon(screen, Colors.BLACK, points, 2)

        # Point d'exclamation
        if self._small_font is not None:
            exclamation = self._small_font.render("!", True, Colors.BLACK)
            exclamation_rect = exclamation.get_rect(center=(x, y + 2))
            screen.blit(exclamation, exclamation_rect)

    def _get_zone_color(self, zone: PerformanceZone) -> Tuple[int, int, int]:
        """
        Retourne la couleur associée à une zone de performance.

        Args:
            zone: Zone de performance

        Returns:
            Couleur RGB
        """
        zone_colors = {
            PerformanceZone.OPTIMAL: Colors.GREEN,
            PerformanceZone.MODERATE: Colors.YELLOW,
            PerformanceZone.CRITICAL: (255, 165, 0),  # Orange
            PerformanceZone.EXHAUSTED: Colors.RED,
        }
        return zone_colors.get(zone, Colors.WHITE)

    def reset(self) -> None:
        """Réinitialise l'interface (frame counter, etc.)."""
        self._frame_count = 0

    def __repr__(self) -> str:
        """Représentation string de l'UI."""
        return f"StaminaBalanceUI(frame={self._frame_count})"
