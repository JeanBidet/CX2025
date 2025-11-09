# CX2025 - Cyclocross Racing Game 🚴

**Jeux de cyclo cross** - A complete cyclocross racing simulation game powered by Full Claude AI Integration.

## 🎮 Overview

CX2025 is an advanced cyclocross racing simulation that features intelligent AI opponents, dynamic race commentary, and realistic race mechanics. The game simulates the challenging world of cyclocross racing with varied terrain, weather conditions, obstacles, and strategic decision-making.

## ✨ Features

### Full Claude AI Integration

- **Intelligent AI Opponents**: Each AI racer has unique skill levels and racing strategies (aggressive, balanced, conservative)
- **Dynamic Race Commentary**: Real-time commentary on race events, obstacles, and position changes
- **Adaptive Strategy**: AI racers adjust their strategy based on position, stamina, and laps remaining
- **Performance Calculation**: Advanced AI considers terrain, weather, stamina, and strategy for realistic racing

### Race Mechanics

- **Multiple Terrain Types**: Pavement, grass, mud, sand, and gravel
- **Weather Conditions**: Sunny, cloudy, rainy, and foggy weather affecting race performance
- **Cyclocross Obstacles**: Barriers, stairs, log jumps, steep climbs, and sharp turns
- **Stamina Management**: Racers must manage energy throughout the race
- **Strategic Racing**: Different racing strategies impact performance over time

### Race Simulation

- **Multi-lap Races**: Configurable number of laps and course length
- **Real-time Standings**: Live position updates and timing information
- **Performance Tracking**: Lap times, best lap, and total race time
- **Visual Feedback**: Stamina bars, medals for top finishers, and race emojis

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- No external dependencies required!

### Installation

1. Clone the repository:
```bash
git clone https://github.com/JeanBidet/CX2025.git
cd CX2025
```

2. Run the game:
```bash
python3 cyclocross_game.py
```

Or make it executable:
```bash
chmod +x cyclocross_game.py
./cyclocross_game.py
```

## 🎯 How to Play

The game runs automatically when started. You'll see:

1. **Race Setup**: Course details, weather conditions, and racer lineup
2. **Lap-by-Lap Action**: Commentary and standings for each lap
3. **Final Results**: Complete race results with podium finishes

### Sample Output

```
🚴 CX2025 - CYCLOCROSS RACE SIMULATION
============================================================
📍 Course: 2.5km x 5 laps
🌤️  Weather: Cloudy
👥 Racers: 8

============================================================
🏁 LAP 1/5
============================================================
  📢 And they're off! Alex Smith makes a strong start from the grid!
  📢 Brilliant technique by Jordan Johnson over the barriers!

📊 Current Standings:
Pos   Racer                Time         Stamina    Strategy    
-----------------------------------------------------------------
1     Alex Smith           9.85s        ██████████ 92.3%  balanced    
2     Jordan Johnson       10.12s       █████████░ 88.7%  aggressive  
...
```

## 🏗️ Architecture

### Core Components

1. **Racer Class**: Represents individual racers with attributes like skill level, stamina, and strategy
2. **RaceCourse Class**: Defines the race environment with terrain, obstacles, and weather
3. **ClaudeAI Class**: The heart of the AI system, providing:
   - Dynamic commentary generation
   - Performance calculation algorithms
   - Strategy decision-making
4. **CyclocrossRace Class**: Main race simulation engine that orchestrates the race

### AI Intelligence

The Claude AI system uses multiple factors for decision-making:

- **Performance Modifiers**: Terrain (0.8-1.1x), Weather (0.9-1.05x), Stamina (0.8-1.2x)
- **Strategy Impact**: Affects performance based on race progress
- **Obstacle Success**: Skill-based probability for clearing obstacles
- **Dynamic Adaptation**: Strategies change based on race position and remaining laps

## 🔧 Customization

You can customize the race by modifying these parameters in the code:

```python
# In main() function:
course = RaceCourse(
    laps=5,              # Number of laps
    length_km=2.5,       # Course length in kilometers
    weather=Weather.RAINY  # Force specific weather
)

num_racers = 8  # Number of AI racers
```

### Custom Race Examples

Run the included examples to see different race configurations:

```bash
python3 example_custom_race.py
```

The examples demonstrate:
- **Short Sprint Race**: Quick 3-lap race with 6 racers
- **Endurance Race**: Long 8-lap race in rainy, muddy conditions
- **Custom Racers**: Define specific racer attributes and strategies
- **Technical Course**: Obstacle-heavy course in foggy conditions

## 📊 Race Statistics

The game tracks:
- Individual lap times for each racer
- Total race time
- Best lap time
- Position changes throughout the race
- Stamina levels
- Racing strategies employed

## 🏆 Scoring

- 🥇 1st Place: Gold Medal
- 🥈 2nd Place: Silver Medal
- 🥉 3rd Place: Bronze Medal

## 🤖 AI Strategies

1. **Aggressive**: Higher early performance, risks stamina depletion
2. **Balanced**: Consistent performance throughout the race
3. **Conservative**: Saves energy early, strong finish

## 🛠️ Technical Details

- **Language**: Python 3.7+
- **Dependencies**: None (uses Python standard library only)
- **Architecture**: Object-oriented design with dataclasses
- **AI System**: Rule-based AI with probabilistic elements

## 📝 License

This project is open source and available for educational and entertainment purposes.

## 🙏 Acknowledgments

- Inspired by the exciting world of cyclocross racing
- Powered by Full Claude AI Integration for intelligent gameplay

## 🐛 Troubleshooting

If you encounter any issues:

1. Ensure Python 3.7+ is installed: `python3 --version`
2. Check file permissions if executable fails: `chmod +x cyclocross_game.py`
3. Run directly with Python: `python3 cyclocross_game.py`

## 🎉 Enjoy the Race!

Experience the thrill of cyclocross racing with intelligent AI opponents and dynamic race commentary. May the best racer win! 🏁
