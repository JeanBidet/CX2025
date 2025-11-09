# Contrôles - CycloCross 2025

## Contrôles du Joueur

### Clavier

| Touche | Action | Description |
|--------|--------|-------------|
| **↑** (Flèche Haut) | Accélérer | Applique une force d'accélération dans la direction du cycliste |
| **↓** (Flèche Bas) | Freiner | Applique une force de freinage pour ralentir |
| **←** (Flèche Gauche) | Tourner à gauche | Fait pivoter le cycliste vers la gauche |
| **→** (Flèche Droite) | Tourner à droite | Fait pivoter le cycliste vers la droite |
| **SHIFT** | Sprint | Augmente temporairement la vitesse maximale (+50%) |

---

## Comportements de Contrôle

### Accélération (↑)
- Applique une force continue dans la direction du cycliste
- L'accélération est progressive (pas instantanée)
- Affectée par le terrain (à venir dans les prompts suivants)
- Limitée par la vitesse maximale

### Freinage (↓)
- Applique une force dans la direction opposée au mouvement
- Freinage progressif (pas d'arrêt brutal)
- Plus efficace que simplement relâcher les touches
- Arrêt complet si la vitesse devient très faible

### Rotation (← →)
- **À basse vitesse** : rotation rapide (rayon de braquage serré)
- **À haute vitesse** : rotation lente (rayon de braquage large)
- Interpolation douce pour éviter les rotations saccadées
- Simule la maniabilité réaliste d'un vélo

### Sprint (SHIFT)
- Augmente la vitesse maximale de 400 à 600 pixels/seconde
- Peut être combiné avec l'accélération
- Dans les prompts suivants : consommera de l'endurance

---

## Inertie et Physique

### Sans Input
Lorsqu'aucune touche n'est pressée :
- Le cycliste ralentit progressivement (drag/friction)
- La vitesse ne tombe jamais immédiatement à 0
- Simule la résistance de l'air et la friction du terrain

### Changements de Direction
- Impossible de tourner instantanément à 180°
- La rotation est limitée par la vitesse actuelle
- Plus réaliste qu'un contrôle arcade traditionnel

---

## Astuces de Gameplay

1. **Anticipez les virages**
   - Ralentissez avant les virages serrés
   - À haute vitesse, commencez à tourner plus tôt

2. **Gestion de l'Inertie**
   - Utilisez le freinage actif plutôt que de simplement relâcher
   - L'inertie peut être utilisée pour économiser de l'énergie

3. **Sprint Stratégique**
   - Ne sprintez pas en continu (endurance à venir)
   - Utilisez le sprint pour des courtes accélérations

4. **Rotation à Basse Vitesse**
   - Ralentissez pour faire des virages serrés
   - À l'arrêt, vous pouvez pivoter rapidement

---

## Configuration Technique

Les contrôles sont implémentés via :
- **InputComponent** : Capture les inputs Phaser
- **MovementComponent** : Applique les forces physiques
- **Phaser Arcade Physics** : Gère la physique bas niveau

### Personnalisation
Pour modifier les touches, éditez [src/components/InputComponent.ts](src/components/InputComponent.ts) :

```typescript
this.keys = {
  up: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W),      // WASD
  down: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S),
  left: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A),
  right: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D),
  sprint: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SHIFT),
};
```

---

## Prochaines Fonctionnalités

Dans les prompts suivants, on ajoutera :
- **Saut** (ESPACE) pour franchir les obstacles
- **Portage du vélo** pour les obstacles non franchissables
- **Endurance** qui limite le sprint
- **Gamepad/Manette** support

---

**Document créé le 28 octobre 2025**
**Projet CycloCross 2025 - Contrôles**
