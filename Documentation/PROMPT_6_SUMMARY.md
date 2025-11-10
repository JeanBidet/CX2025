# PROMPT 6 : SYSTÈME D'ENDURANCE ET D'ÉQUILIBRE - Synthèse d'Implémentation

**Date**: 2025-11-10
**Objectif**: Implémenter les mécaniques de jauges (endurance et équilibre) au cœur du gameplay du cyclo-cross

---

## 📋 Vue d'ensemble

Ce prompt a permis d'implémenter un système complet de gestion de l'endurance et de l'équilibre pour le cycliste, avec des calculs dynamiques basés sur le contexte (terrain, vitesse, pente) et une interface utilisateur claire avec pygame.draw.

---

## ✅ Éléments Implémentés

### 1. **StaminaComponent** (`components/stamina_component.py`)

Composant gérant l'endurance du cycliste avec :

#### Attributs
- `current_stamina: float` - Valeur actuelle (0-100)
- `max_stamina: float` - Capacité totale
- `fatigue_level: float` - Fatigue cumulative (0-100)
- `recovery_rate: float` - Taux de récupération
- `base_drain_rate: float` - Consommation de base

#### Méthodes Clés
- `drain(amount)` - Consommer de l'endurance
- `set_recovering(bool)` - Activer/désactiver récupération
- `get_percentage()` - Obtenir % restant (0-100)
- `get_performance_zone()` - Obtenir zone actuelle
- `get_speed_multiplier()` - Multiplicateur de vitesse selon zone
- `apply_fatigue(amount)` - Ajouter de la fatigue
- `get_fatigue_percentage()` - % de fatigue

#### Calculs Dynamiques

**Formule de drain** :
```
drain = base_drain * velocity_factor * terrain_multiplier * slope_multiplier * fatigue_factor
```

Facteurs :
- **Vitesse** : `1.0 + (current_speed * 0.015)`
- **Terrain** : Multiplicateur du `TerrainData.stamina_drain_multiplier`
- **Pente** :
  - Montée : `1.0 + (slope / 45°) * 2.5`
  - Descente : `max(0.5, 1.0 - (slope / 45°) * 0.5)`
- **Fatigue** : `1.0 + (fatigue / 100) * 0.5`

**Récupération** :
```
recovery = recovery_rate * fatigue_penalty * delta_time
fatigue_penalty = 1.0 - (fatigue / 100) * 0.3
```

---

### 2. **BalanceComponent** (`components/balance_component.py`)

Composant gérant l'équilibre du cycliste avec :

#### Attributs
- `current_balance: float` - Équilibre actuel (0-100)
- `max_balance: float` - Équilibre maximal
- `instability: float` - Facteur temporaire d'instabilité
- `critical_threshold: float` - Seuil de zone critique (20)
- `crash_threshold: float` - Seuil de chute garantie (5)

#### Méthodes Clés
- `apply_imbalance(amount, source)` - Appliquer déséquilibre externe
- `is_critical()` - Vérifier si proche de chute
- `should_crash()` - Déterminer si chute nécessaire
- `get_stability_level()` - Retourne "STABLE", "UNSTABLE", "CRITICAL"
- `reset_balance()` - Réinitialiser après remontée

#### Calculs d'Instabilité

Facteurs d'instabilité :
1. **Camber** (inclinaison latérale) : `abs(camber) * 1.5`
2. **Virages** : `rotation_change * speed_factor * 0.8 * 100`
3. **Grip du terrain** : `(1.0 - grip_level) * 2.0`
4. **Épuisement** : Si endurance < 30%, facteur `* 1.8`

**Chute probabiliste** :
- En dessous de `crash_threshold` : chute garantie
- Entre `crash_threshold` et `critical_threshold` :
  ```
  probability = ((critical - current) / (critical - crash)) * 0.3
  ```

---

### 3. **Zones de Performance** (`config/constants.py`)

Enum `PerformanceZone` :

