# Command Pattern - Documentation

## Vue d'ensemble

Le Command Pattern transforme des requêtes (actions) en objets, permettant de paramétrer les clients avec différentes requêtes, de mettre en file d'attente ou de logger les requêtes, et de supporter des opérations annulables.

## Problème résolu

**Avant** : Les inputs étaient directement couplés à la logique métier dans InputComponent :
```python
if keys[pygame.K_UP]:
    physics.apply_force(forward * force)  # Couplage fort
```

**Problèmes** :
- Impossible de changer les touches sans modifier le code
- Difficile de tester les actions indépendamment
- L'IA ne peut pas réutiliser les mêmes actions
- Pas de support pour replay ou undo
- Violation du principe Open/Closed

**Après** : Les actions sont des objets Command indépendants :
```python
command = AccelerateCommand(force=1200.0)
command.execute(entity, delta_time)  # Découplage complet
```

## Architecture

### 1. Interface ICommand (Protocol)

```python
class ICommand(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def priority(self) -> int: ...

    def execute(self, entity: Entity, delta_time: float) -> None: ...

    def can_execute(self, entity: Entity) -> bool: ...
```

**Pourquoi Protocol ?**
- Duck typing statique en Python
- Pas besoin d'héritage explicite
- Vérification de type à la compilation
- Plus flexible que l'héritage classique

### 2. Classe BaseCommand

Implémentation par défaut de ICommand :
```python
class BaseCommand:
    def __init__(self, name: str, priority: int = 0):
        self._name = name
        self._priority = priority

    def execute(self, entity: Entity, delta_time: float) -> None:
        raise NotImplementedError()

    def can_execute(self, entity: Entity) -> bool:
        return True
```

## Commandes implémentées

### AccelerateCommand
**Action** : Accélère vers l'avant
**Priorité** : 10
**Paramètres** : `force` (Newtons)

```python
command = AccelerateCommand(force=1200.0)
command.execute(cyclist, delta_time)
```

**Implémentation** :
- Récupère le vecteur avant depuis TransformComponent
- Applique la force via PhysicsComponent
- Vérifie que les composants existent

