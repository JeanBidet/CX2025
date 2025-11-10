"""
Script de test pour le State Pattern.
"""

print("Test du State Pattern...")

try:
    print("\n1. Test des imports...")
    from systems.cyclist_state import StateType, ICyclistState
    from systems.cyclist_states import RidingState, CarryingState, RemountingState, CrashedState
    from systems.animation_system import Animation, AnimationController
    from components.state_machine_component import StateMachineComponent
    from entities.cyclist_with_states import CyclistWithStates
    from utils.sprite_generator import SpriteGenerator
    from utils.vector2 import Vector2
    import pygame
    print("  [OK] Tous les imports fonctionnent")

    print("\n2. Test de StateType enum...")
    assert StateType.RIDING
    assert StateType.CARRYING
    assert StateType.REMOUNTING
    assert StateType.CRASHED
    print(f"  [OK] {len(list(StateType))} états définis")

    print("\n3. Test des états concrets...")
    riding = RidingState()
    assert riding.state_type == StateType.RIDING
    print(f"  [OK] RidingState: {riding.state_type.name}")

    carrying = CarryingState()
    assert carrying.state_type == StateType.CARRYING
    print(f"  [OK] CarryingState: {carrying.state_type.name}")

    remounting = RemountingState(duration=1.0)
    assert remounting.state_type == StateType.REMOUNTING
    print(f"  [OK] RemountingState: {remounting.state_type.name}")

    crashed = CrashedState(recovery_duration=2.0)
    assert crashed.state_type == StateType.CRASHED
    print(f"  [OK] CrashedState: {crashed.state_type.name}")

    print("\n4. Test des transitions autorisées...")
    # RIDING peut aller vers CARRYING ou CRASHED
    assert riding.can_transition_to(StateType.CARRYING)
    assert riding.can_transition_to(StateType.CRASHED)
    assert not riding.can_transition_to(StateType.REMOUNTING)
    print("  [OK] RIDING -> CARRYING, CRASHED")

    # CARRYING peut aller vers REMOUNTING ou CRASHED
    assert carrying.can_transition_to(StateType.REMOUNTING)
    assert carrying.can_transition_to(StateType.CRASHED)
    assert not carrying.can_transition_to(StateType.RIDING)
    print("  [OK] CARRYING -> REMOUNTING, CRASHED")

    # REMOUNTING peut aller vers RIDING ou CRASHED
    assert remounting.can_transition_to(StateType.RIDING)
    assert remounting.can_transition_to(StateType.CRASHED)
    assert not remounting.can_transition_to(StateType.CARRYING)
    print("  [OK] REMOUNTING -> RIDING, CRASHED")

    # CRASHED peut uniquement aller vers REMOUNTING
    assert crashed.can_transition_to(StateType.REMOUNTING)
    assert not crashed.can_transition_to(StateType.RIDING)
    assert not crashed.can_transition_to(StateType.CARRYING)
    print("  [OK] CRASHED -> REMOUNTING")

    print("\n5. Test du système d'animation...")
    # Crée des frames de test
    test_frames = [pygame.Surface((10, 10)) for _ in range(4)]
    anim = Animation(test_frames, frame_duration=0.1, loop=True)

    assert anim.get_frame_count() == 4
    assert not anim.is_finished()  # Loop = True
    print(f"  [OK] Animation créée: {anim}")

    # Test update
    anim.update(0.15)  # Plus de 0.1s → devrait passer à frame 1
    frame = anim.get_current_frame()
    assert frame is not None
    print("  [OK] Animation update fonctionne")

    # Test AnimationController
    controller = AnimationController()
    controller.add_animation('test', anim)
    controller.play('test')
    assert controller.get_current_animation_name() == 'test'
    print(f"  [OK] AnimationController: {controller}")

    print("\n6. Test du SpriteGenerator...")
    riding_frames = SpriteGenerator.generate_riding_frames()
    assert len(riding_frames) == 4
    assert isinstance(riding_frames[0], pygame.Surface)
    print(f"  [OK] Riding frames: {len(riding_frames)}")

    carrying_frames = SpriteGenerator.generate_carrying_frames()
    assert len(carrying_frames) == 4
    print(f"  [OK] Carrying frames: {len(carrying_frames)}")

    remounting_frames = SpriteGenerator.generate_remounting_frames()
    assert len(remounting_frames) == 3
    print(f"  [OK] Remounting frames: {len(remounting_frames)}")

    crashed_frames = SpriteGenerator.generate_crashed_frames()
    assert len(crashed_frames) == 4
    print(f"  [OK] Crashed frames: {len(crashed_frames)}")

    print("\n7. Test du StateMachineComponent...")
    from entities.entity import Entity

    test_entity = Entity("TestEntity")
    state_machine = test_entity.add_component(
        StateMachineComponent,
        initial_state=StateType.RIDING
    )

    # Ajoute les états
    state_machine.add_state(StateType.RIDING, RidingState())
    state_machine.add_state(StateType.CARRYING, CarryingState())
    state_machine.add_state(StateType.REMOUNTING, RemountingState())
    state_machine.add_state(StateType.CRASHED, CrashedState())

    assert state_machine.get_state_count() == 4
    print(f"  [OK] StateMachine créée: {state_machine}")

    # Force initial state
    state_machine.change_state(StateType.RIDING, force=True)
    assert state_machine.is_in_state(StateType.RIDING)
    print("  [OK] État initial: RIDING")

    # Test transition valide: RIDING -> CARRYING
    success = state_machine.change_state(StateType.CARRYING)
    assert success
    assert state_machine.is_in_state(StateType.CARRYING)
    print("  [OK] Transition RIDING -> CARRYING reussie")

    # Test transition invalide: CARRYING -> RIDING (non autorisee)
    success = state_machine.change_state(StateType.RIDING)
    assert not success  # Devrait echouer
    assert state_machine.is_in_state(StateType.CARRYING)  # Toujours en CARRYING
    print("  [OK] Transition invalide CARRYING -> RIDING bloquee")

    # Test transition valide: CARRYING -> REMOUNTING
    success = state_machine.change_state(StateType.REMOUNTING)
    assert success
    assert state_machine.is_in_state(StateType.REMOUNTING)
    print("  [OK] Transition CARRYING -> REMOUNTING reussie")

    print("\n8. Test du CyclistWithStates...")
    pygame.init()

    cyclist = CyclistWithStates(
        name="TestCyclist",
        position=Vector2(100, 100),
        is_player=True
    )

    assert cyclist.get_current_state() == StateType.RIDING
    print(f"  [OK] Cyclist créé: {cyclist}")

    # Vérifie que l'animation controller existe
    assert cyclist.animation_controller is not None
    assert cyclist.animation_controller.has_animation('pedal')
    assert cyclist.animation_controller.has_animation('walk')
    assert cyclist.animation_controller.has_animation('mount')
    assert cyclist.animation_controller.has_animation('fall')
    print("  [OK] Toutes les animations chargées")

    # Vérifie que la state machine existe
    assert cyclist.state_machine is not None
    assert cyclist.state_machine.get_state_count() == 4
    print("  [OK] State machine configurée")

    # Test trigger crash
    cyclist.trigger_crash()
    assert cyclist.get_current_state() == StateType.CRASHED
    print("  [OK] Trigger crash fonctionne")

    print("\n9. Test du cycle complet des transitions...")
    # Reset à RIDING
    cyclist.state_machine.change_state(StateType.RIDING, force=True)
    assert cyclist.get_current_state() == StateType.RIDING

    # RIDING -> CARRYING
    cyclist.state_machine.change_state(StateType.CARRYING)
    assert cyclist.get_current_state() == StateType.CARRYING

    # CARRYING -> REMOUNTING
    cyclist.state_machine.change_state(StateType.REMOUNTING)
    assert cyclist.get_current_state() == StateType.REMOUNTING

    # Simule le timer (normalement automatique)
    cyclist.state_machine.change_state(StateType.RIDING, force=True)
    assert cyclist.get_current_state() == StateType.RIDING

    print("  [OK] Cycle complet: RIDING -> CARRYING -> REMOUNTING -> RIDING")

    print("\n" + "="*60)
    print("[SUCCESS] Tous les tests du State Pattern passent!")
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
