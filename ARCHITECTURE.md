# Architecture du Jeu de Cyclo-Cross

## Vue d'ensemble

Ce document décrit l'architecture du jeu de cyclo-cross développé avec Pygame. L'architecture repose sur des principes solides de conception orientée objet et utilise plusieurs design patterns reconnus.

## Principes architecturaux

### 1. Séparation des responsabilités (SRP - Single Responsibility Principle)

Chaque classe a une responsabilité unique et bien définie :
- `Entity` : Gère la position, rotation, scale et les composants d'une entité
- `IComponent` : Définit le contrat pour les composants
- `EntityManager` : Gère le cycle de vie de toutes les entités
- `SceneManager` : Gère les transitions entre scènes
- `Game` : Orchestre le game loop principal

### 2. Open/Closed Principle

Le système est ouvert à l'extension mais fermé à la modification. Pour ajouter un nouveau comportement :
- Créer un nouveau composant héritant de `IComponent`
- Créer une nouvelle scène héritant de `Scene`
- Aucune modification du code existant n'est nécessaire

### 3. Composition sur héritage

L'architecture Entity-Component favorise la composition :
- Une entité peut avoir n'importe quelle combinaison de composants
- Les comportements sont ajoutés dynamiquement
- Évite les problèmes d'héritage multiple et de hiérarchies complexes

## Structure du projet

```
CXPygame/
├── main.py                     # Point d'entrée avec Game Loop
├── config/
│   ├── game_config.py          # Configuration du jeu
│   └── constants.py            # Constantes globales
├── entities/
│   └── entity.py               # Classe Entity de base
├── components/
│   ├── icomponent.py           # Interface IComponent
│   ├── renderer_component.py  # Composant de rendu
│   └── movement_component.py  # Composant de mouvement
├── systems/
│   ├── entity_manager.py      # Gestionnaire d'entités
│   └── scene_manager.py       # Gestionnaire de scènes
├── scenes/
│   ├── scene.py               # Classe Scene de base
│   └── test_scene.py          # Scène de test
├── patterns/
│   ├── commands/              # Command Pattern (futurs prompts)
│   ├── strategies/            # Strategy Pattern (futurs prompts)
│   ├── states/                # State Pattern (futurs prompts)
│   └── factories/             # Factory Pattern (futurs prompts)
├── utils/
│   └── vector2.py             # Classe Vector2 pour calculs 2D
└── assets/
    ├── sprites/               # Images et sprites
    ├── fonts/                 # Polices de caractères
    └── sounds/                # Fichiers audio
```

## Composants principaux

### 1. Game Loop (main.py)

Le game loop suit le pattern classique :

```python
while running:
    delta_time = clock.tick(FPS) / 1000.0
    handle_events()    # Gestion des événements
    update(delta_time) # Mise à jour de la logique
    render()           # Rendu à l'écran
```

**Points clés :**
- FPS fixé à 60 via `pygame.time.Clock()`
- Delta time en secondes pour mouvements indépendants du framerate
- Double buffering avec `pygame.display.flip()`
- Gestion de la pause et du fullscreen

### 2. Architecture Entity-Component

#### Entity (entities/entity.py)

Une entité est un conteneur d'identité avec :
- ID unique (UUID)
- Position, rotation, scale (Vector2)
- Collection de composants
- Tags pour regroupement logique
- État actif/inactif

**Exemple d'utilisation :**
```python
player = Entity("Player")
player.position = Vector2(100, 100)
player.add_component(RendererComponent, 50, 50, Colors.CYAN)
player.add_component(MovementComponent, 200.0)
```

#### IComponent (components/icomponent.py)

Interface définissant le contrat pour tous les composants :
- `init()` : Initialisation après attachement
- `update(delta_time)` : Mise à jour logique
- `destroy()` : Nettoyage des ressources
- Référence au propriétaire (owner)
- État enabled/disabled

