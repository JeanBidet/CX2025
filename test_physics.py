"""
Script de test pour vérifier le système de physique.
"""

print("Test des imports du système de physique...")

try:
    print("  - Import config...")
    from config.game_config import GameConfig
    print(f"    OK - Max speed: {GameConfig.CYCLIST_MAX_SPEED}")

    print("  - Import utils...")
    from utils.vector2 import Vector2
    print("    OK")

    print("  - Import TransformComponent...")
    from components.transform_component import TransformComponent
    print("    OK")

    print("  - Import PhysicsComponent...")
    from components.physics_component import PhysicsComponent
    print("    OK")

    print("  - Import InputComponent...")
    from components.input_component import InputComponent
    print("    OK")

    print("  - Import SpriteRendererComponent...")
    from components.sprite_renderer_component import SpriteRendererComponent
    print("    OK")

    print("  - Import Cyclist...")
    from entities.cyclist import Cyclist
    print("    OK")

    print("  - Import PhysicsTestScene...")
    from scenes.physics_test_scene import PhysicsTestScene
    print("    OK")

    print("\n[OK] Tous les imports fonctionnent!")

    print("\nTest de creation d'un cycliste...")
    cyclist = Cyclist("TestCyclist", Vector2(100, 100), is_player=True)
    print(f"  OK - {cyclist}")

    # Vérifie les composants
    transform = cyclist.get_transform()
    print(f"  Transform: {transform}")

    physics = cyclist.get_physics()
    print(f"  Physics: {physics}")

    input_comp = cyclist.get_input()
    print(f"  Input: {input_comp}")

    print("\n[OK] Systeme de physique fonctionnel!")

except ImportError as e:
    print(f"\n[ERREUR] Erreur d'import: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"\n[ERREUR] Erreur: {e}")
    import traceback
    traceback.print_exc()
