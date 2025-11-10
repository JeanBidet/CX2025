"""
Cyclist With States - Cycliste avec State Machine et animations.

Version améliorée du Cyclist intégrant le State Pattern pour gérer
les différents états (RIDING, CARRYING, REMOUNTING, CRASHED).
"""

from entities.entity import Entity
from components.transform_component import TransformComponent
from components.physics_component import PhysicsComponent
from components.command_input_component import CommandInputComponent
from components.state_machine_component import StateMachineComponent
from systems.cyclist_state import StateType
from systems.cyclist_states import RidingState, CarryingState, RemountingState, CrashedState
from systems.animation_system import Animation, AnimationController
from utils.sprite_generator import SpriteGenerator
from utils.vector2 import Vector2
from config.game_config import GameConfig


class CyclistWithStates(Entity):
    """
    Cycliste avec gestion des états via State Machine.

    Combine :
    - TransformComponent pour position et rotation
    - PhysicsComponent pour mouvement
    - CommandInputComponent pour contrôles
    - StateMachineComponent pour états
    - AnimationController pour animations
    """

    def __init__(
        self,
        name: str = "StateCyclist",
        position: Vector2 | None = None,
        is_player: bool = True,
        profile_name: str = "hybrid"
    ) -> None:
        """
        Initialise un cycliste avec State Machine.

        Args:
            name: Nom du cycliste
            position: Position initiale
            is_player: Si vrai, ajoute les contrôles
            profile_name: Profil de contrôle à utiliser
        """
        super().__init__(name)

        self.is_player = is_player
        self.position = position or Vector2(100, 100)

        # Stocke les paramètres physiques de base
        self._base_max_speed = GameConfig.CYCLIST_MAX_SPEED
        self._base_drag = GameConfig.CYCLIST_DRAG

        # Flag pour effet visuel de crash
        self._crashed_effect_active = False

        # Setup des composants et animations
        self._setup_components()
        self._setup_animations()
        self._setup_state_machine()

    def _setup_components(self) -> None:
        """Configure les composants de base."""
        # Transform
        self.add_component(TransformComponent, self.position.copy())

        # Physics
        self.add_component(
            PhysicsComponent,
            mass=GameConfig.CYCLIST_MASS,
            drag=self._base_drag,
            max_speed=self._base_max_speed,
            use_gravity=False
        )

        # Command Input (pour le joueur)
        if self.is_player:
            self.add_component(
                CommandInputComponent,
                profile_name="hybrid"
            )

    def _setup_animations(self) -> None:
        """Configure le système d'animation."""
        # Crée l'animation controller
        self.animation_controller = AnimationController()

        # Génère les sprites pour chaque animation
        # Animation RIDING (pédalage)
        riding_frames = SpriteGenerator.generate_riding_frames(
            width=40,
            height=60,
            frame_count=4
        )
        riding_anim = Animation(riding_frames, frame_duration=0.15, loop=True)
        self.animation_controller.add_animation('pedal', riding_anim)

        # Animation CARRYING (marche avec vélo)
        carrying_frames = SpriteGenerator.generate_carrying_frames(
            width=40,
            height=60,
            frame_count=4
        )
        carrying_anim = Animation(carrying_frames, frame_duration=0.2, loop=True)
        self.animation_controller.add_animation('walk', carrying_anim)

        # Animation REMOUNTING (remontée)
        remounting_frames = SpriteGenerator.generate_remounting_frames(
            width=40,
            height=60,
            frame_count=3
        )
        remounting_anim = Animation(remounting_frames, frame_duration=0.3, loop=False)
        self.animation_controller.add_animation('mount', remounting_anim)

        # Animation CRASHED (chute)
        crashed_frames = SpriteGenerator.generate_crashed_frames(
            width=40,
            height=60,
            frame_count=4
        )
        crashed_anim = Animation(crashed_frames, frame_duration=0.15, loop=False)
        self.animation_controller.add_animation('fall', crashed_anim)

        # Démarre avec l'animation de pédalage
        self.animation_controller.play('pedal')

    def _setup_state_machine(self) -> None:
        """Configure la State Machine."""
        # Ajoute le StateMachineComponent
        self.state_machine = self.add_component(
            StateMachineComponent,
            initial_state=StateType.RIDING,
            keep_history=True
        )

        # Crée et ajoute les 4 états
        self.state_machine.add_state(StateType.RIDING, RidingState())
        self.state_machine.add_state(StateType.CARRYING, CarryingState())
        self.state_machine.add_state(StateType.REMOUNTING, RemountingState(duration=1.0))
        self.state_machine.add_state(StateType.CRASHED, CrashedState(recovery_duration=2.0))

        # Change vers l'état initial (trigger enter())
        self.state_machine.change_state(StateType.RIDING, force=True)

    def update(self, delta_time: float) -> None:
        """
        Met à jour le cycliste.

        Args:
            delta_time: Temps écoulé
        """
        # Update la state machine (qui update l'état actuel)
        # Les composants sont updatés automatiquement par l'Entity Manager

        # Update l'animation
        self.animation_controller.update(delta_time)

        # Call parent update
        super().update(delta_time)

    def get_current_animation_frame(self):
        """
        Retourne la frame actuelle de l'animation.

        Returns:
            Surface Pygame ou None
        """
        return self.animation_controller.get_current_frame()

    def get_current_state(self) -> StateType:
        """
        Retourne l'état actuel.

        Returns:
            StateType actuel
        """
        return self.state_machine.get_current_state_type()

    def get_current_state_name(self) -> str:
        """
        Retourne le nom de l'état actuel.

        Returns:
            Nom de l'état
        """
        return self.state_machine.get_current_state_name()

    def trigger_crash(self) -> None:
        """Force une transition vers l'état CRASHED."""
        if self.state_machine:
            self.state_machine.change_state(StateType.CRASHED)

    def is_crashed(self) -> bool:
        """Vérifie si le cycliste est en état CRASHED."""
        return self._crashed_effect_active

    def __repr__(self) -> str:
        """Représentation string du cycliste."""
        physics = self.get_component(PhysicsComponent)
        speed = physics.get_speed() if physics else 0.0
        state = self.get_current_state_name()
        return (
            f"CyclistWithStates(name={self.name}, "
            f"state={state}, "
            f"speed={speed:.1f}px/s)"
        )
