# Command Pattern - Système d'Input

## Vue d'ensemble

Le système d'input du jeu CycloCross utilise le **Command Pattern** pour découpler complètement les entrées clavier de la logique métier. Cette architecture permet une grande flexibilité et facilite l'extension, le testing, et la réutilisation du code.

## Pourquoi le Command Pattern ?

### Alternative : Switch/Case traditionnel

```typescript
// ❌ Approche traditionnelle (couplée et rigide)
update() {
  if (this.keys.up.isDown) {
    this.applyAcceleration();
  }
  if (this.keys.down.isDown) {
    this.applyBraking();
  }
  if (this.keys.left.isDown) {
    this.applyLeftTurn();
  }
  // ... problèmes : couplage fort, difficile à tester, pas réutilisable
}
```

### Problèmes de l'approche traditionnelle

1. **Couplage fort** : Le code d'input connaît directement les touches et la logique métier
2. **Difficile à tester** : Impossible de tester les actions sans simuler des touches
3. **Pas extensible** : Ajouter une action nécessite de modifier le code existant
4. **Pas réutilisable** : L'IA ne peut pas utiliser le même système
5. **Pas de replay** : Impossible d'enregistrer/rejouer les actions

### Avantages du Command Pattern

✅ **Découplage total** : Les touches, les actions et la logique sont séparées
✅ **Testabilité** : Chaque commande peut être testée indépendamment
✅ **Extensibilité** : Nouvelles commandes sans modifier le code existant (Open/Closed Principle)
✅ **Réutilisabilité** : L'IA peut utiliser les mêmes commandes
✅ **Replay** : Enregistrement et rejeu de séquences de commandes
✅ **Remapping facile** : Changer les touches dans un fichier de config

## Architecture du système

### 1. L'interface IGameCommand

```typescript
// src/types/IGameCommand.ts
export interface IGameCommand {
  execute(entity: Cyclist, deltaTime: number): void;
  undo?(entity: Cyclist, deltaTime: number): void;
  readonly name?: string;
  readonly priority?: number;
}
```

Tous les objets "Commande" implémentent cette interface. Chaque commande encapsule une action du jeu.

### 2. Les commandes concrètes

Chaque action du jeu est une classe séparée :

- **AccelerateCommand** : Applique une force d'accélération
- **BrakeCommand** : Applique une force de freinage
- **TurnLeftCommand** : Tourne vers la gauche
- **TurnRightCommand** : Tourne vers la droite
- **SprintCommand** : Active/désactive le sprint
- **NullCommand** : Commande vide (Null Object Pattern)

### 3. Le système de Key Bindings

```typescript
// src/config/keyBindings.ts
export enum GameAction {
  ACCELERATE = 'ACCELERATE',
  BRAKE = 'BRAKE',
  TURN_LEFT = 'TURN_LEFT',
  TURN_RIGHT = 'TURN_RIGHT',
  SPRINT = 'SPRINT',
}

export type KeyBindingScheme = {
  [key in GameAction]: number[];
};
```

Les touches sont mappées aux **actions** (pas directement aux commandes), ce qui permet plusieurs touches pour une même action.

### 4. L'InputHandler

```typescript
// src/systems/InputHandler.ts
export class InputHandler {
  private keys: Map<number, Phaser.Input.Keyboard.Key>;
  private commandMap: Map<GameAction, IGameCommand>;
  private keyBindings: KeyBindingScheme;

  public getActiveCommands(): IGameCommand[] {
    // Parcourt les actions actives et retourne les commandes correspondantes
  }
}
```

L'InputHandler est responsable de :
- Enregistrer les touches auprès de Phaser
- Mapper les actions aux commandes
- Retourner les commandes actives chaque frame

### 5. InputComponentNew

```typescript
// src/components/InputComponentNew.ts
export class InputComponentNew extends BaseComponent {
  update(_time: number, delta: number): void {
    // Récupère les commandes actives
    this.commandsToExecute = this.inputHandler.getActiveCommands();

    // Trie par priorité
    this.commandsToExecute.sort((a, b) =>
      (b.priority ?? 0) - (a.priority ?? 0)
    );

    // Exécute toutes les commandes
    this.commandsToExecute.forEach(command => {
      command.execute(this.cyclist, delta);
    });
  }
}
```

Le composant ne connaît ni les touches, ni les actions. Il récupère simplement des commandes et les exécute.

## Comment ajouter une nouvelle commande

### Étape 1 : Créer la commande

```typescript
// src/patterns/commands/JumpCommand.ts
import type { IGameCommand } from '../../types/IGameCommand';
import type { Cyclist } from '@entities/Cyclist';

export class JumpCommand implements IGameCommand {
  public readonly name = 'Jump';
  public readonly priority = 15;

  execute(entity: Cyclist, _deltaTime: number): void {
    // Logique de saut
    const body = entity.getBody();
    body.setVelocityY(-300); // Impulsion verticale
    console.log('[JumpCommand] Saut exécuté');
  }

  undo(entity: Cyclist, _deltaTime: number): void {
    // Optionnel : annuler le saut
  }
}
```