**Avantages :**
- Type hints stricts pour la sécurité du typage
- Cycle de vie clair et prévisible
- Séparation logique/rendu

### 3. Entity Manager (systems/entity_manager.py)

Registre central implémentant le pattern Singleton :
- Gestion du cycle de vie de toutes les entités
- Indexation par ID, type, tag, composant
- Mise à jour automatique de toutes les entités
- Destruction différée (évite les problèmes d'itération)

**Méthodes principales :**
```python
add_entity(entity)                        # Ajoute une entité
get_entities_by_type(EntityType)          # Recherche par type
get_entities_by_tag("player")             # Recherche par tag
get_entities_with_component(Renderer)     # Recherche par composant
update(delta_time)                        # Met à jour toutes les entités
```

### 4. Scene Manager (systems/scene_manager.py)

Gère les différentes scènes du jeu (pattern Singleton) :
- Enregistrement des scènes
- Transitions entre scènes
- Transmission de données entre scènes
- Gestion du cycle de vie (enter/exit)

**Flux de transition :**
```python
# Dans une scène
self.set_next_scene("menu", {"score": 1000})

# Le Scene Manager détecte la transition
# et appelle automatiquement :
current_scene.exit()
new_scene.enter(data)
```

### 5. Scene (scenes/scene.py)

Classe abstraite pour toutes les scènes :
- `enter(data)` : Initialisation de la scène
- `exit()` : Nettoyage de la scène
- `handle_events(events)` : Gestion des événements
- `update(delta_time)` : Logique métier
- `render(screen)` : Rendu visuel

Chaque scène a son propre Entity Manager.

### 6. Vector2 (utils/vector2.py)

Classe utilitaire pour calculs vectoriels 2D :

**Opérations :**
- Arithmétique : `+`, `-`, `*`, `/`
- Longueur : `length()`, `length_squared()`
- Normalisation : `normalize()`
- Distance : `distance_to(other)`
- Rotation : `rotate(angle)`
- Interpolation : `lerp(other, t)`
- Produits : `dot(other)`, `cross(other)`

**Méthodes statiques :**
```python
Vector2.zero()   # (0, 0)
Vector2.one()    # (1, 1)
Vector2.up()     # (0, -1)
Vector2.down()   # (0, 1)
Vector2.left()   # (-1, 0)
Vector2.right()  # (1, 0)
```

## Design Patterns utilisés

### 1. Entity-Component Pattern

**Problème résolu :** Éviter les hiérarchies d'héritage complexes.

**Solution :** Composition de comportements via des composants attachables.

**Exemple :**
```python
# Au lieu de : class Player(MovableEntity, RenderableEntity)
# On fait :
player = Entity("Player")
player.add_component(MovementComponent)
player.add_component(RendererComponent)
```

### 2. Singleton Pattern

**Utilisé pour :** EntityManager, SceneManager

**Justification :** Un seul gestionnaire global doit exister.

**Implémentation :**
```python
class EntityManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### 3. Observer Pattern (implicite)

Le système d'événements Pygame est une forme d'Observer Pattern :
- Les événements sont émis par Pygame
- Les scènes observent et réagissent aux événements

### 4. Template Method Pattern

La classe abstraite `Scene` définit le squelette :
```python
class Scene(ABC):
    @abstractmethod
    def enter(self, data): pass

    @abstractmethod
    def update(self, delta_time): pass

    # etc.
```

Les sous-classes implémentent les détails spécifiques.

## Configuration et constantes

### GameConfig (config/game_config.py)

Configuration centralisée avec dataclass :
- Dimensions de la fenêtre
- FPS cible
- Vitesses par défaut
- Paramètres de debug

**Avantage :** Modification facile sans toucher au code.

### Constants (config/constants.py)

Constantes immuables :
- Énumérations (GameState, SceneType)
- Couleurs (Colors)
- Touches (InputKeys)
- Layers de rendu (RenderLayer)

## Flux de données

```
main.py (Game Loop)
    │
    ├──> handle_events()
    │       └──> SceneManager.handle_events()
    │               └──> CurrentScene.handle_events()
    │
    ├──> update(delta_time)
    │       └──> SceneManager.update()
    │               └──> CurrentScene.update()
    │                       └──> EntityManager.update()
    │                               └──> Entity.update()
    │                                       └──> Component.update()
    │
    └──> render()
            └──> SceneManager.render()
                    └──> CurrentScene.render()
                            └──> Component.render()
```

## Gestion de la performance

### 1. Delta Time

Tous les mouvements utilisent le delta time :
```python
position += velocity * delta_time
```

Garantit des mouvements fluides indépendants du framerate.

### 2. Limitation du Delta Time

```python
delta_time = min(delta_time, DELTA_TIME_MAX)
```

Évite les gros sauts en cas de lag.

### 3. Indexation des entités

L'Entity Manager maintient plusieurs index :
- Par ID : O(1) lookup
- Par type : O(1) lookup
- Par tag : O(1) lookup
- Par composant : O(n) mais rapide

### 4. Destruction différée

Les entités ne sont pas détruites immédiatement mais marquées pour destruction, évitant les problèmes d'itération.

## Extensibilité

L'architecture est conçue pour être facilement extensible :

### Ajouter un nouveau composant

1. Créer une classe héritant de `IComponent`
2. Implémenter `init()`, `update()`, `destroy()`
3. L'attacher à une entité

```python
class StaminaComponent(IComponent):
    def init(self): self.stamina = 100
    def update(self, dt): self.stamina -= dt * 5
    def destroy(self): pass
```

### Ajouter une nouvelle scène

1. Créer une classe héritant de `Scene`
2. Implémenter les méthodes abstraites
3. L'enregistrer dans le SceneManager

```python
class MenuScene(Scene):
    def enter(self, data): ...
    def update(self, dt): ...
    # etc.
```

### Ajouter un nouveau système

Créer un nouveau manager dans `systems/` si nécessaire.

## Type Hints et sécurité du typage

Tout le code utilise des type hints Python :
```python
def add_component(self, component_class: Type[T], *args, **kwargs) -> T:
```

**Avantages :**
- Auto-complétion dans l'IDE
- Détection d'erreurs avant l'exécution
- Documentation implicite
- Meilleure maintenabilité

## Tests et validation

Pour tester l'architecture :

1. Lancer le jeu : `python main.py`
2. Vérifier que la fenêtre s'ouvre
3. Vérifier les FPS (doivent être ~60)
4. Tester les contrôles (flèches ou WASD)
5. Tester les touches de debug (F3, P, F11, ESC)

**Scène de test :**
- Rectangle cyan contrôlable
- 3 obstacles statiques
- Instructions à l'écran
- Debug info (FPS, entités)

## Prochaines étapes (futurs prompts)

L'architecture est prête pour :
1. Ajout de sprites et animations
2. Système de physique (collisions, gravité)
3. IA des adversaires (Strategy Pattern)
4. Gestion du terrain (mud, sand, obstacles)
5. Système de stamina et balance
6. Menu et interface utilisateur
7. Sauvegarde et chargement
8. Sons et musique
9. Effets de particules
10. Mode multijoueur

## Références

- **Pygame Documentation** : https://www.pygame.org/docs/
- **Game Programming Patterns** : Robert Nystrom
- **SOLID Principles** : Robert C. Martin
- **Entity-Component-System** : https://en.wikipedia.org/wiki/Entity_component_system

## Conclusion

Cette architecture fournit une base solide et extensible pour le développement du jeu de cyclo-cross. Elle respecte les principes SOLID, utilise des design patterns éprouvés, et facilite l'ajout de nouvelles fonctionnalités sans modifier le code existant.

Le code est entièrement typé, documenté, et structuré de manière professionnelle, permettant une maintenance aisée et une collaboration efficace.
