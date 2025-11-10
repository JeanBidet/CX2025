"""
Script de test pour vérifier que tous les imports fonctionnent correctement.
"""

print("Test des imports...")

try:
    print("  - Import pygame...")
    import pygame
    print(f"    OK - Pygame version {pygame.version.ver}")

    print("  - Import config...")
    from config.game_config import GameConfig
    from config.constants import GameState, Colors
    print("    OK")

    print("  - Import utils...")
    from utils.vector2 import Vector2
    v = Vector2(10, 20)
    print(f"    OK - Vector2 test: {v}")

    print("  - Import entities...")
    from entities.entity import Entity
    e = Entity("Test")
    print(f"    OK - Entity test: {e}")

    print("  - Import components...")
    from components.icomponent import IComponent
    from components.renderer_component import RendererComponent
    from components.movement_component import MovementComponent
    print("    OK")

    print("  - Import systems...")
    from systems.entity_manager import EntityManager
    from systems.scene_manager import SceneManager
    em = EntityManager()
    sm = SceneManager()
    print(f"    OK - EntityManager: {em}, SceneManager: {sm}")

    print("  - Import scenes...")
    from scenes.scene import Scene
    from scenes.test_scene import TestScene
    print("    OK")

    print("\n[OK] Tous les imports fonctionnent correctement!")
    print("\nTest de fonctionnement basique:")

    # Test Entity-Component
    print("  - Creation d'une entite avec composants...")
    player = Entity("Player")
    player.position = Vector2(100, 200)
    player.add_component(MovementComponent, 200.0)
    print(f"    OK - Player: {player}")
    print(f"    Position: {player.position}")

    # Test Entity Manager
    print("  - Ajout a l'Entity Manager...")
    em.add_entity(player)
    print(f"    OK - Entites gerees: {em.entity_count()}")

    # Test mise a jour
    print("  - Test de mise a jour...")
    em.update(0.016)
    print("    OK")

    print("\n[OK] Architecture fonctionnelle!")

except ImportError as e:
    print(f"\n[ERREUR] Erreur d'import: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"\n[ERREUR] Erreur: {e}")
    import traceback
    traceback.print_exc()
