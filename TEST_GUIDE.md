# Guide de Test - CycloCross 2025

## 🚀 Démarrage Rapide

```bash
# Dans le dossier du projet
npm run dev
```

Le jeu s'ouvre automatiquement sur **http://localhost:3001**

---

## ✅ Checklist de Test - Prompt 2

### 1. Affichage Initial

**Ce que vous devriez voir :**
- [ ] Fond bleu ciel
- [ ] Zone herbeuse (vert clair transparent) en bas
- [ ] Ligne verte marquant le sol
- [ ] FPS affiché en haut à gauche (vert, ~60)
- [ ] Instructions de contrôle en haut à gauche
- [ ] Cycliste cyan au départ (rectangle avec triangle blanc)

**Console du navigateur (F12) :**
```
[RaceScene] Create - Initialisation de la scène
[RaceScene] Monde physique: 10000x720
[RaceScene] Caméra configurée
[Cyclist] Player créé à (100, 550)
[Cyclist] Physique configurée
[MovementComponent] Initialisé
[InputComponent] Initialisé - Touches: Flèches + Shift pour sprint
[RaceScene] Joueur créé et configuré
[RaceScene] Caméra configurée pour suivre le joueur
```

---

### 2. Test d'Accélération (↑)

**Actions :**
1. Appuyer sur ↑ et maintenir
2. Observer le cycliste

**Comportement attendu :**
- [ ] Le cycliste accélère progressivement
- [ ] La vitesse augmente graduellement (pas instantanée)
- [ ] Le cycliste atteint une vitesse maximale (~400 px/s)
- [ ] La caméra suit le cycliste en douceur
- [ ] Le monde défile de droite à gauche

**Timing :**
- Accélération de 0 à vitesse max : ~2-3 secondes

---

### 3. Test de Freinage (↓)

**Actions :**
1. Accélérer jusqu'à vitesse maximale
2. Appuyer sur ↓
3. Observer le ralentissement

**Comportement attendu :**
- [ ] Le cycliste ralentit progressivement
- [ ] Pas d'arrêt instantané
- [ ] Arrêt complet après ~1-2 secondes
- [ ] Pas de recul (le cycliste ne va pas en arrière)

---

### 4. Test de Rotation (← →)

**Actions :**
1. À l'arrêt, appuyer sur ← ou →
2. En mouvement lent, tourner
3. À haute vitesse, tourner

**Comportement attendu :**

**À l'arrêt :**
- [ ] Rotation rapide
- [ ] Le cycliste pivote sur place

**À basse vitesse (<200 px/s) :**
- [ ] Rotation rapide (180°/s)
- [ ] Rayon de braquage serré
- [ ] Facile de faire des virages serrés

**À haute vitesse (>200 px/s) :**
- [ ] Rotation lente (90°/s)
- [ ] Rayon de braquage large
- [ ] Impossible de tourner brusquement

**Interpolation :**
- [ ] Rotation douce, pas saccadée
- [ ] Pas de spin instantané

---

### 5. Test de Sprint (SHIFT)

**Actions :**
1. Accélérer normalement (↑ seul)
2. Noter la vitesse maximale
3. Accélérer avec sprint (↑ + SHIFT)
4. Comparer

**Comportement attendu :**
- [ ] Avec SHIFT : vitesse max augmente de ~50%
- [ ] Normal : ~400 px/s
- [ ] Sprint : ~600 px/s
- [ ] Console log : `[MovementComponent] Sprint: true`

---

### 6. Test d'Inertie (Aucune touche)

**Actions :**
1. Accélérer à vitesse maximale
2. Relâcher toutes les touches
3. Observer

**Comportement attendu :**
- [ ] Le cycliste continue sur sa lancée
- [ ] Ralentissement progressif (pas brutal)
- [ ] Arrêt après ~3-5 secondes
- [ ] Pas d'arrêt instantané

**Explication :**
- C'est le **drag** (friction) qui ralentit le cycliste
- Simule la résistance de l'air

---

### 7. Test de la Caméra

**Actions :**
1. Accélérer vers la droite
2. Observer le comportement de la caméra

**Comportement attendu :**
- [ ] La caméra suit le cycliste
- [ ] Mouvement fluide (lerp, pas saccadé)
- [ ] Le cycliste reste légèrement à gauche du centre (offset de -200)
- [ ] Le monde défile continuellement
- [ ] Pas de "snap" brusque

**Détails techniques :**
- Lerp factor : 0.1 (suivi doux)
- Offset : -200, 0 (décalage à gauche)
- Deadzone : 100×100 (évite micro-mouvements)

---

### 8. Test de Combinaison

**Actions :**
1. ↑ + ← (accélérer + tourner gauche)
2. ↑ + → (accélérer + tourner droite)
3. ↑ + SHIFT (accélérer + sprint)
4. ↓ + ← (freiner + tourner)

**Comportement attendu :**
- [ ] Toutes les combinaisons fonctionnent
- [ ] Pas de conflit entre les touches
- [ ] Comportement fluide

