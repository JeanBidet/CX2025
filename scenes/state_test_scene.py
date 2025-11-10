"""
Scène de test pour le State Pattern.

Démontre l'utilisation du State Pattern avec le cycliste,
permettant de tester les transitions entre états et les animations.
"""

from typing import Optional
import pygame
from scenes.scene import Scene
from entities.cyclist_with_states import CyclistWithStates
from components.transform_component import TransformComponent
from components.physics_component import PhysicsComponent
from components.command_input_component import CommandInputComponent
from components.state_machine_component import StateMachineComponent
from systems.cyclist_state import StateType
from utils.vector2 import Vector2
from config.game_config import GameConfig
from config.constants import Colors


class StateTestScene(Scene):
    """
    Scène de test pour valider le State Pattern.

    Démontre :
    - Gestion des 4 états (RIDING, CARRYING, REMOUNTING, CRASHED)
    - Transitions d'états
    - Animations associées aux états
    - Changements de comportement physique selon l'état
    """

    def __init__(self) -> None:
        """Initialise la scène de test du State Pattern."""
        super().__init__("StateTestScene")
        self._player: Optional[CyclistWithStates] = None
        self._font: Optional[pygame.font.Font] = None
        self._font_small: Optional[pygame.font.Font] = None

    def enter(self, data: Optional[dict] = None) -> None:
        """
        Initialise la scène lors de son activation.

        Args:
            data: Données optionnelles
        """
        print("[StateTestScene] Entrée dans la scène de test du State Pattern")

        # Initialise les polices
        self._font = pygame.font.Font(None, 48)
        self._font_small = pygame.font.Font(None, 24)

        # Crée le cycliste avec states au centre
        center_pos = Vector2(
            GameConfig.WINDOW_WIDTH / 2,
            GameConfig.WINDOW_HEIGHT / 2
        )

        self._player = CyclistWithStates(
            name="StatePlayer",
            position=center_pos,
            is_player=True
        )
        self._player.add_tag("player")

        # Ajoute le joueur à l'Entity Manager
        self._entity_manager.add_entity(self._player)

        print(f"[StateTestScene] Joueur créé: {self._player}")

    def exit(self) -> None:
        """Nettoie la scène lors de sa désactivation."""
        print("[StateTestScene] Sortie de la scène")
        self._entity_manager.clear()
        self._player = None

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Gère les événements de la scène.

        Args:
            events: Liste des événements Pygame
        """
        if not self._player:
            return

        # Transmet les événements au CommandInputComponent
        input_comp = self._player.get_component(CommandInputComponent)
        if input_comp:
            input_comp.set_events(events)

        # Transmet aussi à la State Machine pour gestion dans les états
        state_machine = self._player.get_component(StateMachineComponent)
        if state_machine:
            state_machine.handle_events(events)

        # Gère les événements de test de la scène
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._reset_player()
                elif event.key == pygame.K_x:
                    # Force un crash pour tester
                    self._player.trigger_crash()
                elif event.key == pygame.K_1:
                    # Force état RIDING
                    state_machine.change_state(StateType.RIDING, force=True)
                elif event.key == pygame.K_2:
                    # Force état CARRYING
                    state_machine.change_state(StateType.CARRYING, force=True)
                elif event.key == pygame.K_3:
                    # Force état REMOUNTING
                    state_machine.change_state(StateType.REMOUNTING, force=True)
                elif event.key == pygame.K_4:
                    # Force état CRASHED
                    state_machine.change_state(StateType.CRASHED, force=True)

    def _reset_player(self) -> None:
        """Réinitialise la position et l'état du joueur."""
        if not self._player:
            return

        transform = self._player.get_component(TransformComponent)
        physics = self._player.get_component(PhysicsComponent)
        state_machine = self._player.get_component(StateMachineComponent)

        if transform and physics:
            transform.position = Vector2(
                GameConfig.WINDOW_WIDTH / 2,
                GameConfig.WINDOW_HEIGHT / 2
            )
            transform.rotation = 0
            physics.stop()

        if state_machine:
            state_machine.change_state(StateType.RIDING, force=True)

        print("[StateTestScene] Joueur réinitialisé")

    def update(self, delta_time: float) -> None:
        """
        Met à jour la logique de la scène.

        Args:
            delta_time: Temps écoulé depuis la dernière frame
        """
        # Met à jour toutes les entités
        self._entity_manager.update(delta_time)

        # Garde le joueur dans les limites
        if self._player:
            self._clamp_player_to_bounds()

    def _clamp_player_to_bounds(self) -> None:
        """Garde le joueur dans les limites de l'écran."""
        if not self._player:
            return

        transform = self._player.get_component(TransformComponent)
        physics = self._player.get_component(PhysicsComponent)

        if not transform or not physics:
            return

        pos = transform.position
        margin = 50
        clamped = False

        if pos.x < margin:
            pos.x = margin
            clamped = True
        elif pos.x > GameConfig.WINDOW_WIDTH - margin:
            pos.x = GameConfig.WINDOW_WIDTH - margin
            clamped = True

        if pos.y < margin:
            pos.y = margin
            clamped = True
        elif pos.y > GameConfig.WINDOW_HEIGHT - margin:
            pos.y = GameConfig.WINDOW_HEIGHT - margin
            clamped = True

        if clamped:
            transform.position = pos
            physics.velocity = physics.velocity * 0.5

    def render(self, screen: pygame.Surface) -> None:
        """
        Effectue le rendu de la scène.

        Args:
            screen: Surface Pygame sur laquelle dessiner
        """
        # Fond
        screen.fill(GameConfig.BACKGROUND_COLOR)

        # Rend le joueur avec son animation
        if self._player and self._player.active:
            self._render_player(screen)

        # Affiche le HUD
        self._render_hud(screen)
        self._render_instructions(screen)

    def _render_player(self, screen: pygame.Surface) -> None:
        """
        Rend le joueur avec son animation actuelle.

        Args:
            screen: Surface de rendu
        """
        if not self._player:
            return

        transform = self._player.get_component(TransformComponent)
        if not transform:
            return

        # Récupère la frame actuelle de l'animation
        frame = self._player.get_current_animation_frame()
        if not frame:
            return

        # Position de rendu
        pos = transform.position

        # Applique la rotation si nécessaire
        rotated_frame = pygame.transform.rotate(frame, -transform.rotation_degrees)

        # Centre le sprite
        frame_rect = rotated_frame.get_rect(center=(int(pos.x), int(pos.y)))

        # Applique l'effet de crash si actif
        if self._player.is_crashed():
            # Teinte rouge
            red_overlay = pygame.Surface(rotated_frame.get_size(), pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 80))
            rotated_frame.blit(red_overlay, (0, 0))

        # Dessine le sprite
        screen.blit(rotated_frame, frame_rect.topleft)

    def _render_hud(self, screen: pygame.Surface) -> None:
        """Affiche le HUD avec les stats du joueur."""
        if not self._player or not self._font_small:
            return

        transform = self._player.get_component(TransformComponent)
        physics = self._player.get_component(PhysicsComponent)
        state_machine = self._player.get_component(StateMachineComponent)

        if not transform or not physics or not state_machine:
            return

        # Informations d'état
        current_state = state_machine.get_current_state_name()
        time_in_state = state_machine.get_time_in_current_state()

        hud_texts = [
            f"État: {current_state}",
            f"Temps dans état: {time_in_state:.1f}s",
            f"Position: ({transform.position.x:.0f}, {transform.position.y:.0f})",
            f"Vitesse: {physics.get_speed():.1f} / {physics.max_speed:.1f} px/s",
            f"Rotation: {transform.rotation_degrees:.1f}°",
            f"Animation: {self._player.animation_controller.get_current_animation_name()}",
        ]

        y_offset = 10
        for text in hud_texts:
            self._render_text_with_bg(screen, text, 10, y_offset)
            y_offset += 30

    def _render_instructions(self, screen: pygame.Surface) -> None:
        """Affiche les instructions."""
        if not self._font_small:
            return

        instructions = [
            "Fleches/WASD : Deplacer",
            "ESPACE : Sprint",
            "C : Porter/Remonter",
            "X : Force Crash (test)",
            "",
            "1 : Force RIDING",
            "2 : Force CARRYING",
            "3 : Force REMOUNTING",
            "4 : Force CRASHED",
            "",
            "R : Reset",
            "ESC : Quitter",
        ]

        y_offset = GameConfig.WINDOW_HEIGHT - (len(instructions) * 25) - 10
        for instruction in instructions:
            if instruction:  # Ignore empty lines for spacing
                self._render_text_with_bg(
                    screen,
                    instruction,
                    GameConfig.WINDOW_WIDTH - 320,
                    y_offset,
                    align_right=True
                )
            y_offset += 25

    def _render_text_with_bg(
        self,
        screen: pygame.Surface,
        text: str,
        x: int,
        y: int,
        align_right: bool = False
    ) -> None:
        """
        Rend du texte avec fond semi-transparent.

        Args:
            screen: Surface de rendu
            text: Texte à afficher
            x: Position x
            y: Position y
            align_right: Si vrai, aligne à droite
        """
        if not self._font_small:
            return

        text_surface = self._font_small.render(text, True, Colors.WHITE)
        text_rect = text_surface.get_rect()

        if align_right:
            text_rect.topright = (x, y)
        else:
            text_rect.topleft = (x, y)

        # Fond semi-transparent
        bg_rect = text_rect.inflate(10, 4)
        bg_surface = pygame.Surface(bg_rect.size)
        bg_surface.set_alpha(128)
        bg_surface.fill(Colors.BLACK)
        screen.blit(bg_surface, bg_rect.topleft)

        # Texte
        screen.blit(text_surface, text_rect.topleft)
