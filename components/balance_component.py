"""
Balance Component - Gestion de l'équilibre du cycliste.

Ce composant gère l'équilibre (balance) du cycliste avec un système d'instabilité
basé sur le contexte (terrain, vitesse, camber, endurance). Un équilibre trop faible
déclenche une chute.
"""

from components.icomponent import IComponent
from components.transform_component import TransformComponent
from components.physics_component import PhysicsComponent
from config.game_config import GameConfig
from systems.terrain_manager import TerrainManager
from systems.terrain_data import TerrainData
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from entities.entity import Entity
    from components.stamina_component import StaminaComponent


class BalanceComponent(IComponent):
    """
    Composant gérant l'équilibre du cycliste.

    L'équilibre est affecté par :
    - L'angle de camber du terrain (inclinaison latérale)
    - La vitesse dans les virages (force centrifuge)
    - Le type de terrain (grip réduit = plus d'instabilité)
    - L'épuisement (endurance basse = moins de contrôle)

    L'équilibre se régénère automatiquement en ligne droite sur bon terrain.
    Si l'équilibre tombe en dessous du seuil critique, le cycliste risque de chuter.
    """

    def __init__(self, owner: "Entity") -> None:
        """
        Initialise le composant d'équilibre.

        Args:
            owner: L'entité propriétaire (le cycliste)
        """
        super().__init__(owner)

        # Valeurs actuelles
        self.current_balance: float = GameConfig.BALANCE_MAX
        self.max_balance: float = GameConfig.BALANCE_MAX
        self.instability: float = 0.0  # Facteur temporaire d'instabilité

        # Taux de récupération
        self.recovery_rate: float = GameConfig.BALANCE_RECOVERY_RATE

        # Seuils
        self.critical_threshold: float = GameConfig.BALANCE_CRITICAL_THRESHOLD
        self.crash_threshold: float = GameConfig.BALANCE_CRASH_THRESHOLD

        # Références aux composants requis
        self._transform: TransformComponent | None = None
        self._physics: PhysicsComponent | None = None
        self._stamina: "StaminaComponent | None" = None

        # Historique pour détection de changement de direction
        self._previous_rotation: float = 0.0

        # Source du dernier déséquilibre (pour debug)
        self._last_imbalance_source: str = ""

    def init(self) -> None:
        """Initialise le composant et récupère les références nécessaires."""
        from components.stamina_component import StaminaComponent

        self._transform = self.owner.get_component(TransformComponent)
        self._physics = self.owner.get_component(PhysicsComponent)
        self._stamina = self.owner.get_component(StaminaComponent)

        if self._transform is None:
            raise RuntimeError(
                f"BalanceComponent requiert un TransformComponent sur l'entité {self.owner.name}"
            )
        if self._physics is None:
            raise RuntimeError(
                f"BalanceComponent requiert un PhysicsComponent sur l'entité {self.owner.name}"
            )

        # StaminaComponent est optionnel mais recommandé
        if self._stamina is None:
            print(
                f"[WARNING] BalanceComponent sur {self.owner.name} fonctionne mieux avec StaminaComponent"
            )

        # Initialiser l'historique
        if self._transform is not None:
            self._previous_rotation = self._transform.rotation

    def update(self, delta_time: float) -> None:
        """
        Met à jour l'équilibre.

        Args:
            delta_time: Temps écoulé depuis la dernière frame (secondes)
        """
        if not self.enabled:
            return

        # Calculer les facteurs d'instabilité
        self._calculate_instability(delta_time)

        # Appliquer l'instabilité
        if self.instability > 0:
            self.current_balance = max(0.0, self.current_balance - self.instability * delta_time)

        # Récupération naturelle
        self._recover_balance(delta_time)

        # Décroissance de l'instabilité temporaire
        self.instability = max(0.0, self.instability - 10.0 * delta_time)

    def _calculate_instability(self, delta_time: float) -> None:
        """
        Calcule l'instabilité basée sur le contexte actuel.

        Args:
            delta_time: Temps écoulé (secondes)
        """
        if self._physics is None or self._transform is None:
            return

        total_instability = 0.0

        # 1. Facteur de camber (inclinaison latérale du terrain)
        terrain_data = self._get_current_terrain_data()
        if terrain_data and terrain_data.camber != 0.0:
            camber_instability = (
                abs(terrain_data.camber) * GameConfig.BALANCE_CAMBER_MULTIPLIER
            )
            total_instability += camber_instability
            self._last_imbalance_source = "camber"

        # 2. Facteur de vitesse dans les virages (changement de rotation)
        rotation_change = abs(self._transform.rotation - self._previous_rotation)
        if rotation_change > 0.01:  # Seuil minimal pour éviter le bruit
            current_speed = self._physics.get_speed()
            speed_factor = current_speed / GameConfig.CYCLIST_MAX_SPEED
            turn_instability = rotation_change * speed_factor * GameConfig.BALANCE_SPEED_MULTIPLIER * 100.0
            total_instability += turn_instability
            self._last_imbalance_source = "turning"

        # 3. Facteur de grip du terrain
        if terrain_data:
            # Moins de grip = plus d'instabilité
            grip_instability = (1.0 - terrain_data.grip_level) * GameConfig.BALANCE_TERRAIN_GRIP_FACTOR
            total_instability += grip_instability
            if grip_instability > 0.5:
                self._last_imbalance_source = "low_grip"

        # 4. Facteur d'épuisement (si StaminaComponent disponible)
        if self._stamina is not None:
            stamina_percentage = self._stamina.get_percentage()
            if stamina_percentage < 30.0:  # En dessous de 30% d'endurance
                exhaustion_factor = (30.0 - stamina_percentage) / 30.0
                exhaustion_instability = exhaustion_factor * GameConfig.BALANCE_LOW_STAMINA_MULTIPLIER
                total_instability += exhaustion_instability
                if exhaustion_instability > 1.0:
                    self._last_imbalance_source = "exhaustion"

        # Mettre à jour l'instabilité
        self.instability = total_instability

        # Sauvegarder pour la prochaine frame
        self._previous_rotation = self._transform.rotation

    def _recover_balance(self, delta_time: float) -> None:
        """
        Récupère l'équilibre naturellement.

        La récupération est plus rapide sur bon terrain et en ligne droite.

        Args:
            delta_time: Temps écoulé (secondes)
        """
        # Conditions optimales de récupération : ligne droite + bon grip
        terrain_data = self._get_current_terrain_data()
        recovery_multiplier = 1.0

        if terrain_data:
            # Bon grip facilite la récupération
            recovery_multiplier *= terrain_data.grip_level

            # Terrain plat (camber faible) facilite la récupération
            if abs(terrain_data.camber) < 2.0:
                recovery_multiplier *= 1.5

        # Récupération
        recovery_amount = self.recovery_rate * recovery_multiplier * delta_time
        self.current_balance = min(self.max_balance, self.current_balance + recovery_amount)

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

    def apply_imbalance(self, amount: float, source: str = "unknown") -> None:
        """
        Applique un déséquilibre externe (collision, obstacle, etc.).

        Args:
            amount: Quantité de déséquilibre à appliquer
            source: Source du déséquilibre (pour debug/log)
        """
        self.current_balance = max(0.0, self.current_balance - amount)
        self.instability += amount * 0.5  # Ajoute aussi de l'instabilité temporaire
        self._last_imbalance_source = source

    def is_critical(self) -> bool:
        """
        Vérifie si l'équilibre est dans une zone critique.

        Returns:
            True si proche de la chute
        """
        return self.current_balance <= self.critical_threshold

    def should_crash(self) -> bool:
        """
        Détermine si une chute doit se produire.

        Returns:
            True si le cycliste doit chuter
        """
        if self.current_balance <= self.crash_threshold:
            # Chute garantie sous le seuil
            return True

        if self.is_critical():
            # Entre crash_threshold et critical_threshold : probabilité de chute
            # Plus on est bas, plus la probabilité est haute
            crash_probability = (
                (self.critical_threshold - self.current_balance) /
                (self.critical_threshold - self.crash_threshold)
            ) * 0.3  # Max 30% de chance par frame en zone critique

            return random.random() < crash_probability

        return False

    def get_percentage(self) -> float:
        """
        Obtient le pourcentage d'équilibre restant.

        Returns:
            Pourcentage (0.0 à 100.0)
        """
        return (self.current_balance / self.max_balance) * 100.0

    def get_stability_level(self) -> str:
        """
        Obtient un indicateur textuel du niveau de stabilité.

        Returns:
            "STABLE", "UNSTABLE" ou "CRITICAL"
        """
        if self.current_balance > 60.0:
            return "STABLE"
        elif self.current_balance > self.critical_threshold:
            return "UNSTABLE"
        else:
            return "CRITICAL"

    def get_last_imbalance_source(self) -> str:
        """
        Obtient la dernière source de déséquilibre.

        Returns:
            Nom de la source
        """
        return self._last_imbalance_source

    def reset_balance(self) -> None:
        """Réinitialise l'équilibre au maximum (après remontée en selle)."""
        self.current_balance = self.max_balance
        self.instability = 0.0
        self._last_imbalance_source = ""

    def destroy(self) -> None:
        """Nettoie les ressources du composant."""
        self._transform = None
        self._physics = None
        self._stamina = None

    def __repr__(self) -> str:
        """Représentation string du composant."""
        return (
            f"BalanceComponent("
            f"balance={self.current_balance:.1f}/{self.max_balance:.1f}, "
            f"instability={self.instability:.1f}, "
            f"level={self.get_stability_level()})"
        )