| Zone | Seuil Endurance | Modificateur Vitesse | Effets |
|------|----------------|---------------------|--------|
| **OPTIMAL** | 70-100% | 1.0x | Performance normale |
| **MODERATE** | 40-70% | 0.9x | -10% vitesse max |
| **CRITICAL** | 10-40% | 0.7x | -30% vitesse, contrôle réduit |
| **EXHAUSTED** | 0-10% | 0.5x | -50% vitesse, risque chute élevé |

---

### 4. **Configuration** (`config/game_config.py`)

**Paramètres d'endurance** :
```python
STAMINA_MAX = 100.0
STAMINA_BASE_DRAIN_RATE = 2.0
STAMINA_RECOVERY_RATE = 8.0
STAMINA_VELOCITY_MULTIPLIER = 0.015
STAMINA_SLOPE_MULTIPLIER = 2.5
STAMINA_FATIGUE_RECOVERY_PENALTY = 0.7

# Seuils zones
STAMINA_OPTIMAL_THRESHOLD = 70.0
STAMINA_MODERATE_THRESHOLD = 40.0
STAMINA_CRITICAL_THRESHOLD = 10.0

# Multiplicateurs
PERFORMANCE_OPTIMAL_SPEED_MULT = 1.0
PERFORMANCE_MODERATE_SPEED_MULT = 0.9
PERFORMANCE_CRITICAL_SPEED_MULT = 0.7
PERFORMANCE_EXHAUSTED_SPEED_MULT = 0.5
```

**Paramètres d'équilibre** :
```python
BALANCE_MAX = 100.0
BALANCE_RECOVERY_RATE = 25.0
BALANCE_CRITICAL_THRESHOLD = 20.0
BALANCE_CRASH_THRESHOLD = 5.0

# Facteurs d'instabilité
BALANCE_CAMBER_MULTIPLIER = 1.5
BALANCE_SPEED_MULTIPLIER = 0.8
BALANCE_LOW_STAMINA_MULTIPLIER = 1.8
BALANCE_TERRAIN_GRIP_FACTOR = 2.0
```

**Paramètres de fatigue** :
```python
FATIGUE_ACCUMULATION_RATE = 0.5
FATIGUE_MAX = 100.0
FATIGUE_RECOVERY_IN_CARRYING = 2.0
```

---

### 5. **Interface Utilisateur**

#### **GaugeWidget** (`ui/gauge_widget.py`)

Widget réutilisable pour afficher des jauges :

**Fonctionnalités** :
- Barre de progression horizontale
- Couleur dynamique selon valeur
- Label et pourcentage
- Effet de clignotement
- Mise en cache du rendu texte (optimisation)

**Méthodes** :
- `render(screen, frame_count)` - Affichage
- `set_value(value)` - Mise à jour valeur
- `set_color_by_percentage(percent, thresholds)` - Couleur automatique
- `set_blink_effect(enabled)` - Activer clignotement

#### **StaminaBalanceUI** (`ui/stamina_balance_ui.py`)

Gestionnaire d'interface complet :

**Jauges affichées** :
1. **Barre d'endurance** (20, 20) - 200x20px
   - Couleur selon zone de performance
   - Clignotement en zone critique/épuisée

2. **Barre d'équilibre** (20, 50) - 200x15px
   - Bleu (stable), Jaune (instable), Rouge (critique)
   - Clignotement rapide si proche de chute

3. **Barre de fatigue** (20, 75) - 150x10px
   - Vert à rouge selon accumulation

**Indicateurs contextuels** (coin supérieur droit) :
- Type de terrain avec pastille de couleur
- Grip (adhérence) en pourcentage
- Pente avec flèche indicatrice
- Dévers avec triangle d'avertissement
- Fond semi-transparent (alpha 180)

---

### 6. **Intégration Gameplay**

#### **CyclistWithStates** (`entities/cyclist_with_states.py`)

Modifications :
- Ajout de `StaminaComponent` et `BalanceComponent` dans `_setup_components()`
- Méthode `_apply_stamina_speed_modifier()` - Applique modificateur selon zone
- Méthodes d'accès : `get_stamina()`, `get_balance()`

