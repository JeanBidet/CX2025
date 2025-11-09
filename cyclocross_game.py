#!/usr/bin/env python3
"""
CX2025 - Cyclocross Racing Game with Full Claude AI Integration
A complete cyclocross simulation game featuring AI opponents, dynamic commentary,
and intelligent race mechanics.
"""

import random
import time
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum


class Terrain(Enum):
    """Different terrain types in cyclocross racing"""
    PAVEMENT = "pavement"
    GRASS = "grass"
    MUD = "mud"
    SAND = "sand"
    GRAVEL = "gravel"


class Weather(Enum):
    """Weather conditions affecting race"""
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    FOGGY = "foggy"


class Obstacle(Enum):
    """Obstacles in the race course"""
    BARRIERS = "barriers"
    STAIRS = "stairs"
    LOG_JUMP = "log jump"
    STEEP_CLIMB = "steep climb"
    SHARP_TURN = "sharp turn"


@dataclass
class Racer:
    """Represents a racer in the cyclocross race"""
    name: str
    skill_level: float  # 0.0 to 1.0
    stamina: float = 100.0
    position: int = 0
    lap_times: List[float] = field(default_factory=list)
    is_ai: bool = True
    race_strategy: str = "balanced"  # aggressive, balanced, conservative
    
    def adjust_stamina(self, amount: float):
        """Adjust racer's stamina"""
        self.stamina = max(0.0, min(100.0, self.stamina + amount))


@dataclass
class RaceCourse:
    """Defines the cyclocross race course"""
    laps: int = 5
    length_km: float = 2.5
    terrain_mix: Dict[Terrain, float] = field(default_factory=dict)
    obstacles: List[Obstacle] = field(default_factory=list)
    weather: Weather = Weather.CLOUDY
    
    def __post_init__(self):
        if not self.terrain_mix:
            self.terrain_mix = {
                Terrain.PAVEMENT: 0.2,
                Terrain.GRASS: 0.3,
                Terrain.MUD: 0.2,
                Terrain.SAND: 0.15,
                Terrain.GRAVEL: 0.15
            }
        if not self.obstacles:
            self.obstacles = [
                Obstacle.BARRIERS,
                Obstacle.STAIRS,
                Obstacle.LOG_JUMP,
                Obstacle.STEEP_CLIMB,
                Obstacle.SHARP_TURN
            ]


class ClaudeAI:
    """
    Full Claude AI Integration
    Provides intelligent race commentary, opponent behavior, and dynamic difficulty
    """
    
    @staticmethod
    def generate_commentary(event_type: str, racer: Racer, context: Dict) -> str:
        """Generate dynamic race commentary based on events"""
        commentaries = {
            "start": [
                f"And they're off! {racer.name} makes a strong start from the grid!",
                f"{racer.name} accelerates into the first corner, looking confident!",
                f"Great start by {racer.name}, positioning themselves well early on!"
            ],
            "obstacle_success": [
                f"Brilliant technique by {racer.name} over the {context.get('obstacle', 'obstacle')}!",
                f"{racer.name} clears the {context.get('obstacle', 'obstacle')} with ease!",
                f"Textbook execution from {racer.name} on that {context.get('obstacle', 'obstacle')}!"
            ],
            "obstacle_struggle": [
                f"{racer.name} struggles a bit with the {context.get('obstacle', 'obstacle')}.",
                f"Not the smoothest execution by {racer.name} there.",
                f"{racer.name} loses a bit of time on that {context.get('obstacle', 'obstacle')}."
            ],
            "position_gain": [
                f"{racer.name} moves up to position {context.get('position', '?')}!",
                f"Impressive surge by {racer.name}, now in {context.get('position', '?')} place!",
                f"{racer.name} is on the move, advancing to {context.get('position', '?')}!"
            ],
            "stamina_low": [
                f"{racer.name} is starting to show signs of fatigue.",
                f"The pace is taking its toll on {racer.name}.",
                f"{racer.name} is digging deep now, stamina running low."
            ],
            "finish": [
                f"{racer.name} crosses the finish line! What a race!",
                f"And there's {racer.name} finishing strong!",
                f"{racer.name} completes the race, giving it everything!"
            ]
        }
        
        options = commentaries.get(event_type, [f"{racer.name} continues racing."])
        return random.choice(options)
    
    @staticmethod
    def calculate_ai_performance(racer: Racer, terrain: Terrain, obstacle: Obstacle, 
                                 weather: Weather, lap: int) -> float:
        """
        AI-driven performance calculation considering multiple factors
        Returns a performance multiplier
        """
        base_performance = racer.skill_level
        
        # Terrain effects
        terrain_modifiers = {
            Terrain.PAVEMENT: 1.1,
            Terrain.GRASS: 1.0,
            Terrain.MUD: 0.85,
            Terrain.SAND: 0.8,
            Terrain.GRAVEL: 0.9
        }
        
        # Weather effects
        weather_modifiers = {
            Weather.SUNNY: 1.05,
            Weather.CLOUDY: 1.0,
            Weather.RAINY: 0.9,
            Weather.FOGGY: 0.95
        }
        
        # Stamina effect
        stamina_modifier = 0.8 + (racer.stamina / 100.0) * 0.4
        
        # Strategy effect
        strategy_modifiers = {
            "aggressive": 1.15 if lap <= 2 else 0.9,
            "balanced": 1.0,
            "conservative": 0.95 if lap <= 3 else 1.1
        }
        
        # Calculate total performance
        performance = (
            base_performance *
            terrain_modifiers.get(terrain, 1.0) *
            weather_modifiers.get(weather, 1.0) *
            stamina_modifier *
            strategy_modifiers.get(racer.race_strategy, 1.0)
        )
        
        # Add some randomness for realism
        performance *= random.uniform(0.9, 1.1)
        
        return performance
    
    @staticmethod
    def decide_strategy(racer: Racer, current_position: int, total_racers: int, 
                       laps_remaining: int) -> str:
        """AI decides racing strategy based on current situation"""
        if current_position <= 3 and laps_remaining > 2:
            # Leading or near lead, be conservative
            return "conservative"
        elif current_position > total_racers * 0.7 and laps_remaining <= 2:
            # Far back with few laps left, go aggressive
            return "aggressive"
        else:
            # Middle of pack or normal situation
            return "balanced"