### Étape 2 : Ajouter l'action dans keyBindings.ts

```typescript
// src/config/keyBindings.ts
export enum GameAction {
  // ... actions existantes
  JUMP = 'JUMP', // ✅ Déjà présent
}

// Assigner une touche dans le schéma
export const DEFAULT_KEY_BINDINGS: KeyBindingScheme = {
  // ... autres bindings
  [GameAction.JUMP]: [Phaser.Input.Keyboard.KeyCodes.SPACE],
};
```

### Étape 3 : Enregistrer la commande dans InputHandler

```typescript
// src/systems/InputHandler.ts
private initializeCommands(): void {
  // ... commandes existantes
  this.commandMap.set(GameAction.JUMP, new JumpCommand()); // ✅ Ajouter ici
}
```

### Étape 4 : Exporter la commande

```typescript
// src/patterns/commands/index.ts
export { JumpCommand } from './JumpCommand'; // ✅ Exporter
```

**C'est tout !** Aucune modification du reste du code n'est nécessaire. ✅

## Comment remapper les touches

### Option 1 : Changer le schéma par défaut

```typescript
// src/config/keyBindings.ts
export let ACTIVE_KEY_BINDINGS: KeyBindingScheme = WASD_KEY_BINDINGS; // ✅ Changer ici
```

### Option 2 : Changer dynamiquement dans le jeu

```typescript
// Dans RaceScene ou un menu de paramètres
import { WASD_KEY_BINDINGS } from '@config/keyBindings';

// Changer le schéma de l'InputHandler
this.inputHandler.setKeyBindings(WASD_KEY_BINDINGS);
```

### Option 3 : Créer un schéma personnalisé

```typescript
// src/config/keyBindings.ts
export const CUSTOM_KEY_BINDINGS: KeyBindingScheme = {
  [GameAction.ACCELERATE]: [Phaser.Input.Keyboard.KeyCodes.E],
  [GameAction.BRAKE]: [Phaser.Input.Keyboard.KeyCodes.D],
  [GameAction.TURN_LEFT]: [Phaser.Input.Keyboard.KeyCodes.S],
  [GameAction.TURN_RIGHT]: [Phaser.Input.Keyboard.KeyCodes.F],
  [GameAction.SPRINT]: [Phaser.Input.Keyboard.KeyCodes.W],
  [GameAction.JUMP]: [Phaser.Input.Keyboard.KeyCodes.SPACE],
  [GameAction.DISMOUNT]: [Phaser.Input.Keyboard.KeyCodes.R],
};
```

## Testabilité

### Tester une commande individuellement

```typescript
// tests/commands/AccelerateCommand.test.ts
import { AccelerateCommand } from '@patterns/commands';
import { Cyclist } from '@entities/Cyclist';

describe('AccelerateCommand', () => {
  it('devrait appliquer une accélération', () => {
    const cyclist = createMockCyclist();
    const command = new AccelerateCommand();

    command.execute(cyclist, 16); // Simuler 1 frame à 60fps

    const body = cyclist.getBody();
    expect(body.acceleration.x).toBeGreaterThan(0);
  });
});
```

### Tester l'InputHandler sans touches réelles

```typescript
// tests/systems/InputHandler.test.ts
it('devrait retourner AccelerateCommand quand UP est pressée', () => {
  const inputHandler = new InputHandler(scene);

  // Simuler la touche UP pressée (via mock)
  simulateKeyPress(Phaser.Input.Keyboard.KeyCodes.UP);

  const commands = inputHandler.getActiveCommands();
  expect(commands).toContainInstanceOf(AccelerateCommand);
});
```

### Tester avec des commandes mock

```typescript
// tests/components/InputComponentNew.test.ts
it('devrait exécuter les commandes dans l\'ordre de priorité', () => {
  const mockCommands = [
    { name: 'Low', priority: 5, execute: jest.fn() },
    { name: 'High', priority: 20, execute: jest.fn() },
  ];

  // Injecter les commandes mock
  const inputHandler = createMockInputHandler(mockCommands);
  const component = new InputComponentNew(cyclist, inputHandler);

  component.update(0, 16);

  // Vérifier l'ordre d'exécution
  expect(mockCommands[1].execute).toHaveBeenCalledBefore(mockCommands[0].execute);
});
```

## Utilisation pour l'IA

L'IA peut utiliser exactement les mêmes commandes que le joueur :

```typescript
// src/ai/CyclistAI.ts
export class CyclistAI {
  private cyclist: Cyclist;
  private commands: IGameCommand[];

  constructor(cyclist: Cyclist) {
    this.cyclist = cyclist;
    this.commands = [
      new AccelerateCommand(),
      new TurnLeftCommand(),
      new TurnRightCommand(),
    ];
  }

  update(time: number, delta: number): void {
    // L'IA décide quelle commande exécuter
    const decision = this.makeDecision();

    // Exécute la commande choisie
    decision.execute(this.cyclist, delta);
  }

  private makeDecision(): IGameCommand {
    // Logique de décision de l'IA
    // Par exemple : éviter les obstacles, suivre la trajectoire optimale

    if (this.shouldTurnLeft()) {
      return this.commands[1]; // TurnLeftCommand
    }

    return this.commands[0]; // AccelerateCommand par défaut
  }
}
```

