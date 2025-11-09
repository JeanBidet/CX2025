# Documentation d'Architecture - CycloCross 2025

## Vue d'ensemble

CycloCross 2025 implémente une architecture **Entity-Component** adaptée à Phaser 3, combinant la puissance du moteur de jeu avec une séparation claire des responsabilités selon les principes SOLID.

---

## Principes architecturaux fondamentaux

### 1. Séparation Rendu / Logique Métier

```
┌─────────────────────────────────────────────────────────────┐
│                    COUCHE PHASER                            │
│  (GameObjects, Physics, Rendering, Input, Assets)           │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │           COUCHE LOGIQUE MÉTIER                       │ │
│  │     (Components, Systems, Patterns)                   │ │
│  │                                                       │ │
│  │  • Indépendante de Phaser                            │ │
│  │  • Testable unitairement                             │ │
│  │  • Réutilisable                                      │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Avantages :**
- ✅ Phaser gère ce qu'il fait le mieux (rendu, physique, input)
- ✅ Notre code métier reste indépendant et testable
- ✅ Possibilité de changer de moteur sans tout réécrire
- ✅ Respect du principe de séparation des préoccupations

### 2. Entity-Component Pattern

Au lieu de classes monolithiques héritant de Phaser.Sprite avec toute la logique, nous utilisons :

```typescript
// ❌ ANCIEN : Monolithique
class Cyclist extends Phaser.Sprite {
  stamina = 100;
  balance = 50;

  updateStamina() { /* ... */ }
  updateBalance() { /* ... */ }
  updateAI() { /* ... */ }
  // 500 lignes de code...
}

// ✅ NOUVEAU : Composants modulaires
class Cyclist extends Phaser.Sprite {
  private components: IComponent[] = [];

  addComponent(component: IComponent) {
    this.components.push(component);
  }
}

// Chaque composant = une responsabilité
new Cyclist()
  .addComponent(new StaminaComponent(this))
  .addComponent(new BalanceComponent(this))
  .addComponent(new AIComponent(this));
```

**Avantages :**
- ✅ **Single Responsibility** : chaque composant a une seule raison de changer
- ✅ **Open/Closed** : ajout de comportements sans modifier l'existant
- ✅ **Composition over Inheritance**
- ✅ Réutilisabilité maximale (un composant = plusieurs entités)

---

## Architecture des Composants

### Interface IComponent

Contrat que tous les composants doivent respecter :

```typescript
interface IComponent {
  readonly owner: Phaser.GameObjects.GameObject;

  init(): void;                              // Initialisation
  preUpdate(time: number, delta: number): void;  // Pré-traitement
  update(time: number, delta: number): void;     // Logique principale
  destroy(): void;                           // Nettoyage
}
```

### Classe BaseComponent

Implémentation de base avec comportement par défaut :

```typescript
abstract class BaseComponent implements IComponent {
  constructor(protected owner: Phaser.GameObjects.GameObject) {}

  // Méthodes avec implémentations par défaut
  init(): void {}
  preUpdate(time: number, delta: number): void {}
  destroy(): void {}

  // Méthode abstraite - DOIT être implémentée
  abstract update(time: number, delta: number): void;
}
```

### Cycle de vie d'un composant

```
1. Construction       new MyComponent(owner)
         ↓
2. Ajout à l'entité   entity.addComponent(component)
         ↓
3. Initialisation     component.init()
         ↓
4. Boucle de jeu      ┌─→ component.preUpdate(time, delta)
   (60 FPS)           │   component.update(time, delta)
                      └── (répété chaque frame)
         ↓
5. Destruction        component.destroy()
```

---

## Design Patterns Implémentés

### 1. Command Pattern

**But :** Encapsuler une action comme un objet.

**Utilisation :** Gestion des inputs joueur, système undo/redo.

```typescript
interface ICommand {
  execute(): void;
  undo?(): void;
}

// Exemple : Commande d'accélération
class AccelerateCommand implements ICommand {
  constructor(private cyclist: Cyclist, private amount: number) {}

  execute(): void {
    this.cyclist.velocity += this.amount;
  }

  undo(): void {
    this.cyclist.velocity -= this.amount;
  }
}

// Utilisation
const input = new InputHandler();
input.bindKey('UP', new AccelerateCommand(player, 50));
```

**Avantages :**
- Découple l'invocateur (input) de l'exécutant (cyclist)
- Support undo/redo facilement
- Queue de commandes possible (pour replay, AI, etc.)

---

### 2. State Pattern

**But :** Modifier le comportement d'un objet selon son état interne.

**Utilisation :** États du cycliste (pédalage, sprint, portage, chute).

```typescript
interface IState<TContext> {
  enter(context: TContext): void;
  update(context: TContext, delta: number): void;
  exit(context: TContext): void;
}

// États du cycliste
class RidingState implements IState<Cyclist> {
  enter(cyclist: Cyclist): void {
    cyclist.animation.play('ride');
  }

