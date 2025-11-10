"""
Point d'entrée principal du jeu de cyclo-cross.

Ce fichier contient le Game Loop principal et initialise tous les systèmes
du jeu.
"""

import sys
import pygame
from config.game_config import GameConfig
from config.constants import GameState, Colors
from systems.scene_manager import SceneManager
from scenes.test_scene import TestScene
from scenes.physics_test_scene import PhysicsTestScene
from scenes.command_test_scene import CommandTestScene
from scenes.terrain_test_scene import TerrainTestScene
from scenes.state_test_scene import StateTestScene
from scenes.stamina_balance_test_scene import StaminaBalanceTestScene


class Game:
    """
    Classe principale du jeu gérant le Game Loop et l'initialisation.

    Cette classe orchestre tous les systèmes du jeu et gère le cycle
    de vie de l'application.
    """

    def __init__(self) -> None:
        """Initialise le jeu et tous ses systèmes."""
        print("[Game] Initialisation du jeu...")

        # Initialisation de Pygame
        pygame.init()
        pygame.font.init()

        # Création de la fenêtre
        flags = pygame.FULLSCREEN if GameConfig.FULLSCREEN else 0
        self._screen: pygame.Surface = pygame.display.set_mode(
            GameConfig.get_window_size(),
            flags
        )
        pygame.display.set_caption(GameConfig.WINDOW_TITLE)

        # Horloge pour gérer les FPS
        self._clock: pygame.time.Clock = pygame.time.Clock()

        # État du jeu
        self._running: bool = True
        self._state: GameState = GameState.PLAYING

        # Scene Manager
        self._scene_manager: SceneManager = SceneManager()

        # Police pour afficher les FPS
        self._debug_font: pygame.font.Font = pygame.font.Font(None, 24)

        # Statistiques
        self._fps: float = 0.0

        print("[Game] Initialisation terminée")

    def _setup_scenes(self) -> None:
        """Configure et enregistre toutes les scènes du jeu."""
        print("[Game] Configuration des scènes...")

        # Crée et enregistre la scène de test originale
        test_scene = TestScene()
        self._scene_manager.register_scene("test", test_scene)

        # Crée et enregistre la scène de test physique (Prompt 2)
        physics_scene = PhysicsTestScene()
        self._scene_manager.register_scene("physics", physics_scene)

        # Crée et enregistre la scène de test Command Pattern (Prompt 3)
        command_scene = CommandTestScene()
        self._scene_manager.register_scene("command", command_scene)

        # Crée et enregistre la scène de test Terrain System (Prompt 4)
        terrain_scene = TerrainTestScene()
        self._scene_manager.register_scene("terrain", terrain_scene)

        # Crée et enregistre la scène de test State Pattern (Prompt 5)
        state_scene = StateTestScene()
        self._scene_manager.register_scene("state", state_scene)

        # Crée et enregistre la scène de test Stamina/Balance (Prompt 6)
        stamina_balance_scene = StaminaBalanceTestScene()
        self._scene_manager.register_scene("stamina_balance", stamina_balance_scene)

        # TODO: Ajouter d'autres scènes (Menu, Race, Results) dans les futurs prompts

        # Active la scène de test Stamina/Balance par défaut
        self._scene_manager.change_scene("stamina_balance")

        print("[Game] Scènes configurées")

    def run(self) -> None:
        """
        Lance le Game Loop principal.

        Cette méthode contient la boucle principale du jeu qui tourne
        jusqu'à ce que le jeu soit fermé.
        """
        print("[Game] Démarrage du Game Loop...")

        # Configure les scènes
        self._setup_scenes()

        # Game Loop principal
        while self._running:
            # Calcule le delta time (en secondes)
            delta_time = self._clock.tick(GameConfig.TARGET_FPS) / 1000.0

            # Limite le delta time pour éviter les gros sauts
            delta_time = min(delta_time, GameConfig.DELTA_TIME_MAX)

            # Calcule les FPS
            self._fps = self._clock.get_fps()

            # Gestion des événements
            self._handle_events()

            # Mise à jour
            if self._state != GameState.PAUSED:
                self._update(delta_time)

            # Rendu
            self._render()

        # Nettoyage
        self._cleanup()

    def _handle_events(self) -> None:
        """Gère tous les événements Pygame."""
        events = pygame.event.get()

        for event in events:
            # Fermeture de la fenêtre
            if event.type == pygame.QUIT:
                self._running = False

            # Gestion des touches globales
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                elif event.key == pygame.K_F11:
                    self._toggle_fullscreen()
                elif event.key == pygame.K_p:
                    self._toggle_pause()
                elif event.key == pygame.K_F3:
                    GameConfig.SHOW_DEBUG_INFO = not GameConfig.SHOW_DEBUG_INFO
                elif event.key == pygame.K_F1:
                    self._scene_manager.change_scene("terrain")
                elif event.key == pygame.K_F2:
                    self._scene_manager.change_scene("state")
                elif event.key == pygame.K_F4:
                    self._scene_manager.change_scene("stamina_balance")

        # Transmet les événements au Scene Manager
        self._scene_manager.handle_events(events)

    def _update(self, delta_time: float) -> None:
        """
        Met à jour la logique du jeu.

        Args:
            delta_time: Temps écoulé depuis la dernière frame en secondes
        """
        self._scene_manager.update(delta_time)

    def _render(self) -> None:
        """Effectue le rendu du jeu à l'écran."""
        # Efface l'écran
        self._screen.fill(Colors.BLACK)

        # Rend la scène active
        self._scene_manager.render(self._screen)

        # Affiche les informations de débogage
        if GameConfig.SHOW_DEBUG_INFO:
            self._render_debug_info()

        # Affiche le message de pause
        if self._state == GameState.PAUSED:
            self._render_pause_overlay()

        # Met à jour l'affichage (double buffering)
        pygame.display.flip()

    def _render_debug_info(self) -> None:
        """Affiche les informations de débogage à l'écran."""
        debug_texts = [
            f"FPS: {self._fps:.1f}",
            f"Scene: {self._scene_manager.current_scene_name}",
        ]

        # Ajoute le nombre d'entités si une scène est active
        if self._scene_manager.current_scene:
            entity_count = self._scene_manager.current_scene.entity_manager.entity_count()
            debug_texts.append(f"Entities: {entity_count}")

        y_offset = 10
        for text in debug_texts:
            surface = self._debug_font.render(text, True, Colors.YELLOW)
            self._screen.blit(surface, (10, y_offset))
            y_offset += 25

    def _render_pause_overlay(self) -> None:
        """Affiche un overlay de pause."""
        # Semi-transparent overlay
        overlay = pygame.Surface(GameConfig.get_window_size())
        overlay.set_alpha(128)
        overlay.fill(Colors.BLACK)
        self._screen.blit(overlay, (0, 0))

        # Texte "PAUSE"
        font = pygame.font.Font(None, 72)
        text = font.render("PAUSE", True, Colors.WHITE)
        text_rect = text.get_rect(center=GameConfig.get_window_center())
        self._screen.blit(text, text_rect)

    def _toggle_fullscreen(self) -> None:
        """Bascule entre mode plein écran et mode fenêtré."""
        GameConfig.FULLSCREEN = not GameConfig.FULLSCREEN
        flags = pygame.FULLSCREEN if GameConfig.FULLSCREEN else 0
        self._screen = pygame.display.set_mode(GameConfig.get_window_size(), flags)
        print(f"[Game] Fullscreen: {GameConfig.FULLSCREEN}")

    def _toggle_pause(self) -> None:
        """Bascule entre pause et jeu."""
        if self._state == GameState.PLAYING:
            self._state = GameState.PAUSED
            print("[Game] Jeu en pause")
        elif self._state == GameState.PAUSED:
            self._state = GameState.PLAYING
            print("[Game] Reprise du jeu")

    def _cleanup(self) -> None:
        """Nettoie les ressources avant de quitter."""
        print("[Game] Nettoyage des ressources...")
        pygame.quit()
        print("[Game] Jeu terminé")


def main() -> None:
    """
    Fonction principale du programme.

    Point d'entrée de l'application.
    """
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"[ERROR] Une erreur s'est produite: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