---

### 9. Test du FPS

**Vérifications :**
- [ ] FPS affiché = ~60
- [ ] Stable (pas de baisse)
- [ ] Pas de lag perceptible
- [ ] Mouvement fluide

**En cas de FPS bas :**
- Vérifier la console (F12) pour erreurs
- Fermer autres onglets
- Relancer le navigateur

---

### 10. Test des Limites du Monde

**Actions :**
1. Accélérer vers la droite pendant longtemps
2. Atteindre la fin du monde (10000 pixels)

**Comportement attendu :**
- [ ] Le cycliste peut aller très loin (10000 px)
- [ ] La caméra suit toujours
- [ ] Pas de limite artificielle visible
- [ ] Pas de téléportation

---

## 🐛 Problèmes Courants et Solutions

### Le cycliste n'apparaît pas
**Solutions :**
1. Vérifier la console (F12) pour erreurs
2. Rafraîchir la page (Ctrl+R)
3. Vérifier que le serveur est lancé

### Le cycliste ne bouge pas
**Vérifications :**
1. Les touches fonctionnent-elles dans d'autres applications ?
2. Console : y a-t-il des erreurs ?
3. InputComponent initialisé ? (voir logs)

### FPS bas (<60)
**Solutions :**
1. Fermer autres onglets/applications
2. Utiliser un navigateur moderne (Chrome/Firefox)
3. Vérifier que le GPU est activé

### Caméra saccadée
**Vérifications :**
1. FPS stable à 60 ?
2. Console : erreurs JavaScript ?
3. Trop d'objets dans la scène ?

### Rotation trop rapide/lente
**Ajustement :**
Modifier [src/config/constants.ts](src/config/constants.ts) :
```typescript
CYCLIST_ROTATION_SPEED_LOW = 270  // Plus rapide
CYCLIST_ROTATION_SPEED_HIGH = 45  // Plus lent
```

---

## 🎮 Scénarios de Test Avancés

### Scénario 1 : Course Simple
1. Démarrer
2. Accélérer (↑)
3. Tourner légèrement (← ou →)
4. Sprinter (SHIFT)
5. Freiner avant l'arrêt (↓)

**Objectif :** Tester le flow complet

### Scénario 2 : Slalom
1. Accélérer
2. Alterner ← et → rapidement
3. Observer la maniabilité

**Objectif :** Tester la rotation à différentes vitesses

### Scénario 3 : Stop & Go
1. Accélérer → Freiner → Arrêt complet
2. Répéter 5 fois
3. Observer la fluidité

**Objectif :** Tester l'inertie et le freinage

### Scénario 4 : Sprint Burst
1. Vitesse normale
2. Sprint 2 secondes (SHIFT)
3. Relâcher SHIFT
4. Observer le changement de vitesse max

**Objectif :** Tester le système de sprint

---

## 📊 Métriques à Noter

Pendant les tests, notez :
- [ ] FPS moyen : __________
- [ ] FPS min : __________
- [ ] Temps 0→vitesse max : __________ secondes
- [ ] Temps vitesse max→0 (freinage) : __________ secondes
- [ ] Temps vitesse max→0 (inertie) : __________ secondes
- [ ] Facilité des virages (1-10) : __________
- [ ] Fluidité globale (1-10) : __________

---

## 🔧 Debug Console

### Commandes utiles (dans la console F12)

```javascript
// Accéder au jeu
window.game

// Accéder à la scène
const scene = window.game.scene.keys.RaceScene

// Accéder au joueur (si exposé)
// Note: non exposé par défaut, à ajouter pour debug

// Recharger la page
location.reload()

// Afficher les FPS
window.game.loop.actualFps
```

---

## ✅ Validation Finale

### Checklist complète

- [ ] Tous les contrôles fonctionnent
- [ ] Mouvement fluide et réaliste
- [ ] Inertie perceptible
- [ ] Rotation dépendante de la vitesse
- [ ] Sprint augmente la vitesse
- [ ] Caméra suit le joueur
- [ ] FPS stable à 60
- [ ] Aucune erreur console
- [ ] Code TypeScript compile sans erreur

### Commande finale de validation

```bash
npm run type-check
```

**Résultat attendu :** Aucune erreur TypeScript

---

## 📝 Rapport de Test

**Date :** __________
**Testeur :** __________
**Navigateur :** __________
**OS :** __________

### Résultats

| Test | Statut | Notes |
|------|--------|-------|
| Affichage initial | ☐ | |
| Accélération | ☐ | |
| Freinage | ☐ | |
| Rotation | ☐ | |
| Sprint | ☐ | |
| Inertie | ☐ | |
| Caméra | ☐ | |
| FPS | ☐ | |
| Combinaisons | ☐ | |

### Bugs trouvés

1. __________________________________________
2. __________________________________________
3. __________________________________________

### Améliorations suggérées

1. __________________________________________
2. __________________________________________
3. __________________________________________

---

**Guide créé le 28 octobre 2025**
**Pour CycloCross 2025 - Prompt 2**
