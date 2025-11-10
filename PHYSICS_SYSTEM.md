# Système de Physique - Documentation

## Vue d'ensemble

Le système de physique implémente une simulation newtonienne réaliste pour le mouvement des cyclistes. Il est construit selon l'architecture Entity-Component et sépare clairement les responsabilités.

## Composants implémentés

### 1. TransformComponent

**Responsabilité** : Gestion de la position, rotation et échelle dans l'espace 2D.

**Propriétés** :
- `position` : Vector2 - Position dans le monde
- `rotation` : float - Angle en radians (normalisé entre -π et π)
- `scale` : Vector2 - Échelle de l'entité

**Méthodes principales** :
```python
translate(delta: Vector2)              # Déplace l'entité
rotate(angle: float)                   # Tourne l'entité (radians)
look_at(target: Vector2)               # Oriente vers une cible
get_forward_vector() -> Vector2        # Retourne la direction avant
local_to_world(pos) -> Vector2         # Conversion d'espace
world_to_local(pos) -> Vector2         # Conversion d'espace
```

**Exemple d'utilisation** :
```python
transform = entity.add_component(TransformComponent, Vector2(100, 100))
transform.rotate(math.pi / 4)  # Tourne de 45°
forward = transform.get_forward_vector()  # Direction avant
```

### 2. PhysicsComponent

**Responsabilité** : Simulation physique newtonienne avec forces, vélocité et accélération.

**Propriétés** :
- `mass` : float - Masse en kg
- `drag` : float - Coefficient de traînée (0-1)
- `max_speed` : float - Vitesse maximale en pixels/seconde
- `velocity` : Vector2 - Vélocité actuelle
- `acceleration` : Vector2 - Accélération actuelle

**Équations physiques** :
```
F = ma              → a = F/m
v = v0 + at         (Intégration d'Euler)
p = p0 + vt
drag: v *= pow(drag, dt*60)
```

**Méthodes principales** :
```python
apply_force(force: Vector2)           # Applique une force (accumulée)
apply_impulse(impulse: Vector2)       # Applique une impulsion instantanée
set_velocity(velocity: Vector2)       # Définit la vélocité directement
stop()                                # Arrête tout mouvement
get_speed() -> float                  # Retourne la magnitude de vélocité
get_kinetic_energy() -> float         # E = 1/2 × m × v²
get_momentum() -> Vector2             # p = m × v
```

**Paramètres configurables** :
```python
CYCLIST_MASS = 75.0              # kg (cycliste + vélo)
CYCLIST_DRAG = 0.97              # Plus proche de 1 = moins de résistance
CYCLIST_MAX_SPEED = 400.0        # pixels/seconde
```

**Exemple d'utilisation** :
```python
physics = entity.add_component(PhysicsComponent, mass=75.0, drag=0.97, max_speed=400.0)
physics.apply_force(Vector2(100, 0))  # Force vers la droite
# Dans update(delta_time), la physique est automatiquement calculée
```

### 3. InputComponent

**Responsabilité** : Conversion des entrées clavier en forces physiques appliquées au cycliste.

**Modes de contrôle** :
1. **Tank mode** (par défaut) : Rotation indépendante du mouvement
2. **Auto-orient mode** : Rotation automatique vers la direction du mouvement

**Paramètres** :
- `acceleration_force` : Force d'accélération (N)
- `brake_force` : Force de freinage (N)
- `turn_speed_slow` : Vitesse de rotation à basse vitesse (rad/s)
- `turn_speed_fast` : Vitesse de rotation à haute vitesse (rad/s)
- `speed_threshold` : Seuil de transition entre rotation lente/rapide

**Touches par défaut** :
- Flèches / WASD : Direction
- Haut/W : Accélérer
- Bas/S : Freiner/reculer
- Gauche/A : Tourner à gauche
- Droite/D : Tourner à droite

**Rayon de braquage réaliste** :
À basse vitesse → rotation rapide (maniable)
À haute vitesse → rotation lente (grand rayon de braquage)

