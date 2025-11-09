#!/usr/bin/env python3
"""
Example: Custom Race Configuration
Demonstrates how to customize the CX2025 cyclocross game with different settings
"""

from cyclocross_game import (
    RaceCourse, Racer, CyclocrossRace, Weather, Terrain, Obstacle,
    create_ai_racers
)


def example_short_sprint_race():
    """Example: Quick 3-lap sprint race"""
    print("\n🏁 EXAMPLE 1: Short Sprint Race (3 laps)")
    print("-" * 60)
    
    course = RaceCourse(
        laps=3,
        length_km=1.5,
        weather=Weather.SUNNY
    )
    
    racers = create_ai_racers(6)  # Only 6 racers for faster race
    race = CyclocrossRace(course, racers, show_commentary=True)
    race.run_race()


def example_endurance_race():
    """Example: Long endurance race in challenging conditions"""
    print("\n🏁 EXAMPLE 2: Endurance Race (8 laps, rainy conditions)")
    print("-" * 60)
    
    course = RaceCourse(
        laps=8,
        length_km=3.0,
        weather=Weather.RAINY,
        terrain_mix={
            Terrain.MUD: 0.4,      # Lots of mud in rain
            Terrain.GRASS: 0.3,
            Terrain.GRAVEL: 0.2,
            Terrain.PAVEMENT: 0.1
        }
    )
    
    racers = create_ai_racers(10)  # Larger field
    race = CyclocrossRace(course, racers, show_commentary=False)  # Less commentary
    race.run_race()


def example_custom_racers():
    """Example: Create custom racers with specific attributes"""
    print("\n🏁 EXAMPLE 3: Custom Racers with Defined Skills")
    print("-" * 60)
    
    course = RaceCourse(
        laps=5,
        length_km=2.5,
        weather=Weather.CLOUDY
    )
    
    # Create custom racers with specific attributes
    racers = [
        Racer(name="The Champion", skill_level=0.95, race_strategy="balanced"),
        Racer(name="Speed Demon", skill_level=0.85, race_strategy="aggressive"),
        Racer(name="Steady Eddie", skill_level=0.75, race_strategy="conservative"),
        Racer(name="Rising Star", skill_level=0.80, race_strategy="balanced"),
        Racer(name="The Veteran", skill_level=0.90, race_strategy="conservative"),
        Racer(name="Wild Card", skill_level=0.70, race_strategy="aggressive"),
    ]
    
    race = CyclocrossRace(course, racers, show_commentary=True)
    race.run_race()


def example_technical_course():
    """Example: Technical course with many obstacles"""
    print("\n🏁 EXAMPLE 4: Technical Course (Heavy Obstacles)")
    print("-" * 60)
    
    course = RaceCourse(
        laps=4,
        length_km=2.0,
        weather=Weather.FOGGY,
        obstacles=[
            Obstacle.BARRIERS,
            Obstacle.STAIRS,
            Obstacle.LOG_JUMP,
            Obstacle.STEEP_CLIMB,
            Obstacle.SHARP_TURN,
            Obstacle.BARRIERS,  # Double barriers
            Obstacle.STAIRS,    # More stairs
        ]
    )
    
    # Create racers with varying skill levels
    racers = create_ai_racers(8)
    race = CyclocrossRace(course, racers, show_commentary=True)
    race.run_race()


def main():
    """Run example races"""
    print("\n" + "="*60)
    print("🚴 CX2025 - CUSTOM RACE EXAMPLES")
    print("   Demonstrating different race configurations")
    print("="*60)
    
    examples = [
        ("1", "Short Sprint Race", example_short_sprint_race),
        ("2", "Endurance Race", example_endurance_race),
        ("3", "Custom Racers", example_custom_racers),
        ("4", "Technical Course", example_technical_course),
    ]
    
    print("\nAvailable examples:")
    for num, name, _ in examples:
        print(f"  {num}. {name}")
    
    print("\nSelect an example (1-4) or 'all' to run all examples:")
    try:
        choice = input("> ").strip().lower()
        
        if choice == "all":
            for _, _, func in examples:
                func()
                input("\nPress Enter to continue to next example...")
        elif choice in ["1", "2", "3", "4"]:
            idx = int(choice) - 1
            examples[idx][2]()
        else:
            print("Invalid choice. Running Example 1 by default.")
            example_short_sprint_race()
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting examples.")
    
    print("\n" + "="*60)
    print("Examples complete! Try modifying the code to create your own races.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
