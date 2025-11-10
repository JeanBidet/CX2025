# 🐍 Prompts Jeu Cyclo-Cross - Pygame Version

## 📚 Vue d'Ensemble

Série complète de 11 prompts pour créer un jeu de cyclo-cross 2D avec Pygame
et une architecture exemplaire utilisant les design patterns.

## 🎯 Stack Technique

- **Langage** : Python 3.10+
- **Framework** : Pygame
- **Style** : Type hints stricts (mypy compatible)
- **Architecture** : Entity-Component + Design Patterns
- **Vue** : Top-down 2D
- **Graphismes** : Pixel art simple

## 📋 Liste des Prompts

### ✅ Prompts Détaillés (1-5)

1. **prompt_pygame_01_architecture_base.txt**
   - Setup Pygame + environnement virtuel
   - Entity-Component architecture
   - Game loop à 60 FPS
   - Scene Manager
   - Vector2 et utilitaires

2. **prompt_pygame_02_physique_mouvement.txt**
   - Moteur physique custom (pas de lib externe)
   - PhysicsComponent et TransformComponent
   - Contrôles clavier Pygame
   - Rotation et inertie

3. **prompt_pygame_03_command_pattern.txt**
   - Command Pattern avec typing.Protocol
   - InputHandler intégré avec pygame.key
   - Configuration touches flexible
   - Préparation replay et IA

4. **prompt_pygame_04_factory_terrains.txt**
   - Factory Pattern pour terrains
   - Grille 2D de tuiles
   - Rendu avec pygame.draw ou sprites
   - Chargement maps JSON
   - Intégration physique (vitesse, grip)

5. **prompt_pygame_05_state_pattern.txt**
   - State Pattern avec typing.Protocol
   - États : RIDING, CARRYING, REMOUNTING, CRASHED
   - Système d'animation frame-by-frame
   - Transitions et effets visuels

### 📝 Prompts Concis (6-11)

6. **prompt_pygame_06_endurance_equilibre.txt**
   - Jauges avec pygame.draw
   - Calculs dynamiques
   - Zones de performance

7. **prompt_pygame_07_obstacles_factory.txt**
   - Factory pour obstacles
   - Collisions pygame.Rect
   - Mécaniques saut/portage

8. **prompt_pygame_08_composite_circuits.txt**
   - Composite Pattern
   - Track Builder
   - Sérialisation JSON

9. **prompt_pygame_09_strategy_ia.txt**
   - Strategy Pattern
   - Pathfinding simple
   - IA utilisant Commands

10. **prompt_pygame_10_course_scoring.txt**
    - RaceManager
    - Chronométrage précis
    - Classement et stats

11. **prompt_pygame_11_ui_feedback.txt**
    - HUD complet
    - Particules custom
    - Menus et effets

## 🎨 Design Patterns Utilisés

1. **Entity-Component** (Prompt 1) - Architecture modulaire
2. **Command Pattern** (Prompt 3) - Gestion inputs
3. **Factory Pattern** (Prompts 4, 7) - Création objets
4. **State Pattern** (Prompt 5) - États cycliste
5. **Strategy Pattern** (Prompt 9) - Comportements IA
6. **Composite Pattern** (Prompt 8) - Construction circuits
7. **Observer Pattern** (Prompt 10) - Événements

## 🚀 Installation et Setup

### Première installation (déjà fait)

```bash
# Créer environnement virtuel
python -m venv venv

# Activer (Windows)
venv\Scripts\activate

# Activer (Linux/Mac)
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Lancer le jeu

```bash
# Avec l'environnement virtuel activé
python main.py

# Ou directement avec le Python du venv
venv\Scripts\python.exe main.py  # Windows
venv/bin/python main.py          # Linux/Mac
```

### Commandes en jeu

- **Flèches** ou **WASD** : Déplacer le rectangle
- **ESPACE** : Afficher la position du joueur
- **P** : Pause
- **F3** : Toggle debug info
- **F11** : Toggle fullscreen
- **ECHAP** : Quitter le jeu

## 📁 Structure Recommandée

```
cyclo-cross-pygame/
├── main.py
├── requirements.txt
├── config/
│   ├── game_config.py
│   └── constants.py
├── entities/
│   ├── entity.py
│   └── cyclist.py
├── components/
│   ├── physics_component.py
│   ├── transform_component.py
│   ├── stamina_component.py
│   └── ...
├── patterns/
│   ├── commands/
│   ├── strategies/
│   ├── states/
│   └── factories/
├── systems/
│   ├── race_manager.py
│   ├── terrain_manager.py
│   └── ...
├── scenes/
│   ├── menu_scene.py
│   ├── race_scene.py
│   └── results_scene.py
├── utils/
│   ├── vector2.py
│   └── helpers.py
└── assets/
    ├── sprites/
    ├── fonts/
    └── sounds/