```python
# Interpolation de la vitesse de rotation
speed_ratio = current_speed / speed_threshold
turn_speed = turn_speed_slow + (turn_speed_fast - turn_speed_slow) * speed_ratio
```

**Exemple d'utilisation** :
```python
input_comp = entity.add_component(
    InputComponent,
    acceleration_force=600.0,
    brake_force=1000.0,
    turn_speed_slow=4.0,
    turn_speed_fast=1.5
)
input_comp.set_control_mode_auto_orient()  # Change le mode
```

### 4. SpriteRendererComponent

**Responsabilité** : Rendu visuel avec support de la rotation.

**Fonctionnalités** :
- Rendu de rectangles colorés ou sprites
- Rotation automatique basée sur TransformComponent
- Flèche directionnelle par défaut
- Support de transparence (alpha)

**Paramètres** :
- `width`, `height` : Dimensions du sprite
- `color` : Couleur si mode rectangle
- `sprite_path` : Chemin vers image (optionnel)
- `use_rotation` : Active/désactive la rotation
- `draw_direction_arrow` : Dessine une flèche de direction

**Optimisation** :
- Utilise `pygame.transform.rotate()` pour la rotation
- Le sprite est centré sur la position de l'entité
- Support de l'alpha pour la transparence

**Exemple d'utilisation** :
```python
renderer = entity.add_component(
    SpriteRendererComponent,
    width=40,
    height=60,
    color=Colors.CYAN,
    use_rotation=True
)
# Dans la boucle de rendu
renderer.render(screen)
```

## Classe Cyclist

**Responsabilité** : Entité prête à l'emploi combinant tous les composants.

**Composants inclus** :
1. TransformComponent
2. PhysicsComponent
3. InputComponent (si `is_player=True`)

**Méthodes helper** :
```python
get_transform() -> TransformComponent
get_physics() -> PhysicsComponent
get_input() -> InputComponent | None
get_speed() -> float
get_direction() -> Vector2
stop()
apply_force(force: Vector2)
```

**Exemple d'utilisation** :
```python
# Créer un cycliste joueur
player = Cyclist("Player", Vector2(640, 360), is_player=True)
player.add_component(SpriteRendererComponent, 40, 60, Colors.CYAN)

# Créer un cycliste IA
ai = Cyclist("AI1", Vector2(100, 100), is_player=False)
# L'IA n'a pas d'InputComponent, contrôlez-le manuellement
ai.apply_force(Vector2(100, 0))
```

## Paramètres physiques

Tous les paramètres sont centralisés dans `config/game_config.py` :

```python
# Paramètres physiques du cycliste
CYCLIST_MASS: float = 75.0                    # Masse (kg)
CYCLIST_DRAG: float = 0.97                    # Traînée (0-1)
CYCLIST_MAX_SPEED: float = 400.0              # Vitesse max (px/s)

# Paramètres de contrôle
CYCLIST_ACCELERATION_FORCE: float = 600.0     # Force accélération (N)
CYCLIST_BRAKE_FORCE: float = 1000.0           # Force freinage (N)
CYCLIST_TURN_SPEED_SLOW: float = 4.0          # Rotation lente (rad/s)
CYCLIST_TURN_SPEED_FAST: float = 1.5          # Rotation rapide (rad/s)
CYCLIST_SPEED_THRESHOLD: float = 150.0        # Seuil transition (px/s)
```

### Ajuster le feeling du jeu

**Pour plus de réactivité** :
- Augmenter `CYCLIST_ACCELERATION_FORCE`
- Augmenter `CYCLIST_TURN_SPEED_SLOW`
- Diminuer `CYCLIST_MASS`

