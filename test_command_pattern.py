"""
Script de test pour le Command Pattern.
"""

print("Test du Command Pattern...")

try:
    print("\n1. Test des imports...")
    from patterns.commands.command import ICommand, BaseCommand
    from patterns.commands.movement_commands import (
        AccelerateCommand,
        BrakeCommand,
        TurnLeftCommand,
        TurnRightCommand,
        SprintCommand,
        StopCommand
    )
    from patterns.commands.command_input_handler import CommandInputHandler
    from config.input_config import get_profile, list_available_profiles
    from components.command_input_component import CommandInputComponent
    print("  [OK] Tous les imports fonctionnent")

    print("\n2. Test des commandes...")
    accelerate = AccelerateCommand(force=1000.0)
    print(f"  [OK] {accelerate}")
    assert accelerate.name == "Accelerate"
    assert accelerate.priority == 10

    brake = BrakeCommand(force=1500.0)
    print(f"  [OK] {brake}")

    turn_left = TurnLeftCommand()
    print(f"  [OK] {turn_left}")

    sprint = SprintCommand()
    print(f"  [OK] {sprint}")

    stop = StopCommand()
    print(f"  [OK] {stop}")
    assert stop.priority == 50  # Plus haute priorité

    print("\n3. Test du CommandInputHandler...")
    import pygame
    pygame.init()

    handler = CommandInputHandler()
    handler.bind_key(pygame.K_UP, accelerate)
    handler.bind_key(pygame.K_DOWN, brake)
    handler.bind_event(pygame.K_SPACE, sprint)
    print(f"  [OK] Handler créé: {handler}")

    # Test du binding
    bound_keys = handler.get_bound_keys()
    print(f"  [OK] Touches liées: {len(bound_keys)}")
    assert pygame.K_UP in bound_keys

    print("\n4. Test des profils...")
    profiles = list_available_profiles()
    print(f"  [OK] Profils disponibles: {profiles}")
    assert "arrows" in profiles
    assert "wasd" in profiles
    assert "hybrid" in profiles

    # Test chargement profil
    profile = get_profile("hybrid")
    print(f"  [OK] Profil 'hybrid' chargé: {profile.name}")
    assert len(profile.key_bindings) > 0
    print(f"       Touches définies: {len(profile.key_bindings)}")

    print("\n5. Test CommandInputComponent...")
    from entities.entity import Entity
    from components.transform_component import TransformComponent
    from components.physics_component import PhysicsComponent
    from utils.vector2 import Vector2

    # Crée une entité de test
    entity = Entity("TestEntity")
    entity.add_component(TransformComponent, Vector2(100, 100))
    entity.add_component(PhysicsComponent, mass=70.0, drag=0.985, max_speed=450.0)

    # Ajoute le CommandInputComponent
    input_comp = entity.add_component(CommandInputComponent, profile_name="hybrid")
    print(f"  [OK] CommandInputComponent créé: {input_comp}")

    # Test changement de profil
    input_comp.load_profile("arrows")
    assert input_comp.get_profile_name() == "arrows"
    print(f"  [OK] Changement de profil vers 'arrows'")

    # Test enable/disable
    input_comp.disable()
    assert not input_comp.is_enabled()
    input_comp.enable()
    assert input_comp.is_enabled()
    print(f"  [OK] Enable/disable fonctionnel")

    print("\n6. Test de priorité des commandes...")
    commands = [
        StopCommand(),        # Priority 50
        SprintCommand(),      # Priority 20
        BrakeCommand(),       # Priority 15
        AccelerateCommand(),  # Priority 10
    ]

    # Tri par priorité
    commands.sort(key=lambda c: c.priority, reverse=True)
    assert commands[0].name == "Stop"
    assert commands[1].name == "Sprint"
    assert commands[2].name == "Brake"
    assert commands[3].name == "Accelerate"
    print(f"  [OK] Priorités correctement ordonnées")

    print("\n7. Test can_execute...")
    command = AccelerateCommand()
    assert command.can_execute(entity)  # A les composants nécessaires
    print(f"  [OK] can_execute retourne True pour entité valide")

    # Test avec entité sans composants
    empty_entity = Entity("Empty")
    assert not command.can_execute(empty_entity)
    print(f"  [OK] can_execute retourne False pour entité invalide")

    print("\n" + "="*60)
    print("[SUCCESS] Tous les tests du Command Pattern passent!")
    print("="*60)

except ImportError as e:
    print(f"\n[ERREUR] Import: {e}")
    import traceback
    traceback.print_exc()
except AssertionError as e:
    print(f"\n[ERREUR] Assertion: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"\n[ERREUR] {e}")
    import traceback
    traceback.print_exc()
finally:
    try:
        pygame.quit()
    except:
        pass
