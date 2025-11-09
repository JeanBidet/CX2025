# Documentation des Paramètres Physiques - CycloCross 2025

## Vue d'ensemble

Ce document explique tous les paramètres physiques utilisés dans le jeu et leur impact sur le mouvement du cycliste. Les valeurs ont été ajustées pour donner une sensation réaliste de conduite d'un vélo de cyclo-cross.

---

## Système de Physique

### Moteur Physique : Phaser Arcade Physics

Le jeu utilise **Phaser Arcade Physics**, un moteur physique 2D simple et performant qui gère :
- Velocity (vitesse)
- Acceleration (accélération)
- Drag (résistance/friction)
- Mass (masse/inertie)
- Collisions

**Avantages :**
- Performances excellentes (60 FPS stable)
- Intégration automatique du delta time
- Formules physiques pré-implémentées

---

## Paramètres du Cycliste

Tous les paramètres sont définis dans [src/config/constants.ts](src/config/constants.ts).

### 1. Accélération

```typescript
CYCLIST_ACCELERATION = 300  // pixels/seconde²
```

**Description :** Force appliquée lorsque le joueur accélère (touche ↑).

**Impact :**
- Plus c'est élevé, plus le cycliste accélère vite
- Valeur actuelle : accélération modérée, réaliste pour un vélo

**Formule Phaser :**
```
velocity += acceleration * deltaTime
```

**Recommandations d'ajustement :**
- 200-250 : Accélération lente (vélo lourd, terrain difficile)
- 300-350 : Accélération normale ✅
- 400-500 : Accélération rapide (vélo léger, asphalte)

---

### 2. Freinage

```typescript
CYCLIST_BRAKE_ACCELERATION = 500  // pixels/seconde²
```

**Description :** Force appliquée lors du freinage (touche ↓).

**Impact :**
- Plus c'est élevé, plus le cycliste ralentit vite
- Valeur actuelle : freinage efficace mais pas instantané

**Recommandations d'ajustement :**
- 300-400 : Freinage progressif
- 500-600 : Freinage normal ✅
- 700+ : Freinage d'urgence (adhérence maximale)

---

### 3. Vitesse Maximale

```typescript
CYCLIST_MAX_SPEED = 400        // pixels/seconde (normal)
CYCLIST_SPRINT_MAX_SPEED = 600 // pixels/seconde (sprint)
```

**Description :** Vitesse maximale que peut atteindre le cycliste.

**Impact :**
- Limite la vitesse peu importe l'accélération
- Sprint : +50% de vitesse

**Conversion approximative :**
- 400 px/s ≈ 25 km/h (vitesse normale)
- 600 px/s ≈ 38 km/h (sprint)

**Recommandations d'ajustement :**
- 300-350 : Cycliste lent
- 400-450 : Vitesse normale ✅
- 500-600 : Cycliste rapide
- 700+ : Cycliste pro

---

### 4. Drag (Résistance)

```typescript
CYCLIST_DRAG = 0.05
```

**Valeur effective appliquée :** `0.05 * 10000 = 500`

**Description :** Friction de l'air et résistance naturelle qui ralentit progressivement le cycliste.

**Impact :**
- Plus c'est élevé, plus le cycliste ralentit vite sans input
- Simule la résistance de l'air et la friction du terrain

**Formule Phaser :**
```
velocity *= (1 - drag * deltaTime)
```