**Pour plus d'inertie** :
- Diminuer `CYCLIST_DRAG` (plus proche de 1 = moins d'inertie)
- Augmenter `CYCLIST_MASS`
- Diminuer `CYCLIST_BRAKE_FORCE`

**Pour plus de vitesse** :
- Augmenter `CYCLIST_MAX_SPEED`
- Augmenter `CYCLIST_ACCELERATION_FORCE`

**Pour un rayon de braquage plus large** :
- Diminuer `CYCLIST_TURN_SPEED_FAST`
- Augmenter `CYCLIST_SPEED_THRESHOLD`

## Flux de données

```
1. Input (clavier)
   ↓
2. InputComponent.update()
   - Lit pygame.key.get_pressed()
   - Calcule forces selon direction
   - Applique forces à PhysicsComponent
   ↓
3. PhysicsComponent.update(delta_time)
   - Accumule forces : F_total
   - Calcule accélération : a = F/m
   - Met à jour vélocité : v = v0 + at
   - Applique drag : v *= drag^(dt*60)
   - Limite vitesse max
   - Met à jour position : p = p0 + vt
   - Réinitialise forces
   ↓
4. TransformComponent.update()
   - Synchronise position avec entité
   - Synchronise rotation
   ↓
5. SpriteRendererComponent.render(screen)
   - Lit position/rotation depuis TransformComponent
   - Applique rotation au sprite
   - Dessine à l'écran
```

## Intégration d'Euler

Le système utilise l'**intégration d'Euler** pour sa simplicité :

```python
# Mise à jour de la vélocité
velocity = velocity + acceleration * delta_time

# Mise à jour de la position
position = position + velocity * delta_time
```

**Avantages** :
- Simple à implémenter
- Performant
- Suffisant pour un jeu 2D

**Limitations** :
- Peut être instable avec de très grandes forces
- Moins précis que Verlet ou RK4
- Solution : limiter `delta_time` avec `DELTA_TIME_MAX`

## Formules physiques utilisées

### Force et accélération
```
F = ma
a = F / m
```

### Vélocité
```
v(t) = v₀ + at
```

### Position
```
p(t) = p₀ + vt
```

### Drag (résistance)
```
v = v × drag^(dt × 60)
```
Normalisé à 60 FPS pour cohérence.

### Énergie cinétique
```
E = ½mv²
```

### Momentum
```
p = mv
```

## Scène de test

La scène `PhysicsTestScene` démontre :
- Cycliste contrôlable au centre
- Marqueurs de référence aux coins
- Ligne de départ
- HUD avec statistiques en temps réel :
  - Position
  - Vitesse (absolute et pourcentage)
  - Rotation
  - Vélocité
- Jauge de vitesse visuelle
- Instructions à l'écran

**Touches spéciales** :
- R : Reset position
- ESPACE : Affiche stats dans console
- ESC : Quitter

## Validation des critères

### Mouvement fluide ✓
- 60 FPS constant grâce au delta time
- Pas de saccades

### Inertie perceptible ✓
- Accélération progressive
- Pas d'arrêt instantané
- Drag appliqué continuellement

### Rotation réaliste ✓
- Dépend de la vitesse (rayon de braquage)
- Interpolation douce
- Angle normalisé

### Freinage graduel ✓
- Force opposée à la vélocité
- Proportionnel à la vitesse actuelle

### Réponse intuitive ✓
- Contrôles immédiats
- Prévisibles
- Ajustables via config

### Paramètres ajustables ✓
- Tous centralisés dans GameConfig
- Modifications sans recompilation
- Commentés et documentés

### Séparation physique/rendu ✓
- PhysicsComponent : logique
- SpriteRendererComponent : visuel
- TransformComponent : transformation

### Type hints complets ✓
- Tous les fichiers typés
- Pas de `Any`
- Compatible mypy

## Prochaines étapes (Prompt 3+)

Le système de physique est maintenant prêt pour :
- Command Pattern (Prompt 3) : Enregistrement et replay
- Terrains (Prompt 4) : Modificateurs de friction et vitesse
- États (Prompt 5) : RIDING, CARRYING, etc.
- Collisions (Prompt 7) : Obstacles et limites
- IA (Prompt 9) : Forces appliquées par stratégies

## Références

- **Intégration d'Euler** : https://en.wikipedia.org/wiki/Euler_method
- **Game Physics** : "Game Physics Engine Development" par Ian Millington
- **Pygame** : https://www.pygame.org/docs/ref/transform.html