### BrakeCommand
**Action** : Freine le véhicule
**Priorité** : 15 (plus haute que l'accélération)
**Paramètres** : `force` (Newtons)

**Implémentation** :
- Calcule la direction opposée à la vélocité
- Applique une force de freinage

### TurnLeftCommand / TurnRightCommand
**Action** : Rotation avec rayon de braquage variable
**Priorité** : 5
**Paramètres** : `turn_speed_slow`, `turn_speed_fast`, `speed_threshold`

**Implémentation** :
- Vitesse de rotation dépend de la vitesse actuelle
- Basse vitesse → rotation rapide (maniable)
- Haute vitesse → rotation lente (réaliste)

### SprintCommand
**Action** : Boost temporaire de vitesse
**Priorité** : 20 (très haute)
**Paramètres** : `boost_multiplier`

**Implémentation** :
- Multiplie la force d'accélération
- TODO: Consommera de la stamina (Prompt 6)

### ReverseCommand
**Action** : Marche arrière
**Priorité** : 12
**Paramètres** : `force` (50% de la force normale)

### StopCommand
**Action** : Arrêt d'urgence
**Priorité** : 50 (la plus haute)

**Implémentation** :
- Appelle `physics.stop()` directement
- Arrête tout mouvement instantanément

## CommandInputHandler

Responsable du mapping touches → commandes.

### Fonctionnalités

**1. Binding de touches maintenues**
```python
handler.bind_key(pygame.K_UP, AccelerateCommand(force=1200.0))
```
Utilise `pygame.key.get_pressed()`

**2. Binding d'événements ponctuels**
```python
handler.bind_event(pygame.K_SPACE, SprintCommand())
```
Utilise `pygame.KEYDOWN` dans la event loop

**3. Gestion des priorités**
Les commandes sont triées par priorité avant exécution :
```python
commands.sort(key=lambda cmd: cmd.priority, reverse=True)
```

**4. Prévention des duplications**
Une touche traitée en KEYDOWN n'est pas retraitée en get_pressed()

### Exemple d'utilisation

```python
handler = CommandInputHandler()

# Configuration
handler.bind_key(pygame.K_UP, AccelerateCommand(force=1200.0))
handler.bind_key(pygame.K_LEFT, TurnLeftCommand())
handler.bind_event(pygame.K_SPACE, SprintCommand())

# Dans la boucle de jeu
events = pygame.event.get()
commands = handler.handle_input(events)

for command in commands:
    if command.can_execute(entity):
        command.execute(entity, delta_time)
```

## Configuration des touches

Fichier `config/input_config.py` centralise tous les mappings.

### Profils disponibles

**1. Arrows** : Flèches directionnelles uniquement
```python
profile = create_arrows_profile()
```

**2. WASD** : Clavier WASD
```python
profile = create_wasd_profile()
```

**3. Hybrid** (par défaut) : Flèches + WASD
```python
profile = create_hybrid_profile()
```

### Structure d'un profil

```python
class InputProfile:
    name: str
    key_bindings: Dict[int, Callable[[], ICommand]]
    event_bindings: Dict[int, Callable[[], ICommand]]
```

**Pourquoi des factories ?**
- Chaque touche doit avoir sa propre instance de commande
- Les commandes peuvent avoir un état interne
- Évite les problèmes de partage d'état

### Création d'un nouveau profil

```python
def create_custom_profile() -> InputProfile:
    profile = InputProfile("Custom")

    profile.key_bindings = {
        pygame.K_i: lambda: AccelerateCommand(force=1500.0),
        pygame.K_k: lambda: BrakeCommand(force=2000.0),
        pygame.K_j: lambda: TurnLeftCommand(),
        pygame.K_l: lambda: TurnRightCommand(),
    }

    profile.event_bindings = {
        pygame.K_SPACE: lambda: SprintCommand(),
    }

    return profile

# Ajouter au dictionnaire des profils
AVAILABLE_PROFILES["custom"] = create_custom_profile
```

## CommandInputComponent

Composant attachable aux entités pour gérer les inputs via commandes.

### Fonctionnalités

**1. Chargement de profil**
```python
input_comp = entity.add_component(CommandInputComponent, profile_name="hybrid")
```

**2. Changement de profil à chaud**
```python
input_comp.load_profile("arrows")
```

**3. Activation/désactivation**
```python
input_comp.disable()  # Pour cutscenes, game over, etc.
input_comp.enable()
```

**4. Transmission d'événements**
```python
# Dans la scène
input_comp.set_events(events)
```

**5. Exécution automatique**
```python
# Dans update()
commands = handler.handle_input(events)
for command in commands:
    if command.can_execute(entity):
        command.execute(entity, delta_time)
```

### Cycle de vie

```
1. init() → Charge le profil de contrôle
2. set_events(events) → Reçoit les événements de la frame
3. update(delta_time) → Traite les inputs et exécute les commandes
4. destroy() → Nettoie les ressources
```

## Avantages du Command Pattern

### 1. Découplage complet
Les inputs ne connaissent pas la logique métier :
- InputHandler → Commandes → Entités
- Chaque couche est indépendante

### 2. Réutilisabilité
Les mêmes commandes peuvent être utilisées par :
- Le joueur (via clavier)
- L'IA (via algorithmes)
- Le replay (via enregistrement)
- Les tests (via scripts)

### 3. Testabilité
Chaque commande est testable indépendamment :
```python
def test_accelerate_command():
    entity = create_test_entity()
    command = AccelerateCommand(force=100.0)

    assert command.can_execute(entity)
    command.execute(entity, 0.016)

    physics = entity.get_component(PhysicsComponent)
    assert physics.get_speed() > 0
```

### 4. Extensibilité (Open/Closed)
Ajout d'une nouvelle commande sans modifier l'existant :
```python
class DismountCommand(BaseCommand):
    def execute(self, entity: Entity, delta_time: float):
        # Logique de descente du vélo
        pass
```

### 5. Flexibilité de configuration
Remapping trivial dans `input_config.py` :
```python
# Passer de flèches à WASD : 2 lignes
input_comp.load_profile("wasd")
```

### 6. Support futur pour replay/undo
Structure prête pour :
```python
class CommandRecorder:
    def record(self, command: ICommand, timestamp: float):
        self._history.append((command, timestamp))

    def replay(self):
        for command, timestamp in self._history:
            command.execute(entity, delta_time)
```

## Différences avec Strategy Pattern

**Command Pattern** :
- Encapsule une **action/requête**
- Focus sur **quoi faire**
- Peut être mis en file d'attente, loggé, annulé
- Exemple : `AccelerateCommand`, `TurnLeftCommand`

**Strategy Pattern** :
- Encapsule un **algorithme complet**
- Focus sur **comment faire**
- Peut être changé à l'exécution
- Exemple : `AggressiveAI`, `DefensiveAI`

Les deux sont complémentaires :
- IA utilise une **Strategy** pour décider quelles **Commands** exécuter
- Commands exécutent les actions décidées par la Strategy

## Utilisation par l'IA (futur Prompt 9)

L'IA pourra utiliser les mêmes commandes :

```python
class AIComponent(IComponent):
    def update(self, delta_time: float):
        # Décide quelle commande exécuter
        if self._should_accelerate():
            command = AccelerateCommand()
            command.execute(self.owner, delta_time)

        if self._should_turn():
            command = TurnLeftCommand()
            command.execute(self.owner, delta_time)
```

**Avantages** :
- Même logique physique pour joueur et IA
- Pas de code dupliqué
- Comportements cohérents

## Macro-commandes (extension future)

Combiner plusieurs commandes :

```python
class MacroCommand(BaseCommand):
    def __init__(self, commands: List[ICommand]):
        super().__init__("Macro", priority=0)
        self._commands = commands

    def execute(self, entity: Entity, delta_time: float):
        for command in self._commands:
            if command.can_execute(entity):
                command.execute(entity, delta_time)

# Exemple : Drift = Accelerate + Turn
drift_left = MacroCommand([
    AccelerateCommand(force=800.0),
    TurnLeftCommand()
])
```

## Validation des critères

### ✅ Ajout de nouvelle commande sans modification
```python
# 1. Créer la commande
class NewCommand(BaseCommand):
    def execute(self, entity, delta_time):
        # Logique
        pass

# 2. L'ajouter dans input_config.py
profile.key_bindings[pygame.K_x] = lambda: NewCommand()
```
**Aucun autre fichier modifié !**

### ✅ Remapping uniquement dans config
Changer les touches = modifier `input_config.py` seulement.

### ✅ Commandes testables indépendamment
Chaque commande est une classe isolée, testable en unit test.

### ✅ Prêt pour replay
Structure permet d'enregistrer et rejouer des commandes.

### ✅ Plusieurs entités, différents handlers
```python
player1.add_component(CommandInputComponent, profile_name="arrows")
player2.add_component(CommandInputComponent, profile_name="wasd")
```

### ✅ Principe Open/Closed respecté
Ouvert à l'extension (nouvelles commandes), fermé à la modification.

### ✅ Type hints stricts partout
`typing.Protocol`, génériques, pas de `Any`.

## Comparaison avant/après

### Avant (InputComponent direct)
```python
def update(self, delta_time: float):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:  # Couplé aux touches
        force = forward * 600.0
        physics.apply_force(force)  # Couplé à la physique
```

**Problèmes** :
- Touches hardcodées
- Logique mélangée
- Difficile à tester
- Impossible pour l'IA de réutiliser

### Après (Command Pattern)
```python
# Configuration (input_config.py)
profile.key_bindings[pygame.K_UP] = lambda: AccelerateCommand(600.0)

# Composant (command_input_component.py)
commands = handler.handle_input(events)
for command in commands:
    command.execute(entity, delta_time)

# Commande (movement_commands.py)
class AccelerateCommand:
    def execute(self, entity, delta_time):
        force = transform.get_forward_vector() * self.force
        physics.apply_force(force)
```

**Avantages** :
- ✅ Découplage complet
- ✅ Configuration externe
- ✅ Facilement testable
- ✅ Réutilisable par l'IA
- ✅ Extensible sans modification

## Scène de démonstration

`CommandTestScene` démontre :
- Utilisation de `CommandInputComponent`
- Changement de profil à chaud (TAB)
- Toggle des contrôles (T)
- Affichage des touches liées
- HUD informatif

**Touches** :
- **TAB** : Cycle entre les profils (arrows → wasd → hybrid)
- **T** : Active/désactive les contrôles
- **R** : Reset position
- **Flèches/WASD** : Contrôle selon profil actif
- **SPACE** : Sprint

## Prochaines étapes

Le Command Pattern est maintenant prêt pour :
- **Prompt 4** : Terrains modifiant la physique via commandes
- **Prompt 5** : États limitant certaines commandes
- **Prompt 6** : Stamina consommée par certaines commandes
- **Prompt 9** : IA utilisant les commandes
- **Replay system** : Enregistrement/lecture de commandes
- **Undo/Redo** : Implémentation de IUndoableCommand

## Références

- **Design Patterns** : Gang of Four (Command Pattern)
- **Game Programming Patterns** : Robert Nystrom (Command chapter)
- **typing.Protocol** : PEP 544
- **Pygame Input** : https://www.pygame.org/docs/ref/key.html