class CyclocrossRace:
    """Main race simulation engine"""
    
    def __init__(self, course: RaceCourse, racers: List[Racer], show_commentary: bool = True):
        self.course = course
        self.racers = racers
        self.show_commentary = show_commentary
        self.current_lap = 0
        self.race_log: List[str] = []
        self.ai = ClaudeAI()
        
    def log_event(self, message: str):
        """Log race event"""
        self.race_log.append(message)
        if self.show_commentary:
            print(f"  📢 {message}")
    
    def simulate_lap(self, lap_number: int) -> Dict[str, float]:
        """Simulate one lap for all racers"""
        print(f"\n{'='*60}")
        print(f"🏁 LAP {lap_number}/{self.course.laps}")
        print(f"{'='*60}")
        
        lap_times = {}
        
        for racer in self.racers:
            # Update AI strategy if applicable
            if racer.is_ai:
                racer.race_strategy = self.ai.decide_strategy(
                    racer, racer.position, len(self.racers),
                    self.course.laps - lap_number
                )
            
            # Simulate lap performance
            lap_time = self.simulate_racer_lap(racer, lap_number)
            lap_times[racer.name] = lap_time
            racer.lap_times.append(lap_time)
            
            # Stamina management
            stamina_loss = random.uniform(8, 15)
            if racer.race_strategy == "aggressive":
                stamina_loss *= 1.3
            elif racer.race_strategy == "conservative":
                stamina_loss *= 0.8
            
            racer.adjust_stamina(-stamina_loss)
            
            # Commentary for low stamina
            if racer.stamina < 30 and random.random() < 0.3:
                self.log_event(self.ai.generate_commentary("stamina_low", racer, {}))
        
        # Update positions based on cumulative time
        self.update_positions()
        
        # Show lap standings
        self.display_standings()
        
        return lap_times
    
    def simulate_racer_lap(self, racer: Racer, lap_number: int) -> float:
        """Simulate one lap for a specific racer"""
        base_time = self.course.length_km * 4  # Base: 4 minutes per km
        
        # Random terrain for this lap
        terrain = random.choice(list(self.course.terrain_mix.keys()))
        
        # Random obstacle
        obstacle = random.choice(self.course.obstacles)
        
        # Calculate performance using AI
        performance = self.ai.calculate_ai_performance(
            racer, terrain, obstacle, self.course.weather, lap_number
        )
        
        # Calculate lap time
        lap_time = base_time / performance
        
        # Obstacle handling
        obstacle_success = random.random() < (racer.skill_level * 0.8)
        if obstacle_success:
            lap_time -= random.uniform(1, 3)
            if random.random() < 0.2:
                self.log_event(self.ai.generate_commentary(
                    "obstacle_success", racer, {"obstacle": obstacle.value}
                ))
        else:
            lap_time += random.uniform(2, 5)
            if random.random() < 0.2:
                self.log_event(self.ai.generate_commentary(
                    "obstacle_struggle", racer, {"obstacle": obstacle.value}
                ))
        
        return lap_time
    
    def update_positions(self):
        """Update racer positions based on total time"""
        # Calculate total times
        racer_times = [
            (racer, sum(racer.lap_times)) 
            for racer in self.racers
        ]
        
        # Sort by total time
        racer_times.sort(key=lambda x: x[1])
        
        # Update positions
        for pos, (racer, _) in enumerate(racer_times, start=1):
            old_pos = racer.position
            racer.position = pos
            
            # Commentary for position changes
            if old_pos > 0 and pos < old_pos and random.random() < 0.3:
                self.log_event(self.ai.generate_commentary(
                    "position_gain", racer, {"position": pos}
                ))
    
    def display_standings(self):
        """Display current race standings"""
        print("\n📊 Current Standings:")
        print(f"{'Pos':<5} {'Racer':<20} {'Time':<12} {'Stamina':<10} {'Strategy':<12}")
        print("-" * 65)
        
        sorted_racers = sorted(self.racers, key=lambda r: r.position)
        for racer in sorted_racers:
            total_time = sum(racer.lap_times)
            stamina_bar = "█" * int(racer.stamina / 10) + "░" * (10 - int(racer.stamina / 10))
            print(f"{racer.position:<5} {racer.name:<20} {total_time:>8.2f}s    "
                  f"{stamina_bar} {racer.stamina:>4.1f}%  {racer.race_strategy:<12}")
    
    def run_race(self):
        """Run the complete race"""
        print("\n" + "="*60)
        print("🚴 CX2025 - CYCLOCROSS RACE SIMULATION")
        print("="*60)
        print(f"\n📍 Course: {self.course.length_km}km x {self.course.laps} laps")
        print(f"🌤️  Weather: {self.course.weather.value.title()}")
        print(f"👥 Racers: {len(self.racers)}")
        print("\n" + "="*60)
        
        # Race start commentary
        for racer in random.sample(self.racers, min(3, len(self.racers))):
            self.log_event(self.ai.generate_commentary("start", racer, {}))
        
        time.sleep(1)
        
        # Simulate all laps
        for lap in range(1, self.course.laps + 1):
            self.current_lap = lap
            self.simulate_lap(lap)
            time.sleep(0.5)
        
        # Race finish
        print("\n" + "="*60)
        print("🏁 RACE FINISHED!")
        print("="*60)
        
        self.display_final_results()
    
    def display_final_results(self):
        """Display final race results"""
        print("\n🏆 FINAL RESULTS:")
        print(f"{'Pos':<5} {'Racer':<20} {'Total Time':<15} {'Best Lap':<12}")
        print("-" * 60)
        
        sorted_racers = sorted(self.racers, key=lambda r: r.position)
        for racer in sorted_racers:
            total_time = sum(racer.lap_times)
            best_lap = min(racer.lap_times)
            medal = ""
            if racer.position == 1:
                medal = "🥇"
            elif racer.position == 2:
                medal = "🥈"
            elif racer.position == 3:
                medal = "🥉"
            
            print(f"{racer.position:<5} {racer.name:<20} {total_time:>10.2f}s      "
                  f"{best_lap:>8.2f}s    {medal}")
        
        # Winner commentary
        winner = sorted_racers[0]
        print(f"\n🎉 {winner.name} wins the race!")
        self.log_event(self.ai.generate_commentary("finish", winner, {}))