#### **RidingState** (`systems/cyclist_states.py`)

Comportements ajoutés :
- **Enter** : Active drain d'endurance (`set_recovering(False)`)
- **Update** :
  - Vérifie équilibre : transition vers CRASHED si `should_crash()`
  - Si EXHAUSTED : applique instabilité supplémentaire (5.0/sec)

#### **CarryingState** (`systems/cyclist_states.py`)

Comportements ajoutés :
- **Enter** :
  - Active récupération d'endurance (`set_recovering(True)`)
  - Boost d'équilibre initial (+20 si < 50)
- **Exit** :
  - Désactive récupération (`set_recovering(False)`)

---

### 7. **Scène de Test** (`scenes/stamina_balance_test_scene.py`)

Scène complète de test avec :

**Contrôles de test** :
- `T` : Changer type de terrain
- `S` : Augmenter pente (+10°)
- `D` : Diminuer pente (-10°)
- `B` : Appliquer déséquilibre (-30 balance)
- `F` : Drainer endurance (-20 stamina)
- `R` : Reset stamina et balance

**Affichage** :
- Terrain avec grille 5x5
- Jauges complètes (stamina, balance, fatigue)
- Indicateurs contextuels
- Debug info (état, vitesse, zone, stabilité)
- Instructions à l'écran

**Terrain de test** :
- 6 types de terrain cyclables (asphalt, grass, sand, mud, gravel, dirt)
- Pente variable : -10° à +10°
- Camber variable : -6° à +6°

---

## 📊 Formules Documentées

### Drain d'Endurance
```
total_drain = base_drain
              * (1 + speed * 0.015)                    // velocity_factor
              * terrain_stamina_multiplier              // terrain
              * slope_multiplier                        // pente
              * (1 + fatigue/100 * 0.5)                // fatigue
              * delta_time
```

### Récupération d'Endurance
```
recovery = recovery_rate
           * (1 - fatigue/100 * 0.3)                   // fatigue_penalty
           * delta_time
```

### Instabilité Totale
```
instability = abs(camber) * 1.5                        // camber_factor
            + rotation_change * (speed/max_speed) * 0.8 * 100  // turn_factor
            + (1 - grip) * 2.0                         // grip_factor
            + exhaustion_factor * 1.8                   // (if stamina < 30%)
```

### Probabilité de Chute
```
if balance <= crash_threshold (5):
    crash = true
elif balance <= critical_threshold (20):
    probability = ((critical - balance) / (critical - crash)) * 0.3
    crash = random() < probability
else:
    crash = false
```

---

## 🎯 Critères de Validation

✅ **Fonctionnalités** :
- [x] L'endurance varie de manière réaliste et prévisible
- [x] Les zones de performance sont clairement perceptibles
- [x] L'équilibre rend les sections techniques challengeantes
- [x] Le joueur doit faire des choix stratégiques (porter vs pédaler)
- [x] Les valeurs sont facilement ajustables dans config
- [x] L'interface donne toute l'information sans surcharge
- [x] La fatigue cumulative force une gestion long terme

