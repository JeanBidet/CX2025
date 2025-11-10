"""
Stamina Component - Gestion de l'endurance du cycliste.

Ce composant gère l'endurance (stamina) du cycliste avec un système de drain
dynamique basé sur le contexte (terrain, vitesse, pente), ainsi qu'un système
de fatigue cumulative qui affecte la capacité de récupération.
"""

from components.icomponent import IComponent
from components.transform_component import TransformComponent
from components.physics_component import PhysicsComponent
from config.game_config import GameConfig
from config.constants import PerformanceZone
from systems.terrain_manager import TerrainManager
from systems.terrain_data import TerrainData
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity


class StaminaComponent(IComponent):
    """
    Composant gérant l'endurance du cycliste.

    L'endurance est consommée par l'effort et se régénère au repos (mode portage).
    Le drain est influencé par :
    - La vitesse actuelle
    - Le type de terrain (multiplicateur du TerrainData)
    - La pente (montées drainent plus)
    - La fatigue cumulative (réduit la récupération)

    Les zones de performance modifient les capacités du cycliste :
    - OPTIMAL (70-100%) : performance normale
    - MODERATE (40-70%) : -10% vitesse max
    - CRITICAL (10-40%) : -30% vitesse, contrôle réduit
    - EXHAUSTED (0-10%) : -50% vitesse, risque de chute élevé
    """

    def __init__(self, owner: "Entity") -> None:
        """
        Initialise le composant d'endurance.

        Args:
            owner: L'entité propriétaire (le cycliste)
        """
        super().__init__(owner)

        # Valeurs actuelles
        self.current_stamina: float = GameConfig.STAMINA_MAX
        self.max_stamina: float = GameConfig.STAMINA_MAX
        self.fatigue_level: float = 0.0  # 0 à FATIGUE_MAX

        # Taux de drain et récupération
        self.base_drain_rate: float = GameConfig.STAMINA_BASE_DRAIN_RATE
        self.recovery_rate: float = GameConfig.STAMINA_RECOVERY_RATE

        # Zone de performance actuelle
        self._current_zone: PerformanceZone = PerformanceZone.OPTIMAL

        # Références aux composants requis
        self._transform: TransformComponent | None = None
        self._physics: PhysicsComponent | None = None

        # État de récupération
        self._is_recovering: bool = False

    def init(self) -> None:
        """Initialise le composant et récupère les références nécessaires."""
        self._transform = self.owner.get_component(TransformComponent)
        self._physics = self.owner.get_component(PhysicsComponent)

        if self._transform is None:
            raise RuntimeError(
                f"StaminaComponent requiert un TransformComponent sur l'entité {self.owner.name}"
            )
        if self._physics is None:
            raise RuntimeError(
                f"StaminaComponent requiert un PhysicsComponent sur l'entité {self.owner.name}"
            )

    def update(self, delta_time: float) -> None:
        """
        Met à jour l'endurance.

        Args:
            delta_time: Temps écoulé depuis la dernière frame (secondes)
        """
        if not self.enabled:
            return

        # Récupération ou drain selon l'état
        if self._is_recovering:
            self._recover(delta_time)
        else:
            self._drain_stamina(delta_time)

        # Mise à jour de la zone de performance
        self._update_performance_zone()

        # Accumulation de la fatigue si on fait un effort
        if not self._is_recovering and self.current_stamina < self.max_stamina:
            self._accumulate_fatigue(delta_time)

    def _drain_stamina(self, delta_time: float) -> None:
        """
        Draine l'endurance en fonction du contexte actuel.

        Formule de drain :
        drain = base_drain * velocity_factor * terrain_multiplier * slope_multiplier * fatigue_factor

        Args:
            delta_time: Temps écoulé (secondes)
        """
        if self._physics is None or self._transform is None:
            return

        # Facteur de vitesse : plus on va vite, plus on consomme
        current_speed = self._physics.get_speed()
        velocity_factor = 1.0 + (current_speed * GameConfig.STAMINA_VELOCITY_MULTIPLIER)

        # Facteur de terrain : récupérer les données du terrain actuel
        terrain_data = self._get_current_terrain_data()
        terrain_multiplier = terrain_data.stamina_drain_multiplier if terrain_data else 1.0

        # Facteur de pente : les montées drainent plus
        # Note: Pour l'instant, on utilise terrain_data.slope
        # Une future amélioration pourrait calculer la pente réelle du terrain
        slope_multiplier = self._calculate_slope_multiplier(terrain_data)

        # Facteur de fatigue : la fatigue réduit l'efficacité
        fatigue_factor = 1.0 + (self.fatigue_level / GameConfig.FATIGUE_MAX) * 0.5

        # Calcul du drain total
        total_drain = (
            self.base_drain_rate
            * velocity_factor
            * terrain_multiplier
            * slope_multiplier
            * fatigue_factor
            * delta_time
        )

        # Application du drain
        self.drain(total_drain)

    def _recover(self, delta_time: float) -> None:
        """
        Récupère de l'endurance (en mode portage ou repos).

        La récupération est réduite par la fatigue cumulative.

        Args:
            delta_time: Temps écoulé (secondes)
        """
        # Facteur de réduction basé sur la fatigue
        fatigue_penalty = 1.0 - (
            self.fatigue_level / GameConfig.FATIGUE_MAX
            * (1.0 - GameConfig.STAMINA_FATIGUE_RECOVERY_PENALTY)
        )

        recovery_amount = self.recovery_rate * fatigue_penalty * delta_time
        self.current_stamina = min(self.max_stamina, self.current_stamina + recovery_amount)

        # Récupération de la fatigue en mode repos
        self.fatigue_level = max(
            0.0, self.fatigue_level - GameConfig.FATIGUE_RECOVERY_IN_CARRYING * delta_time
        )

    def _accumulate_fatigue(self, delta_time: float) -> None:
        """
        Accumule la fatigue durant l'effort.

        Args:
            delta_time: Temps écoulé (secondes)
        """
        fatigue_gain = GameConfig.FATIGUE_ACCUMULATION_RATE * delta_time
        self.fatigue_level = min(GameConfig.FATIGUE_MAX, self.fatigue_level + fatigue_gain)

    def _calculate_slope_multiplier(self, terrain_data: TerrainData | None) -> float:
        """
        Calcule le multiplicateur de drain basé sur la pente.

        Args:
            terrain_data: Données du terrain actuel

        Returns:
            Multiplicateur de drain (1.0 = plat, >1.0 = montée, <1.0 = descente)
        """
        if terrain_data is None or terrain_data.slope == 0.0:
            return 1.0

        # Montée : multiplicateur augmente
        # Descente : multiplicateur diminue (mais reste > 0.5 pour éviter récup gratuite)
        if terrain_data.slope > 0:
            # Montée : 1.0 + (slope / 45°) * SLOPE_MULTIPLIER
            return 1.0 + (abs(terrain_data.slope) / 45.0) * GameConfig.STAMINA_SLOPE_MULTIPLIER
        else:
            # Descente : 0.5 à 1.0 selon la pente
            return max(0.5, 1.0 - (abs(terrain_data.slope) / 45.0) * 0.5)

    def _get_current_terrain_data(self) -> TerrainData | None:
        """
        Récupère les données du terrain à la position actuelle du cycliste.

        Returns:
            TerrainData ou None si pas de terrain
        """
        if self._transform is None:
            return None

        terrain_manager = TerrainManager.get_instance()
        if terrain_manager is None:
            return None

        return terrain_manager.get_terrain_data_at_position(self._transform.position)

    def _update_performance_zone(self) -> None:
        """Met à jour la zone de performance selon le pourcentage d'endurance."""
        percentage = self.get_percentage()

        if percentage >= GameConfig.STAMINA_OPTIMAL_THRESHOLD:
            self._current_zone = PerformanceZone.OPTIMAL
        elif percentage >= GameConfig.STAMINA_MODERATE_THRESHOLD:
            self._current_zone = PerformanceZone.MODERATE
        elif percentage >= GameConfig.STAMINA_CRITICAL_THRESHOLD:
            self._current_zone = PerformanceZone.CRITICAL
        else:
            self._current_zone = PerformanceZone.EXHAUSTED

    def drain(self, amount: float) -> None:
        """
        Consomme de l'endurance.

        Args:
            amount: Quantité d'endurance à consommer
        """
        self.current_stamina = max(0.0, self.current_stamina - amount)

    def set_recovering(self, is_recovering: bool) -> None:
        """
        Active ou désactive le mode récupération.

        Args:
            is_recovering: True pour récupérer, False pour drainer
        """
        self._is_recovering = is_recovering

    def is_empty(self) -> bool:
        """
        Vérifie si l'endurance est épuisée.

        Returns:
            True si l'endurance est à 0
        """
        return self.current_stamina <= 0.0

    def get_percentage(self) -> float:
        """
        Obtient le pourcentage d'endurance restant.

        Returns:
            Pourcentage (0.0 à 100.0)
        """
        return (self.current_stamina / self.max_stamina) * 100.0

    def get_performance_zone(self) -> PerformanceZone:
        """
        Obtient la zone de performance actuelle.

        Returns:
            Zone de performance
        """
        return self._current_zone

    def get_speed_multiplier(self) -> float:
        """
        Obtient le multiplicateur de vitesse selon la zone de performance.

        Returns:
            Multiplicateur de vitesse (0.5 à 1.0)
        """
        zone_to_multiplier = {
            PerformanceZone.OPTIMAL: GameConfig.PERFORMANCE_OPTIMAL_SPEED_MULT,
            PerformanceZone.MODERATE: GameConfig.PERFORMANCE_MODERATE_SPEED_MULT,
            PerformanceZone.CRITICAL: GameConfig.PERFORMANCE_CRITICAL_SPEED_MULT,
            PerformanceZone.EXHAUSTED: GameConfig.PERFORMANCE_EXHAUSTED_SPEED_MULT,
        }
        return zone_to_multiplier.get(self._current_zone, 1.0)

    def apply_fatigue(self, amount: float) -> None:
        """
        Applique directement de la fatigue (pour événements externes).

        Args:
            amount: Quantité de fatigue à ajouter
        """
        self.fatigue_level = min(GameConfig.FATIGUE_MAX, self.fatigue_level + amount)

    def get_fatigue_percentage(self) -> float:
        """
        Obtient le pourcentage de fatigue.

        Returns:
            Pourcentage (0.0 à 100.0)
        """
        return (self.fatigue_level / GameConfig.FATIGUE_MAX) * 100.0

    def destroy(self) -> None:
        """Nettoie les ressources du composant."""
        self._transform = None
        self._physics = None

    def __repr__(self) -> str:
        """Représentation string du composant."""
        return (
            f"StaminaComponent("
            f"stamina={self.current_stamina:.1f}/{self.max_stamina:.1f}, "
            f"fatigue={self.fatigue_level:.1f}, "
            f"zone={self._current_zone.name})"
        )