**Avantages pour l'IA :**
- Même physique que le joueur (équitable)
- Réutilisation du code existant
- Testabilité de l'IA indépendamment du reste
- Possibilité d'enregistrer les décisions de l'IA

## Système de Replay

Le Command Pattern permet facilement d'enregistrer et rejouer les actions :

```typescript
// src/systems/ReplayRecorder.ts
export class ReplayRecorder {
  private recordedCommands: Array<{
    time: number;
    command: IGameCommand;
  }> = [];

  // Enregistrer une commande
  record(time: number, command: IGameCommand): void {
    this.recordedCommands.push({ time, command });
  }

  // Rejouer les commandes enregistrées
  replay(cyclist: Cyclist, currentTime: number, delta: number): void {
    const commandsToReplay = this.recordedCommands.filter(
      record => record.time === currentTime
    );

    commandsToReplay.forEach(record => {
      record.command.execute(cyclist, delta);
    });
  }

  // Sauvegarder dans un fichier JSON
  exportToJson(): string {
    return JSON.stringify(this.recordedCommands.map(r => ({
      time: r.time,
      commandName: r.command.name,
    })));
  }
}
```

**Cas d'usage du replay :**
- Mode spectateur
- Partage de parties
- Débogage (reproduire un bug)
- Mode "ghost" (course contre son meilleur temps)

## Système de priorité des commandes

Certaines commandes sont plus prioritaires que d'autres :

```typescript
// Priorités définies dans les commandes
SprintCommand.priority = 20    // Très prioritaire
AccelerateCommand.priority = 10 // Priorité moyenne
BrakeCommand.priority = 10      // Priorité moyenne
TurnLeftCommand.priority = 5    // Faible priorité
```

**Exemple :** Si le joueur appuie simultanément sur Sprint + Accélération, le sprint est traité en premier.

## Système Undo/Redo (futur)

Le Command Pattern supporte nativement l'annulation :

```typescript
// src/systems/CommandHistory.ts
export class CommandHistory {
  private history: IGameCommand[] = [];
  private currentIndex: number = -1;

  execute(command: IGameCommand, entity: Cyclist, delta: number): void {
    command.execute(entity, delta);
    this.history.push(command);
    this.currentIndex++;
  }

  undo(entity: Cyclist, delta: number): void {
    if (this.currentIndex >= 0) {
      const command = this.history[this.currentIndex];
      command.undo?.(entity, delta);
      this.currentIndex--;
    }
  }

  redo(entity: Cyclist, delta: number): void {
    if (this.currentIndex < this.history.length - 1) {
      this.currentIndex++;
      const command = this.history[this.currentIndex];
      command.execute(entity, delta);
    }
  }
}
```

## Commandes composites (futur)

On peut combiner plusieurs commandes en une seule :

```typescript
// src/patterns/commands/DriftCommand.ts
export class DriftCommand implements IGameCommand {
  public readonly name = 'Drift';

  private brakeCommand = new BrakeCommand();
  private turnCommand: IGameCommand;

  constructor(direction: 'left' | 'right') {
    this.turnCommand = direction === 'left'
      ? new TurnLeftCommand()
      : new TurnRightCommand();
  }

  execute(entity: Cyclist, deltaTime: number): void {
    // Exécute freinage + virage = dérapage
    this.brakeCommand.execute(entity, deltaTime);
    this.turnCommand.execute(entity, deltaTime);
  }
}
```

## Résumé

Le Command Pattern apporte de nombreux avantages au système d'input :

| Critère | Sans Pattern | Avec Command Pattern |
|---------|-------------|----------------------|
| **Couplage** | Fort (touches ↔ logique) | Faible (découplé) |
| **Testabilité** | Difficile | Facile (tests unitaires) |
| **Extensibilité** | Modification du code existant | Ajouter nouvelle classe |
| **Réutilisabilité** | Non (code spécifique joueur) | Oui (IA, replay, etc.) |
| **Remapping** | Code hardcodé | Fichier de config |
| **Undo/Redo** | Impossible | Natif |
| **Replay** | Impossible | Facile |

**Conclusion :** Le Command Pattern est un investissement initial plus important, mais qui devient rapidement rentable dès qu'on ajoute des fonctionnalités avancées (IA, replay, tests, etc.).

## Références

- [Game Programming Patterns - Command Pattern](https://gameprogrammingpatterns.com/command.html)
- [Refactoring Guru - Command Pattern](https://refactoring.guru/design-patterns/command)
- Documentation Phaser 3 : [Input System](https://photonstorm.github.io/phaser3-docs/Phaser.Input.html)