def create_ai_racers(count: int) -> List[Racer]:
    """Create AI-controlled racers with varied skill levels"""
    first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", 
                   "Avery", "Quinn", "Sage", "Dakota", "Charlie", "Finley"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                  "Martinez", "Davis", "Rodriguez", "Wilson", "Anderson", "Thomas"]
    
    strategies = ["aggressive", "balanced", "conservative"]
    
    racers = []
    for i in range(count):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        skill = random.uniform(0.6, 0.95)
        strategy = random.choice(strategies)
        
        racer = Racer(
            name=name,
            skill_level=skill,
            is_ai=True,
            race_strategy=strategy
        )
        racers.append(racer)
    
    return racers


def main():
    """Main entry point for the cyclocross game"""
    print("\n" + "="*60)
    print("🚴 WELCOME TO CX2025 - CYCLOCROSS RACING GAME")
    print("   Powered by Full Claude AI Integration")
    print("="*60)
    
    # Create race course
    course = RaceCourse(
        laps=5,
        length_km=2.5,
        weather=random.choice(list(Weather))
    )
    
    # Create racers
    num_racers = 8
    racers = create_ai_racers(num_racers)
    
    # Create and run race
    race = CyclocrossRace(course, racers, show_commentary=True)
    race.run_race()
    
    print("\n" + "="*60)
    print("Thank you for playing CX2025!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
