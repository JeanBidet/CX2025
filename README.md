# CycloCross 2025

Jeu de cyclo-cross développé avec **Phaser 3**, **TypeScript** et **Vite**, mettant l'accent sur une architecture propre et des design patterns robustes.

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Contrôles](#-contrôles)
- [Technologies](#-technologies)
- [Installation](#-installation)
- [Scripts disponibles](#-scripts-disponibles)
- [Architecture](#-architecture)
- [Structure du projet](#-structure-du-projet)
- [Design Patterns](#-design-patterns)
- [Conventions de code](#-conventions-de-code)
- [Développement](#-développement)
- [Documentation technique](#-documentation-technique)

---

## 🎯 Vue d'ensemble

**CycloCross 2025** est un jeu de course de cyclo-cross qui simule les défis uniques de ce sport : terrains variés (boue, sable, gravier), obstacles nécessitant portage du vélo, gestion de l'endurance et de l'équilibre.

Le projet démontre l'utilisation professionnelle de :
- **Phaser 3** comme moteur de jeu
- **TypeScript** en mode strict pour la qualité du code
- **Architecture Entity-Component** combinant Phaser et logique métier
- **Design Patterns** (Command, State, Strategy, Factory)
- **Principes SOLID** et séparation des préoccupations

---

## 🎮 Contrôles

### Clavier

| Touche | Action |
|--------|--------|
| **↑** | Accélérer |
| **↓** | Freiner |
| **← →** | Tourner |
| **SHIFT** | Sprint (+50% vitesse) |

### Caractéristiques du Mouvement
- ✅ **Inertie réaliste** : accélération et freinage progressifs
- ✅ **Rotation dépendante de la vitesse** : plus rapide à basse vitesse, plus lente à haute vitesse
- ✅ **Physique Arcade** : 60 FPS stable avec delta time
- ✅ **Sprint** : boost temporaire de vitesse
- ✅ **Caméra fluide** : suit le joueur avec interpolation douce

Pour plus de détails, voir [CONTROLS.md](CONTROLS.md) et [PHYSICS.md](PHYSICS.md).

---

## 🛠️ Technologies

| Technologie | Version | Rôle |
|------------|---------|------|
| **Phaser 3** | ^3.87.0 | Moteur de jeu (rendu, physique, assets) |
| **TypeScript** | ^5.6.3 | Langage principal (typage strict) |
| **Vite** | ^6.0.3 | Build tool moderne (HMR, optimisations) |
| **Node.js** | 18+ | Environnement d'exécution |

---

## 📦 Installation

### Prérequis

- Node.js 18 ou supérieur
- npm ou yarn

### Étapes

```bash
# Cloner le dépôt
git clone <url-du-repo>
cd CycloCross2025

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

Le jeu sera accessible sur `http://localhost:3000`.

---

## 🚀 Scripts disponibles

| Commande | Description |
|----------|-------------|
| `npm run dev` | Lance le serveur de développement avec HMR |
| `npm run build` | Build de production dans `/dist` |
| `npm run preview` | Prévisualise le build de production |
| `npm run type-check` | Vérifie les types TypeScript sans build |

---

## 🏗️ Architecture

### Principes architecturaux

Le projet utilise une **architecture Entity-Component** adaptée à Phaser :

```
┌─────────────────────────────────────────┐
│         Phaser GameObjects              │
│     (Sprite, Container, etc.)           │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │     Composants Métier             │ │
│  │  (StaminaComponent, AIComponent)  │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**Avantages :**
- ✅ Séparation rendu (Phaser) / logique métier (Components)
- ✅ Réutilisabilité des composants
- ✅ Testabilité maximale
- ✅ Extensibilité sans modifier l'existant (Open/Closed Principle)

### Flux de données

```
User Input → Command → Entity → Component → State/Strategy → GameObject Update
```

---

## 📁 Structure du projet

```
CycloCross2025/
├── assets/                      # Ressources du jeu
│   ├── sprites/                 # Images et spritesheets
│   ├── tilemaps/                # Cartes du parcours
│   └── sounds/                  # Musiques et effets sonores
│
├── src/
│   ├── main.ts                  # Point d'entrée de l'application
│   │
│   ├── config/                  # Configuration du jeu
│   │   ├── gameConfig.ts        # Configuration Phaser
│   │   ├── constants.ts         # Constantes globales
│   │   └── index.ts             # Exports centralisés
│   │
│   ├── scenes/                  # Scènes Phaser
│   │   └── RaceScene.ts         # Scène de course principale
│   │
│   ├── entities/                # Entités du jeu (GameObjects)
│   │   └── DemoSprite.ts        # Exemple d'entité avec composants
│   │
│   ├── components/              # Composants métier
│   │   ├── BaseComponent.ts     # Classe de base des composants
│   │   └── RotationComponent.ts # Exemple de composant
│   │
│   ├── systems/                 # Systèmes globaux
│   │   ├── RaceManager.ts       # (À venir) Gestion de la course
│   │   └── TerrainManager.ts    # (À venir) Gestion du terrain
│   │
│   ├── patterns/                # Design Patterns
│   │   ├── commands/            # Pattern Command
│   │   ├── strategies/          # Pattern Strategy
│   │   ├── states/              # Pattern State
│   │   └── factories/           # Pattern Factory
│   │
│   ├── types/                   # Types et interfaces TypeScript
│   │   ├── IComponent.ts        # Interface des composants
│   │   ├── ICommand.ts          # Interface Command
│   │   ├── IState.ts            # Interface State
│   │   ├── IStrategy.ts         # Interface Strategy
│   │   ├── enums.ts             # Énumérations
│   │   ├── gameData.ts          # Types de données métier
│   │   └── index.ts             # Exports centralisés
│   │
│   └── utils/                   # Fonctions utilitaires
│       └── MathUtils.ts         # Utilitaires mathématiques
│
├── index.html                   # Point d'entrée HTML
├── package.json                 # Dépendances et scripts
├── tsconfig.json                # Configuration TypeScript
├── vite.config.ts               # Configuration Vite
└── README.md                    # Ce fichier
```

---

## 🎨 Design Patterns

### 1. **Entity-Component Pattern**

Sépare les GameObjects Phaser de la logique métier.

```typescript
// Component
class StaminaComponent implements IComponent {
  constructor(private owner: Phaser.GameObjects.GameObject) {}

  update(time: number, delta: number): void {
    // Logique d'endurance
  }
}

// Entity
class Cyclist extends Phaser.GameObjects.Sprite {
  private components: IComponent[] = [];

  addComponent(component: IComponent): void {
    this.components.push(component);
  }
}
```

### 2. **Command Pattern**

Encapsule les actions en objets (utile pour input, undo/redo, replay, IA).

```typescript
interface IGameCommand {
  execute(entity: Cyclist, deltaTime: number): void;
  undo?(entity: Cyclist, deltaTime: number): void;
  readonly name?: string;
  readonly priority?: number;
}

class AccelerateCommand implements IGameCommand {
  public readonly name = 'Accelerate';
  public readonly priority = 10;

  execute(entity: Cyclist, _deltaTime: number): void {
    const body = entity.getBody();
    const angle = entity.rotation;
    const forceX = Math.cos(angle) * CYCLIST_ACCELERATION;
    const forceY = Math.sin(angle) * CYCLIST_ACCELERATION;
    body.setAcceleration(forceX, forceY);
  }
}
```

**Voir [COMMAND_PATTERN.md](docs/COMMAND_PATTERN.md) pour un guide complet.**

### 3. **State Pattern**

Gère les états du cycliste (pédalage, sprint, portage, chute).

```typescript
interface IState<TContext> {
  enter(context: TContext): void;
  update(context: TContext, delta: number): void;
  exit(context: TContext): void;
}

class RidingState implements IState<Cyclist> {
  enter(cyclist: Cyclist): void { /* ... */ }
  update(cyclist: Cyclist, delta: number): void { /* ... */ }
  exit(cyclist: Cyclist): void { /* ... */ }
}
```

### 4. **Strategy Pattern**

Interchangeabilité des algorithmes (IA, calculs de terrain).

```typescript
interface IStrategy<TInput, TOutput> {
  execute(input: TInput): TOutput;
}

class AggressiveAI implements IStrategy<AIInput, void> {
  execute(input: AIInput): void {
    // Logique d'IA agressive
  }
}
```

---

## 📐 Conventions de code

### TypeScript

- **Mode strict activé** (`strict: true`)
- **Pas de `any`** (utiliser `unknown` si nécessaire)
- **Types explicites** pour les paramètres et retours de fonctions publiques
- **JSDoc** pour toutes les interfaces et classes publiques

### Nommage

| Type | Convention | Exemple |
|------|-----------|---------|
| Classes | PascalCase | `RaceManager`, `Cyclist` |
| Interfaces | IPascalCase | `IComponent`, `ICommand` |
| Types | PascalCase | `CyclistStats`, `TerrainData` |
| Enums | PascalCase | `TerrainType`, `CyclistState` |
| Variables | camelCase | `maxSpeed`, `currentState` |
| Constants | UPPER_SNAKE_CASE | `GAME_WIDTH`, `GRAVITY` |
| Fichiers | PascalCase.ts | `RaceScene.ts`, `BaseComponent.ts` |

### Organisation des fichiers

- **Un export principal par fichier** (sauf pour types/enums)
- **Imports groupés** : librairies externes → internes → types
- **Alias de paths** : `@config`, `@scenes`, `@types`, etc.

---

## 🧪 Développement

### Hot Module Replacement (HMR)

Vite supporte le HMR : les modifications de code sont reflétées instantanément sans recharger la page.

### Debugging

L'instance Phaser est exposée globalement :

```javascript
// Dans la console du navigateur
window.game // Instance Phaser.Game
window.game.scene.keys.RaceScene // Accès à la scène
```

### Configuration du debug Phaser

Dans [constants.ts](src/config/constants.ts) :

```typescript
export const DEBUG_MODE = true;  // Active le mode debug
export const SHOW_FPS = true;    // Affiche les FPS
export const SHOW_COLLISIONS = false; // Affiche les hitboxes
```

---

## 📚 Documentation technique

### Documentation avancée

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Architecture détaillée du projet
- **[PHYSICS.md](docs/PHYSICS.md)** - Documentation complète du système physique
- **[CONTROLS.md](docs/CONTROLS.md)** - Guide des contrôles et input système
- **[COMMAND_PATTERN.md](docs/COMMAND_PATTERN.md)** - Guide complet du Command Pattern pour l'input système
- **[TEST_GUIDE.md](docs/TEST_GUIDE.md)** - Guide de test du système de mouvement

### Cycle de vie d'un composant

```typescript
class CustomComponent extends BaseComponent {
  // 1. Constructeur
  constructor(owner: Phaser.GameObjects.GameObject) {
    super(owner);
  }

  // 2. Initialisation (appelé une fois)
  init(): void {
    // Setup initial
  }

  // 3. Pre-update (chaque frame)
  preUpdate(time: number, delta: number): void {
    // Calculs préparatoires
  }

  // 4. Update (chaque frame)
  update(time: number, delta: number): void {
    // Logique principale
  }

  // 5. Destruction
  destroy(): void {
    // Nettoyage
  }
}
```

### Cycle de vie d'une scène Phaser

```typescript
class CustomScene extends Phaser.Scene {
  // 1. Préchargement des assets
  preload(): void {
    this.load.image('key', 'path/to/image.png');
  }

  // 2. Création de la scène
  create(): void {
    // Initialisation des GameObjects
  }

  // 3. Mise à jour (60 FPS)
  update(time: number, delta: number): void {
    // Logique du jeu
  }
}
```

### Ajout d'un nouveau composant

1. Créer le fichier dans `src/components/`
2. Hériter de `BaseComponent`
3. Implémenter la méthode `update()`
4. Attacher le composant à une entité

```typescript
// MonComposant.ts
export class MonComposant extends BaseComponent {
  update(time: number, delta: number): void {
    // Logique
  }
}

// Dans une entité ou scène
const sprite = new DemoSprite(this, x, y);
sprite.addComponent(new MonComposant(sprite));
```

---

## 🎓 Objectifs pédagogiques

Ce projet démontre :

✅ **Intégration d'un moteur de jeu** (Phaser 3) avec une architecture custom
✅ **TypeScript strict** pour la qualité et la maintenabilité
✅ **Design Patterns** appliqués à un contexte de jeu
✅ **Principes SOLID** (Single Responsibility, Open/Closed, etc.)
✅ **Séparation des préoccupations** (rendu vs logique métier)
✅ **Tooling moderne** (Vite, HMR, path aliases)
✅ **Documentation professionnelle** (JSDoc, README, architecture)

---

## 🚧 Prochaines étapes (Prompts suivants)

Ce projet est en développement itératif. Les prochaines fonctionnalités incluront :

### ✅ Terminé (Prompts 1-3)
- [x] Architecture de base avec Entity-Component Pattern
- [x] Système d'input et contrôles joueur (flèches + SHIFT)
- [x] Implémentation des cyclistes avec Phaser Arcade Physics
- [x] Physique réaliste (inertie, accélération, freinage)
- [x] Système de caméra suivant le joueur
- [x] Rotation dépendante de la vitesse
- [x] Command Pattern pour le système d'input (découplage, testabilité, extensibilité)
- [x] Configuration des key bindings (DEFAULT, WASD, HYBRID)
- [x] InputHandler pour mapper actions → commandes

### 🔜 À venir
- [ ] Gestion du terrain et obstacles
- [ ] Système d'endurance et équilibre
- [ ] Intelligence Artificielle des adversaires
- [ ] Interface utilisateur (HUD avec endurance, vitesse, position)
- [ ] Système de collisions
- [ ] Menu et écran de résultats
- [ ] Sons et musiques
- [ ] Système de particules et effets visuels (boue, poussière)

---

## 📝 Licence

Projet éducatif développé dans le cadre d'un cours universitaire.

---

## 🤝 Contribution

Ce projet suit une approche pédagogique guidée par prompts. Pour toute question ou suggestion d'amélioration de l'architecture, ouvrir une issue ou un PR.

---

**Développé avec ❤️ et Phaser 3**
