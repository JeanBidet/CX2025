"""
Scène de test pour le Command Pattern.

Cette scène démontre l'utilisation du Command Pattern pour gérer les inputs,
permettant un remapping facile et une meilleure testabilité.
"""

from typing import Optional
import pygame
from scenes.scene import Scene
from entities.entity import Entity
from components.transform_component import TransformComponent
from components.physics_component import PhysicsComponent
from components.command_input_component import CommandInputComponent
from components.sprite_renderer_component import SpriteRendererComponent
from config.game_config import GameConfig
from config.constants import Colors
from config.input_config import list_available_profiles
from utils.vector2 import Vector2


class CommandTestScene(Scene):
    """
    Scène de test pour valider le Command Pattern.

    Démontre :
    - Utilisation de CommandInputComponent
    - Changement de profil à chaud
    - Exécution des différentes commandes
    - Affichage des touches liées
    """

    def __init__(self) -> None:
        """Initialise la scène de test du Command Pattern."""
        super().__init__("CommandTestScene")
        self._player: Optional[Entity] = None
        self._font: Optional[pygame.font.Font] = None
        self._font_small: Optional[pygame.font.Font] = None
        self._current_profile_index: int = 0
        self._available_profiles: list[str] = []

    def enter(self, data: Optional[dict] = None) -> None:
        """
        Initialise la scène lors de son activation.

        Args:
            data: Données optionnelles de la scène précédente
        """
        print("[CommandTestScene] Entrée dans la scène de test Command Pattern")

        # Initialise les polices
        self._font = pygame.font.Font(None, 36)
        self._font_small = pygame.font.Font(None, 24)

        # Récupère la liste des profils disponibles
        self._available_profiles = list_available_profiles()

        # Crée le joueur au centre
        center_pos = Vector2(
            GameConfig.WINDOW_WIDTH / 2,
            GameConfig.WINDOW_HEIGHT / 2
        )
        self._player = Entity("CommandPlayer")
        self._player.add_tag("player")

        # Ajoute les composants
        self._player.add_component(TransformComponent, center_pos)
        self._player.add_component(
            PhysicsComponent,
            mass=GameConfig.CYCLIST_MASS,
            drag=GameConfig.CYCLIST_DRAG,
            max_speed=GameConfig.CYCLIST_MAX_SPEED
        )

        # Ajoute le CommandInputComponent avec le profil par défaut
        self._player.add_component(
            CommandInputComponent,
            profile_name="hybrid"
        )

        # Ajoute le renderer
        self._player.add_component(
            SpriteRendererComponent,
            width=40,
            height=60,
            color=Colors.CYAN,
            use_rotation=True
        )

        # Ajoute le joueur à l'Entity Manager
        self._entity_manager.add_entity(self._player)

        print(f"[CommandTestScene] Profils disponibles: {self._available_profiles}")

    def exit(self) -> None:
        """Nettoie la scène lors de sa désactivation."""
        print("[CommandTestScene] Sortie de la scène")
        self._entity_manager.clear()
        self._player = None

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """
        Gère les événements de la scène.

        Args:
            events: Liste des événements Pygame
        """
        # Transmet les événements au CommandInputComponent du joueur
        if self._player:
            input_comp = self._player.get_component(CommandInputComponent)
            if input_comp:
                input_comp.set_events(events)

        # Gère les événements de la scène
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._reset_player()
                elif event.key == pygame.K_TAB:
                    self._cycle_profile()
                elif event.key == pygame.K_t:
                    self._toggle_input()

    def _reset_player(self) -> None:
        """Réinitialise la position et la vélocité du joueur."""
        if not self._player:
            return

        transform = self._player.get_component(TransformComponent)
        physics = self._player.get_component(PhysicsComponent)

        if transform and physics:
            transform.position = Vector2(
                GameConfig.WINDOW_WIDTH / 2,
                GameConfig.WINDOW_HEIGHT / 2
            )
            transform.rotation = 0
            physics.stop()
            print("[CommandTestScene] Joueur réinitialisé")

    def _cycle_profile(self) -> None:
        """Change le profil de contrôle au suivant dans la liste."""
        if not self._player or not self._available_profiles:
            return

        input_comp = self._player.get_component(CommandInputComponent)
        if input_comp:
            # Passe au profil suivant
            self._current_profile_index = (
                self._current_profile_index + 1
            ) % len(self._available_profiles)

            new_profile = self._available_profiles[self._current_profile_index]
            input_comp.load_profile(new_profile)

            print(f"[CommandTestScene] Profil changé: {new_profile}")

    def _toggle_input(self) -> None:
        """Active/désactive les contrôles."""
        if not self._player:
            return

        input_comp = self._player.get_component(CommandInputComponent)
        if input_comp:
            if input_comp.is_enabled():
                input_comp.disable()
                print("[CommandTestScene] Contrôles désactivés")
            else:
                input_comp.enable()
                print("[CommandTestScene] Contrôles activés")

    def update(self, delta_time: float) -> None:
        """
        Met à jour la logique de la scène.

        Args:
            delta_time: Temps écoulé depuis la dernière frame
        """
        # Met à jour toutes les entités (incluant CommandInputComponent)
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

        # Rend les entités
        for entity in self._entity_manager.get_all_entities():
            renderer = entity.get_component(SpriteRendererComponent)
            if renderer and entity.active:
                renderer.render(screen)

        # Affiche le HUD
        self._render_hud(screen)
        self._render_instructions(screen)
        self._render_key_bindings(screen)

    def _render_hud(self, screen: pygame.Surface) -> None:
        """Affiche le HUD avec les stats du joueur."""
        if not self._player or not self._font_small:
            return

        transform = self._player.get_component(TransformComponent)
        physics = self._player.get_component(PhysicsComponent)
        input_comp = self._player.get_component(CommandInputComponent)

        if not transform or not physics or not input_comp:
            return

        hud_texts = [
            f"Profil: {input_comp.get_profile_name()}",
            f"Position: ({transform.position.x:.0f}, {transform.position.y:.0f})",
            f"Vitesse: {physics.get_speed():.1f} px/s",
            f"Rotation: {transform.rotation_degrees:.1f}°",
            f"Controles: {'ON' if input_comp.is_enabled() else 'OFF'}",
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
            "TAB : Changer profil de controle",
            "T : Toggle controles ON/OFF",
            "R : Reset position",
            "ESC : Quitter",
        ]

        y_offset = GameConfig.WINDOW_HEIGHT - 140
        for instruction in instructions:
            self._render_text_with_bg(
                screen,
                instruction,
                GameConfig.WINDOW_WIDTH - 350,
                y_offset,
                align_right=True
            )
            y_offset += 30

    def _render_key_bindings(self, screen: pygame.Surface) -> None:
        """Affiche les touches liées."""
        if not self._player or not self._font_small:
            return

        input_comp = self._player.get_component(CommandInputComponent)
        if not input_comp:
            return

        # Titre
        title_y = 200
        self._render_text_with_bg(
            screen,
            "Touches liees:",
            GameConfig.WINDOW_WIDTH - 300,
            title_y,
            align_right=True
        )

        # Affiche quelques bindings clés
        key_names = {
            pygame.K_UP: "UP",
            pygame.K_DOWN: "DOWN",
            pygame.K_LEFT: "LEFT",
            pygame.K_RIGHT: "RIGHT",
            pygame.K_w: "W",
            pygame.K_s: "S",
            pygame.K_a: "A",
            pygame.K_d: "D",
            pygame.K_SPACE: "SPACE",
        }

        bound_keys = input_comp.get_bound_keys()
        y_offset = title_y + 30

        for key, key_name in key_names.items():
            if key in bound_keys:
                command_name = bound_keys[key]
                text = f"{key_name}: {command_name}"
                self._render_text_with_bg(
                    screen,
                    text,
                    GameConfig.WINDOW_WIDTH - 300,
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