  update(cyclist: Cyclist, delta: number): void {
    // Logique de pédalage normal
    if (cyclist.stamina < 20) {
      cyclist.changeState(new RecoveringState());
    }
  }

  exit(cyclist: Cyclist): void {
    cyclist.animation.stop();
  }
}

class SprintingState implements IState<Cyclist> {
  // État de sprint avec consommation d'endurance accrue
}
```

**Avantages :**
- Chaque état = une classe (Single Responsibility)
- Transitions d'états explicites
- Facilite l'ajout de nouveaux états

---

### 3. Strategy Pattern

**But :** Définir une famille d'algorithmes interchangeables.

**Utilisation :** IA des adversaires, calculs de terrain.

```typescript
interface IStrategy<TInput, TOutput> {
  execute(input: TInput): TOutput;
}

// Stratégies d'IA
class AggressiveAI implements IStrategy<AIInput, void> {
  execute(input: AIInput): void {
    // Sprinte souvent, prend des risques
  }
}

class DefensiveAI implements IStrategy<AIInput, void> {
  execute(input: AIInput): void {
    // Économise l'endurance, évite les obstacles
  }
}

// Changement de stratégie à la volée
opponent.setAIStrategy(new AggressiveAI());
```

**Avantages :**
- Algorithmes interchangeables à runtime
- Open/Closed : nouveaux algorithmes sans modifier l'existant
- Facilite les tests (mock des stratégies)

---

### 4. Factory Pattern (à venir)

**But :** Créer des objets sans spécifier leur classe exacte.

**Utilisation :** Création d'obstacles, d'adversaires IA, de terrains.

```typescript
// Sera implémenté dans les prompts suivants
interface IEntityFactory {
  create(config: EntityConfig): Phaser.GameObjects.GameObject;
}

class CyclistFactory implements IEntityFactory {
  create(config: CyclistConfig): Cyclist {
    const cyclist = new Cyclist(/* ... */);
    cyclist.addComponent(new StaminaComponent(cyclist));
    cyclist.addComponent(new BalanceComponent(cyclist));
    return cyclist;
  }
}
```

---

## Flux de données et interactions

### 1. Boucle de jeu principale

```
User Input
    ↓
Command Pattern (AccelerateCommand, JumpCommand)
    ↓
Entity (Cyclist)
    ↓
Components (StaminaComponent, BalanceComponent)
    ↓
State Pattern (RidingState, SprintingState)
    ↓
Phaser GameObject Update
    ↓
Rendering (Phaser)
```

### 2. Mise à jour d'une entité avec composants

```typescript
// Dans RaceScene.update()
update(time: number, delta: number): void {
  // Pour chaque entité avec composants
  this.entities.forEach(entity => {
    entity.updateComponents(time, delta);
  });
}

// Dans Entity.updateComponents()
updateComponents(time: number, delta: number): void {
  this.components.forEach(component => {
    if (component.isActive()) {
      component.preUpdate(time, delta);
      component.update(time, delta);
    }
  });
}
```

---

## Principes SOLID appliqués

### S - Single Responsibility Principle

✅ **Chaque composant a une seule responsabilité**
- `StaminaComponent` : gestion de l'endurance uniquement
- `BalanceComponent` : gestion de l'équilibre uniquement
- `AIComponent` : intelligence artificielle uniquement

### O - Open/Closed Principle

✅ **Ouvert à l'extension, fermé à la modification**
- Ajout d'un nouveau composant sans modifier les existants
- Nouveaux états/stratégies sans changer le code de base

```typescript
// Ajout d'un nouveau composant sans toucher au reste
class TurboComponent extends BaseComponent {
  update(time: number, delta: number): void {
    // Nouvelle fonctionnalité
  }
}

cyclist.addComponent(new TurboComponent(cyclist));
```

### L - Liskov Substitution Principle

✅ **Les dérivées peuvent remplacer les classes de base**
- Tout `BaseComponent` peut être remplacé par une sous-classe
- `IState<Cyclist>` : tous les états sont interchangeables

### I - Interface Segregation Principle

✅ **Interfaces spécifiques plutôt qu'une interface générale**
- `IComponent` : contrat de composant
- `ICommand` : contrat de commande
- `IState<T>` : contrat d'état (générique)
- `IStrategy<TIn, TOut>` : contrat de stratégie (générique)

### D - Dependency Inversion Principle

✅ **Dépendre d'abstractions, pas de concrétions**
- Les entités dépendent de `IComponent`, pas de classes concrètes
- Le système d'IA dépend de `IStrategy`, pas d'implémentations

```typescript
// ❌ Mauvais : dépend d'une classe concrète
class Cyclist {
  private ai = new AggressiveAI();  // Couplage fort
}

// ✅ Bon : dépend d'une interface
class Cyclist {
  private ai: IStrategy<AIInput, void>;