✅ **Code Quality** :
- [x] Type hints Python complets partout
- [x] Documentation des formules de calcul
- [x] Composants modulaires et réutilisables
- [x] Performance optimisée (mise en cache, pas d'allocation en update loop)

---

## 📁 Fichiers Créés/Modifiés

### Nouveaux fichiers
```
components/stamina_component.py        (313 lignes)
components/balance_component.py        (296 lignes)
ui/gauge_widget.py                     (270 lignes)
ui/stamina_balance_ui.py               (333 lignes)
ui/__init__.py                         (10 lignes)
scenes/stamina_balance_test_scene.py   (369 lignes)
INSTALLATION.md                        (169 lignes)
Documentation/PROMPT_6_SUMMARY.md      (ce fichier)
```

### Fichiers modifiés
```
config/constants.py                    (+7 lignes)  - PerformanceZone enum
config/game_config.py                  (+35 lignes) - Constantes stamina/balance
entities/cyclist_with_states.py       (+19 lignes) - Intégration composants
systems/cyclist_states.py              (+49 lignes) - Gestion states
main.py                                (+4 lignes)  - Enregistrement scène
.gitignore                             (+3 lignes)  - node_modules
```

**Total** : ~1800 lignes de code ajoutées

---

## 🎮 Gameplay Résultant

### Boucle de Gameplay
1. Le cycliste pédale (état RIDING)
2. L'endurance se draine selon vitesse, terrain, pente
3. La fatigue s'accumule progressivement
4. L'équilibre fluctue selon virages, camber, grip, endurance
5. Si équilibre critique → risque de chute (CRASHED)
6. Le joueur peut porter le vélo (CARRYING) pour récupérer
7. Zones de performance modifient la vitesse max en temps réel

### Décisions Stratégiques
- **Pédaler fort** : Progression rapide mais drain élevé
- **Pédaler modéré** : Équilibre drain/vitesse
- **Porter le vélo** : Récupération active mais lent
- **Gérer les virages** : Ralentir pour éviter la chute
- **Choisir le terrain** : Éviter les zones difficiles si fatigué

---

## 🔧 Équilibrage Actuel

Les valeurs actuelles sont un bon point de départ :

**Endurance** :
- Drain de base : 2.0/sec (modéré)
- Récupération : 8.0/sec (rapide en portage)
- Seuils de zones : 70%, 40%, 10% (équilibrés)

**Équilibre** :
- Récupération : 25.0/sec (rapide)
- Seuils : 20 (critique), 5 (chute)
- Multiplicateurs : permettent variété sans être punitifs

**Recommandations de tuning** :
- Tester sur parcours longs (5+ minutes)
- Ajuster selon retours joueurs
- Possibilité de profils de difficulté (facile/normal/difficile)

---

## 📈 Améliorations Futures Possibles

1. **Effets visuels** :
   - Shader de fatigue (écran assombri)
   - Wobble de caméra en zone instable
   - Particules de transpiration

2. **Audio** :
   - Sons de respiration selon zone
   - Heartbeat rapide en épuisement
   - Son d'alerte en équilibre critique

3. **Mécaniques avancées** :
   - Boost temporaire (consomme beaucoup d'endurance)
   - Drafting (récupération derrière adversaire)
   - Nutrition (items pour récupérer)

4. **IA** :
   - NPCs qui gèrent aussi leur endurance
   - Stratégies adaptatives selon fatigue

5. **Multijoueur** :
   - Affichage jauges adversaires
   - Comparaison performance en temps réel

---

## 🎓 Concepts Démontrés

### Design Patterns
- **Component Pattern** : StaminaComponent, BalanceComponent
- **State Pattern** : Intégration avec états existants
- **Observer Pattern** : UI observe les composants
- **Strategy Pattern** : Calculs contextuels dynamiques

### Game Design
- **Resource Management** : Endurance comme ressource limitée
- **Risk/Reward** : Vitesse vs sécurité
- **Feedback Loops** : Fatigue → récupération réduite
- **Player Agency** : Choix tactiques constants

### Ingénierie Logicielle
- **Type Safety** : Type hints complets
- **Performance** : Cache, optimisations
- **Modularity** : Composants découplés
- **Configuration** : Paramètres externalisés

---

## ✨ Conclusion

Le système d'endurance et d'équilibre est **complet, fonctionnel et prêt pour le gameplay**.

L'architecture est :
- ✅ **Modulaire** : Composants indépendants
- ✅ **Performante** : Optimisations en place
- ✅ **Évolutive** : Facile d'ajouter des mécaniques
- ✅ **Configurable** : Paramètres ajustables
- ✅ **Testable** : Scène de test complète

**Le jeu est maintenant prêt pour le prochain prompt !**

---

**Auteur** : Claude Code
**Date** : 2025-11-10
**Prompt** : 6/N
**Statut** : ✅ Implémenté et testé
