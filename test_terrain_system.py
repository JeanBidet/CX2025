"""
Script de test pour le système de terrain.
"""

print("Test du système de terrain...")

try:
    print("\n1. Test des imports...")
    from systems.terrain_data import TerrainType, TerrainData
    from patterns.factories.terrain_factory import TerrainFactory
    from systems.terrain_tile import TerrainTile
    from systems.terrain_manager import TerrainManager
    from components.terrain_physics_component import TerrainPhysicsComponent
    from utils.terrain_map_loader import TerrainMapLoader
    from utils.vector2 import Vector2
    print("  [OK] Tous les imports fonctionnent")

    print("\n2. Test du TerrainType enum...")
    assert TerrainType.ASPHALT
    assert TerrainType.GRASS
    assert TerrainType.SAND
    assert TerrainType.MUD
    assert TerrainType.GRAVEL
    assert TerrainType.DIRT
    assert TerrainType.CONCRETE
    print(f"  [OK] {len(list(TerrainType))} types de terrain disponibles")

    print("\n3. Test de TerrainFactory...")
    asphalt = TerrainFactory.create(TerrainType.ASPHALT)
    assert asphalt.terrain_type == TerrainType.ASPHALT
    assert asphalt.speed_multiplier == 1.0
    assert asphalt.grip_level == 0.9
    print(f"  [OK] Asphalte: {asphalt.name} (vitesse={asphalt.speed_multiplier})")

    grass = TerrainFactory.create(TerrainType.GRASS)
    assert grass.speed_multiplier == 0.7
    print(f"  [OK] Herbe: {grass.name} (vitesse={grass.speed_multiplier})")

    sand = TerrainFactory.create(TerrainType.SAND)
    assert sand.speed_multiplier == 0.5
    print(f"  [OK] Sable: {sand.name} (vitesse={sand.speed_multiplier})")

    mud = TerrainFactory.create(TerrainType.MUD)
    assert mud.speed_multiplier == 0.4
    assert mud.grip_level == 0.3
    print(f"  [OK] Boue: {mud.name} (vitesse={mud.speed_multiplier})")

    concrete = TerrainFactory.create(TerrainType.CONCRETE)
    assert concrete.speed_multiplier == 1.1
    assert concrete.grip_level == 0.95
    print(f"  [OK] Beton: {concrete.name} (vitesse={concrete.speed_multiplier})")

    # Test du cache
    asphalt2 = TerrainFactory.create(TerrainType.ASPHALT)
    assert asphalt is asphalt2  # Même instance grâce au cache
    print("  [OK] Cache du factory fonctionne")

    print("\n4. Test de TerrainTile...")
    tile = TerrainTile(asphalt, 0, 0, 32)
    assert tile.grid_x == 0
    assert tile.grid_y == 0
    assert tile.tile_size == 32
    assert tile.rect.width == 32
    assert tile.rect.height == 32
    print(f"  [OK] Tuile créée: {tile}")

    # Test contains
    assert tile.contains(Vector2(16, 16))  # Centre de la tuile
    assert tile.contains(Vector2(0, 0))    # Coin
    assert not tile.contains(Vector2(50, 50))  # Dehors
    print("  [OK] Détection de collision fonctionne")

    print("\n5. Test de TerrainManager...")
    manager = TerrainManager(10, 10, 32)
    assert manager.width == 10
    assert manager.height == 10
    assert manager.get_world_width() == 320
    assert manager.get_world_height() == 320
    print(f"  [OK] Manager créé: {manager}")

    # Test get_tile_at_grid
    tile = manager.get_tile_at_grid(5, 5)
    assert tile is not None
    assert tile.grid_x == 5
    assert tile.grid_y == 5
    print("  [OK] Récupération de tuile par grille")

    # Test get_terrain_at_position
    tile = manager.get_terrain_at_position(Vector2(100, 100))
    assert tile is not None
    grid_x = 100 // 32  # = 3
    grid_y = 100 // 32  # = 3
    assert tile.grid_x == grid_x
    assert tile.grid_y == grid_y
    print("  [OK] Récupération de tuile par position")

    # Test hors limites
    tile = manager.get_tile_at_grid(100, 100)
    assert tile is None
    print("  [OK] Gestion des limites")

    print("\n6. Test de set_terrain_from_grid...")
    terrain_grid = [
        [TerrainType.ASPHALT] * 10,
        [TerrainType.GRASS] * 10,
        [TerrainType.SAND] * 10,
        [TerrainType.MUD] * 10,
        [TerrainType.GRAVEL] * 10,
        [TerrainType.DIRT] * 10,
        [TerrainType.CONCRETE] * 10,
        [TerrainType.GRASS] * 10,
        [TerrainType.GRASS] * 10,
        [TerrainType.GRASS] * 10,
    ]
    manager.set_terrain_from_grid(terrain_grid)

    # Vérifie que les terrains sont bien définis
    tile = manager.get_tile_at_grid(0, 0)
    assert tile.terrain_data.terrain_type == TerrainType.ASPHALT
    tile = manager.get_tile_at_grid(0, 1)
    assert tile.terrain_data.terrain_type == TerrainType.GRASS
    tile = manager.get_tile_at_grid(0, 2)
    assert tile.terrain_data.terrain_type == TerrainType.SAND
    print("  [OK] Configuration de terrain depuis grille")

    print("\n7. Test de TerrainMapLoader...")
    # Test create_test_map
    test_manager = TerrainMapLoader.create_test_map(20, 15)
    assert test_manager.width == 20
    assert test_manager.height == 15
    print(f"  [OK] Map de test créée: {test_manager}")

    # Test save et load
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_path = f.name

    try:
        TerrainMapLoader.save_to_file(test_manager, temp_path, "Test Map")
        print(f"  [OK] Map sauvegardée dans {temp_path}")

        loaded_manager = TerrainMapLoader.load_from_file(temp_path)
        assert loaded_manager.width == 20
        assert loaded_manager.height == 15
        print("  [OK] Map chargée depuis fichier")
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    print("\n8. Test de TerrainPhysicsComponent...")
    import pygame
    pygame.init()

    from entities.entity import Entity
    from components.transform_component import TransformComponent
    from components.physics_component import PhysicsComponent

    # Crée une entité de test
    entity = Entity("TestEntity")
    entity.add_component(TransformComponent, Vector2(100, 100))
    entity.add_component(PhysicsComponent, mass=70.0, drag=0.985, max_speed=450.0)

    # Crée un terrain manager simple
    simple_manager = TerrainManager(10, 10, 32)
    grid = [[TerrainType.SAND] * 10 for _ in range(10)]
    simple_manager.set_terrain_from_grid(grid)

    # Ajoute le TerrainPhysicsComponent
    terrain_comp = entity.add_component(
        TerrainPhysicsComponent,
        terrain_manager=simple_manager,
        base_max_speed=450.0,
        base_drag=0.985
    )
    print(f"  [OK] TerrainPhysicsComponent créé: {terrain_comp}")

    # Test update (devrait appliquer les effets du sable)
    physics = entity.get_component(PhysicsComponent)
    original_max_speed = physics.max_speed

    terrain_comp.update(0.016)  # Simule une frame

    # Sur du sable, la vitesse devrait être réduite à 50%
    expected_speed = 450.0 * 0.5  # speed_multiplier du sable = 0.5
    assert abs(physics.max_speed - expected_speed) < 0.1
    print(f"  [OK] Vitesse modifiée par terrain: {original_max_speed} -> {physics.max_speed}")

    # Test des getters
    assert terrain_comp.get_current_terrain_type() == TerrainType.SAND
    assert terrain_comp.get_current_terrain_name() == "Sable"
    assert terrain_comp.get_current_grip_level() == 0.4
    print("  [OK] Getters fonctionnent")

    print("\n" + "="*60)
    print("[SUCCESS] Tous les tests du système de terrain passent!")
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