  setAI(ai: IStrategy<AIInput, void>) {
    this.ai = ai;  // Injection de dépendance
  }
}
```

---

## Structure de fichiers détaillée

```
src/
├── main.ts                    # Point d'entrée
│
├── config/                    # Configuration
│   ├── gameConfig.ts          # Config Phaser
│   ├── constants.ts           # Constantes globales
│   └── index.ts               # Exports
│
├── scenes/                    # Scènes Phaser
│   └── RaceScene.ts           # Scène de course
│
├── entities/                  # GameObjects avec composants
│   └── DemoSprite.ts          # Exemple d'entité
│
├── components/                # Composants métier
│   ├── BaseComponent.ts       # Classe de base
│   └── RotationComponent.ts   # Exemple de composant
│
├── systems/                   # Systèmes globaux
│   ├── RaceManager.ts         # (À venir)
│   └── TerrainManager.ts      # (À venir)
│
├── patterns/                  # Design patterns
│   ├── commands/              # Pattern Command
│   ├── strategies/            # Pattern Strategy
│   ├── states/                # Pattern State
│   └── factories/             # Pattern Factory
│
├── types/                     # Types TypeScript
│   ├── IComponent.ts          # Interface Component
│   ├── ICommand.ts            # Interface Command
│   ├── IState.ts              # Interface State
│   ├── IStrategy.ts           # Interface Strategy
│   ├── enums.ts               # Énumérations
│   ├── gameData.ts            # Types de données
│   └── index.ts               # Exports centralisés
│
└── utils/                     # Utilitaires
    └── MathUtils.ts           # Fonctions mathématiques
```

---

## Exemple concret : Création d'un cycliste

```typescript
// 1. Créer l'entité Phaser
const cyclist = new Cyclist(scene, x, y);

// 2. Ajouter les composants métier
cyclist.addComponent(new StaminaComponent(cyclist, {
  maxStamina: 100,
  recoveryRate: 10
}));

cyclist.addComponent(new BalanceComponent(cyclist, {
  maxBalance: 80,
  stabilityFactor: 0.5
}));

cyclist.addComponent(new AIComponent(cyclist,
  new AggressiveAI()  // Strategy Pattern
));

// 3. Définir l'état initial
cyclist.changeState(new RidingState());  // State Pattern

// 4. Ajouter à la scène
scene.add.existing(cyclist);

// 5. Le update est géré automatiquement
// RaceScene.update() → cyclist.updateComponents() → chaque component.update()
```

---

## Tests et maintenabilité

### Testabilité des composants

Les composants sont faciles à tester unitairement car ils :
- N'ont qu'une seule responsabilité
- Dépendent d'interfaces, pas de concrétions
- Peuvent être testés sans Phaser (mock du owner)

```typescript
// Test exemple (pseudo-code)
describe('StaminaComponent', () => {
  it('should decrease stamina when sprinting', () => {
    const mockOwner = createMockGameObject();
    const stamina = new StaminaComponent(mockOwner);

    stamina.sprint();
    stamina.update(0, 16); // 1 frame à 60 FPS

    expect(stamina.getValue()).toBeLessThan(100);
  });
});
```

### Extensibilité

Pour ajouter une nouvelle fonctionnalité :
1. Créer un nouveau composant héritant de `BaseComponent`
2. Implémenter la méthode `update()`
3. Ajouter le composant aux entités concernées

**Aucune modification du code existant nécessaire** (Open/Closed Principle).

---

## Conventions de nommage

| Type | Convention | Exemple |
|------|-----------|---------|
| Interface | `I` + PascalCase | `IComponent`, `ICommand` |
| Classe | PascalCase | `BaseComponent`, `Cyclist` |
| Composant | PascalCase + `Component` | `StaminaComponent` |
| État | PascalCase + `State` | `RidingState` |
| Stratégie | PascalCase + suffixe | `AggressiveAI` |
| Fichier | Même nom que l'export principal | `StaminaComponent.ts` |

---

## Prochaines étapes (Prompts suivants)

1. **Système d'input** : Implémentation du Command Pattern pour les contrôles
2. **Physique et mouvement** : Composants de vélocité et collision
3. **Terrain et obstacles** : Factory Pattern pour génération procédurale
4. **Endurance et équilibre** : Composants métier complets
5. **Intelligence Artificielle** : Strategy Pattern pour comportements IA
6. **Interface utilisateur** : HUD avec barre d'endurance, position, temps
7. **Système de caméra** : Suivi fluide du joueur
8. **Audio** : Musique et effets sonores
9. **Particules et effets** : Visuel de boue, poussière, etc.
10. **Menu et résultats** : Scènes additionnelles

---

## Ressources et références

- [Phaser 3 Documentation](https://photonstorm.github.io/phaser3-docs/)
- [Game Programming Patterns](https://gameprogrammingpatterns.com/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Entity Component System](https://en.wikipedia.org/wiki/Entity_component_system)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)

---

**Document créé le 28 octobre 2025**
**Projet CycloCross 2025 - Architecture de base**