```

## 🔑 Différences Clés Pygame vs Phaser

| Aspect | Pygame | Phaser |
|--------|--------|--------|
| **Physique** | Custom (manuel) | Arcade Physics intégré |
| **Animations** | Frame-by-frame manuel | Système intégré |
| **Tilemaps** | Grille 2D custom | Tilemap + Tiled |
| **Collisions** | pygame.Rect manual | Intégré avec groupes |
| **Événements** | pygame.event custom | EventEmitter |
| **UI** | pygame.draw manuel | GameObjects variés |

## 💡 Avantages Pygame

✅ **Pédagogique** : Comprendre les mécaniques bas niveau
✅ **Contrôle total** : Pas de "magie" du framework
✅ **Python** : Syntaxe claire, type hints
✅ **Léger** : Dépendances minimales
✅ **Portable** : Windows, Mac, Linux facilement

## 📖 Ordre d'Implémentation

Suivre l'ordre strict des prompts 1 → 11 :

1. ✅ **Architecture et setup** - COMPLÉTÉ
   - Environnement virtuel Python configuré
   - Pygame installé (version 2.6.1)
   - Structure de projet complète
   - Architecture Entity-Component fonctionnelle
   - Entity Manager et Scene Manager implémentés
   - Classe Vector2 complète
   - Game Loop à 60 FPS
   - Scène de test avec rectangle contrôlable

2. ✅ **Physique custom** - COMPLÉTÉ
   - PhysicsComponent avec forces, vélocité, accélération
   - TransformComponent pour position/rotation/scale
   - InputComponent pour contrôles clavier
   - Intégration d'Euler pour simulation physique
   - Rayon de braquage réaliste selon vitesse
   - Inertie et drag configurables
   - Classe Cyclist complète
   - SpriteRendererComponent avec rotation
   - PhysicsTestScene démonstration
   - Documentation PHYSICS_SYSTEM.md

3. ✅ **Command Pattern** - COMPLÉTÉ
   - Interface ICommand avec typing.Protocol
   - 7 commandes concrètes (Accelerate, Brake, Turn, Sprint, Stop, Reverse)
   - CommandInputHandler pour mapping touches->commandes
   - Configuration des touches dans input_config.py
   - 3 profils de contrôle (arrows, wasd, hybrid)
   - CommandInputComponent remplaçant InputComponent
   - Système de priorités pour résoudre les conflits
   - Changement de profil à chaud
   - CommandTestScene démonstration
   - Documentation COMMAND_PATTERN.md
   - Architecture prête pour IA et replay

4. ⏭️ Terrains avec Factory
5. ⏭️ State Pattern
6. ⏭️ Jauges
7. ⏭️ Obstacles
8. ⏭️ Circuits
9. ⏭️ IA
10. ⏭️ Course et scoring
11. ⏭️ UI et polish

## 🎓 Objectifs Pédagogiques

Ce projet démontre :
- ✅ Architecture logicielle professionnelle
- ✅ Design patterns en Python
- ✅ Type hints et typing.Protocol
- ✅ Implémentation moteur physique
- ✅ Gestion d'état et événements
- ✅ Code maintenable et extensible
- ✅ Principes SOLID en pratique

## 🧪 Qualité de Code

**Standards requis :**
- Type hints complets (mypy --strict)
- Style PEP 8 (black, flake8)
- Docstrings pour classes publiques
- Commentaires en français
- Tests unitaires recommandés

## 📚 Ressources

- [Documentation Pygame](https://www.pygame.org/docs/)
- [Tutoriels Pygame](https://www.pygame.org/wiki/tutorials)
- [Type hints Python](https://docs.python.org/3/library/typing.html)
- [Design Patterns Python](https://refactoring.guru/design-patterns/python)

## 🎮 Résultat Final

À la fin des 11 prompts :
- ✅ Jeu de cyclo-cross jouable
- ✅ Architecture exemplaire
- ✅ Design patterns bien appliqués
- ✅ Type hints stricts partout
- ✅ IA fonctionnelle
- ✅ Système de course complet
- ✅ UI polie
- ✅ Code extensible

## 💬 Comparaison Phaser vs Pygame

**Phaser recommandé si :**
- Déploiement web prioritaire
- Besoin de rapidité de développement
- Préférence pour TypeScript/JavaScript

**Pygame recommandé si :**
- Apprentissage des mécaniques bas niveau
- Préférence pour Python
- Contrôle total souhaité
- Distribution desktop

## ✨ Points Forts de cette Approche

1. **Pas de réinvention** : Les design patterns sont identiques entre Pygame et Phaser
2. **Transférable** : Les concepts s'appliquent à n'importe quel framework
3. **Compréhension** : Implémenter soi-même renforce l'apprentissage
4. **Portfolio** : Code Python professionnel avec type hints
5. **Évolutif** : Architecture permet ajout facile de features

Bon développement ! 🚴‍♂️🐍


# Idée
Sable |-------|-x-|------|
      |----------|-x-|---|
      |--|-x-|-----------|
      Suivre l'ornière