**Comportement :**
- Drag = 0 : Le cycliste ne ralentit jamais (glisse à l'infini)
- Drag faible (0.01-0.03) : Ralentissement très lent
- Drag normal (0.05) : Ralentissement progressif ✅
- Drag élevé (0.1+) : Ralentissement rapide

**Recommandations d'ajustement :**
- 0.03 : Terrain lisse (asphalte)
- 0.05 : Terrain normal ✅
- 0.08 : Terrain difficile (herbe)
- 0.12+ : Terrain très difficile (boue)

---

### 5. Masse

```typescript
CYCLIST_MASS = 1
```

**Description :** Masse du cycliste + vélo. Affecte l'inertie et les collisions.

**Impact :**
- Plus c'est élevé, plus il est difficile de changer la vitesse
- Affecte les collisions (un cycliste lourd pousse plus fort)

**Recommandations d'ajustement :**
- 0.5 : Cycliste léger (vélo de route)
- 1.0 : Normal ✅
- 1.5 : Cycliste lourd (VTT, équipement)
- 2.0+ : Très lourd (cargo bike)

---

### 6. Bounce (Élasticité)

```typescript
CYCLIST_BOUNCE = 0.2
```

**Description :** Élasticité lors des collisions (0 = pas de rebond, 1 = rebond total).

**Impact :**
- Détermine si le cycliste rebondit sur les obstacles
- Valeur actuelle : léger rebond réaliste

**Recommandations d'ajustement :**
- 0.0 : Pas de rebond (collision mole)
- 0.2 : Rebond léger ✅
- 0.5 : Rebond moyen
- 0.8+ : Très élastique (irréaliste)

---

### 7. Rotation

```typescript
CYCLIST_ROTATION_SPEED_LOW = 180   // degrés/seconde (vitesse basse)
CYCLIST_ROTATION_SPEED_HIGH = 90   // degrés/seconde (vitesse haute)
CYCLIST_ROTATION_SPEED_THRESHOLD = 200  // seuil de vitesse
CYCLIST_ROTATION_LERP = 0.1  // facteur d'interpolation
```

**Description :** Vitesse de rotation du cycliste selon sa vitesse actuelle.

**Logique :**
- À basse vitesse (< 200 px/s) : rotation rapide (180°/s) → rayon de braquage serré
- À haute vitesse (> 200 px/s) : rotation lente (90°/s) → rayon de braquage large

**Impact :**
- Simule la maniabilité réaliste d'un vélo
- Plus on va vite, plus il est difficile de tourner

**Lerp (Linear Interpolation) :**
- 0.1 = rotation très douce (réaliste) ✅
- 0.5 = rotation rapide
- 1.0 = rotation instantanée (pas fluide)

**Recommandations d'ajustement :**

Pour rotation plus rapide :
```typescript
CYCLIST_ROTATION_SPEED_LOW = 270
CYCLIST_ROTATION_SPEED_HIGH = 135
```

Pour rotation plus lente :
```typescript
CYCLIST_ROTATION_SPEED_LOW = 120
CYCLIST_ROTATION_SPEED_HIGH = 60
```

---

## Formules Physiques Utilisées

### 1. Accélération dans une direction

```typescript
// Calculer les composantes X et Y de l'accélération
const angle = cyclist.rotation;
const forceX = Math.cos(angle) * acceleration;
const forceY = Math.sin(angle) * acceleration;

// Appliquer au body Phaser
body.setAcceleration(forceX, forceY);
```

**Explication :**
- L'angle du cycliste détermine la direction
- `Math.cos(angle)` donne la composante horizontale
- `Math.sin(angle)` donne la composante verticale
- Phaser intègre automatiquement : `velocity += acceleration * delta`

---

### 2. Freinage

```typescript
// Vecteur de direction actuel (normalisé)
const speed = Math.sqrt(velocity.x² + velocity.y²);
const dirX = velocity.x / speed;
const dirY = velocity.y / speed;

// Force de freinage dans la direction opposée
const brakeForceX = -dirX * CYCLIST_BRAKE_ACCELERATION;
const brakeForceY = -dirY * CYCLIST_BRAKE_ACCELERATION;

body.setAcceleration(brakeForceX, brakeForceY);
```

**Explication :**
- On calcule la direction actuelle du mouvement
- On applique une force dans la direction opposée
- Le cycliste ralentit progressivement

---

### 3. Vitesse actuelle (scalaire)

```typescript
const speed = Math.sqrt(velocity.x² + velocity.y²);
```

**Explication :**
- Théorème de Pythagore pour calculer la norme du vecteur vitesse
- Utile pour afficher la vitesse au joueur
- Utilisé pour déterminer le comportement de rotation

---

## Multiplicateurs de Terrain (à venir)

Dans les prompts suivants, on ajoutera des multiplicateurs de terrain :

```typescript
// Exemple
const terrainMultiplier = 0.6; // Boue
const effectiveAcceleration = CYCLIST_ACCELERATION * terrainMultiplier;
```

**Impact :**
- `1.0` : Terrain normal (asphalte)
- `0.85` : Herbe
- `0.6` : Boue
- `0.5` : Sable

---

## Tests et Ajustements

### Comment tester les paramètres

1. **Lancer le jeu :**
```bash
npm run dev
```

2. **Tester l'accélération :**
- Appuyer sur ↑ et observer le temps pour atteindre la vitesse max
- Trop lent ? Augmenter `CYCLIST_ACCELERATION`
- Trop rapide ? Diminuer `CYCLIST_ACCELERATION`

3. **Tester le freinage :**
- Atteindre la vitesse max puis appuyer sur ↓
- Noter le temps d'arrêt
- Ajuster `CYCLIST_BRAKE_ACCELERATION` si nécessaire

4. **Tester l'inertie (drag) :**
- Accélérer puis relâcher toutes les touches
- Observer combien de temps le cycliste met à s'arrêter
- Ajuster `CYCLIST_DRAG`

5. **Tester la rotation :**
- À basse vitesse : tourner doit être facile
- À haute vitesse : tourner doit être difficile
- Ajuster `CYCLIST_ROTATION_SPEED_LOW/HIGH`

### Console de debug

Ouvrir la console du navigateur (F12) pour voir :
- Logs d'initialisation des composants
- Vitesse actuelle (si décommenté dans MovementComponent)
- Événements physiques

---

## Comparaison des Valeurs

| Paramètre | Lent | Normal ✅ | Rapide |
|-----------|------|----------|--------|
| Accélération | 200 | 300 | 500 |
| Freinage | 300 | 500 | 800 |
| Vitesse max | 300 | 400 | 600 |
| Drag | 0.03 | 0.05 | 0.10 |
| Masse | 0.5 | 1.0 | 2.0 |
| Rotation (basse vitesse) | 120 | 180 | 270 |

---

## Prochaines Étapes

Dans les prompts suivants, on ajoutera :
1. **Multiplicateurs de terrain** dynamiques selon la surface
2. **Système d'endurance** qui affecte l'accélération
3. **Perte d'équilibre** qui affecte la vélocité
4. **Collisions** avec obstacles et autres cyclistes
5. **Effets visuels** (particules de boue, poussière)

---

## Ressources

- [Phaser 3 Arcade Physics Documentation](https://photonstorm.github.io/phaser3-docs/Phaser.Physics.Arcade.html)
- [Arcade Body Properties](https://photonstorm.github.io/phaser3-docs/Phaser.Physics.Arcade.Body.html)
- [Game Feel: A Game Designer's Guide to Virtual Sensation](https://www.amazon.com/Game-Feel-Designers-Sensation-Kaufmann/dp/0123743281)

---

**Document mis à jour le 28 octobre 2025**
**Projet CycloCross 2025 - Système de physique et mouvement**
