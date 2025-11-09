import { TerrainType } from '@/types/enums';
import type { TerrainData, CyclistStats } from '@/types/gameData';

/**
 * Constantes globales du jeu de cyclo-cross.
 * Centralise toutes les valeurs de configuration pour faciliter l'équilibrage.
 */

// ============================================================================
// CONFIGURATION DU JEU
// ============================================================================

/** Largeur du canvas en pixels */
export const GAME_WIDTH = 1280;

/** Hauteur du canvas en pixels */
export const GAME_HEIGHT = 720;

/** FPS cible */
export const TARGET_FPS = 60;

/** Couleur de fond (ciel bleu) */
export const BACKGROUND_COLOR = '#87CEEB';

// ============================================================================
// CONFIGURATION DE LA COURSE
// ============================================================================

/** Longueur totale d'un tour de parcours (pixels) */
export const TRACK_LENGTH = 10000;

/** Nombre de tours par défaut */
export const DEFAULT_LAPS = 3;

/** Position Y de la ligne de course (sol) */
export const GROUND_Y = 600;

/** Largeur de la piste */
export const TRACK_WIDTH = 200;

// ============================================================================
// STATISTIQUES DU JOUEUR
// ============================================================================

export const PLAYER_STATS: CyclistStats = {
  maxSpeed: 400,                  // pixels/seconde
  acceleration: 200,               // pixels/seconde²
  maxStamina: 100,                // points
  staminaRecoveryRate: 10,        // points/seconde
  balance: 80,                     // sur 100
  jumpPower: 150,                  // pixels
  sprintMultiplier: 1.5,          // multiplicateur de vitesse
};

// ============================================================================
// CONFIGURATION DES TERRAINS
// ============================================================================

export const TERRAIN_CONFIG: Record<TerrainType, TerrainData> = {
  [TerrainType.ASPHALT]: {
    type: TerrainType.ASPHALT,
    speedMultiplier: 1.0,
    staminaDrain: 5,
    color: '#404040',
    affectsBalance: false,
  },
  [TerrainType.GRASS]: {
    type: TerrainType.GRASS,
    speedMultiplier: 0.85,
    staminaDrain: 8,
    color: '#4CAF50',
    affectsBalance: false,
  },
  [TerrainType.MUD]: {
    type: TerrainType.MUD,
    speedMultiplier: 0.6,
    staminaDrain: 15,
    color: '#8B4513',
    affectsBalance: true,
  },
  [TerrainType.SAND]: {
    type: TerrainType.SAND,
    speedMultiplier: 0.5,
    staminaDrain: 20,
    color: '#F4A460',
    affectsBalance: true,
  },
  [TerrainType.GRAVEL]: {
    type: TerrainType.GRAVEL,
    speedMultiplier: 0.75,
    staminaDrain: 12,
    color: '#A9A9A9',
    affectsBalance: true,
  },
};

// ============================================================================
// PHYSIQUE
// ============================================================================

/** Gravité pour les sauts (pixels/seconde²) */
export const GRAVITY = 800;

/** Friction de base */
export const BASE_FRICTION = 0.98;

/** Vitesse minimale avant arrêt complet */
export const MIN_SPEED_THRESHOLD = 0.1;

// ============================================================================
// INTERFACE UTILISATEUR
// ============================================================================

/** Taille de la police pour les FPS */
export const FPS_FONT_SIZE = '18px';

/** Couleur du texte des FPS */
export const FPS_COLOR = '#00ff00';

/** Position X du texte des FPS */
export const FPS_X = 10;

/** Position Y du texte des FPS */
export const FPS_Y = 30;

// ============================================================================
// CONTRÔLES
// ============================================================================

/** Touches de contrôle du joueur */
export const CONTROLS = {
  ACCELERATE: 'UP',
  BRAKE: 'DOWN',
  JUMP: 'SPACE',
  SPRINT: 'SHIFT',
} as const;

// ============================================================================
// PHYSIQUE DU MOUVEMENT (Arcade Physics)
// ============================================================================

/**
 * Paramètres physiques du cycliste.
 * Toutes les valeurs sont en pixels et secondes.
 */

/** Accélération avant (pixels/seconde²) */
export const CYCLIST_ACCELERATION = 300;

/** Accélération de freinage (pixels/seconde²) */
export const CYCLIST_BRAKE_ACCELERATION = 500;

/** Vitesse maximale normale (pixels/seconde) */
export const CYCLIST_MAX_SPEED = 400;

/** Vitesse maximale en sprint (pixels/seconde) */
export const CYCLIST_SPRINT_MAX_SPEED = 600;

/** Drag (résistance) - réduit la vitesse progressivement (0-1, plus c'est haut plus ça freine) */
export const CYCLIST_DRAG = 0.05;

/** Masse du cycliste + vélo (affecte l'inertie) */
export const CYCLIST_MASS = 1;

/** Bounce (rebond) lors des collisions (0-1) */
export const CYCLIST_BOUNCE = 0.2;

/** Vitesse de rotation (degrés/seconde) à basse vitesse */
export const CYCLIST_ROTATION_SPEED_LOW = 180;

/** Vitesse de rotation (degrés/seconde) à haute vitesse */
export const CYCLIST_ROTATION_SPEED_HIGH = 90;

/** Seuil de vitesse pour rotation rapide vs lente (pixels/seconde) */
export const CYCLIST_ROTATION_SPEED_THRESHOLD = 200;

/** Facteur d'interpolation pour la rotation (0-1, plus c'est bas plus c'est lisse) */
export const CYCLIST_ROTATION_LERP = 0.1;

// ============================================================================
// DIMENSIONS DES ENTITÉS
// ============================================================================

/** Largeur du cycliste */
export const CYCLIST_WIDTH = 40;

/** Hauteur du cycliste */
export const CYCLIST_HEIGHT = 60;

/** Rayon de collision du cycliste */
export const CYCLIST_COLLISION_RADIUS = 20;

// ============================================================================
// PARAMÈTRES DE LA CAMÉRA
// ============================================================================

/** Décalage de la caméra par rapport au joueur (X) */
export const CAMERA_OFFSET_X = -400;

/** Décalage de la caméra par rapport au joueur (Y) */
export const CAMERA_OFFSET_Y = -200;

/** Vitesse de suivi de la caméra (lerp factor) */
export const CAMERA_LERP = 0.1;

// ============================================================================
// SYSTÈME D'ENDURANCE
// ============================================================================

/** Endurance maximale */
export const ENDURANCE_MAX = 100;

/** Endurance initiale au démarrage */
export const ENDURANCE_INITIAL = 100;

/** Taux de dégradation de base (points/seconde) pendant l'effort */
export const ENDURANCE_DRAIN_RATE_BASE = 5;

/** Taux de dégradation pendant l'accélération (points/seconde) */
export const ENDURANCE_DRAIN_RATE_ACCELERATE = 8;

/** Taux de dégradation pendant le sprint (points/seconde) */
export const ENDURANCE_DRAIN_RATE_SPRINT = 15;

/** Taux de récupération au repos (points/seconde) */
export const ENDURANCE_RECOVERY_RATE = 10;

/** Seuil de vitesse pour considérer le cycliste au repos (pixels/seconde) */
export const ENDURANCE_REST_SPEED_THRESHOLD = 10;

/** Durée minimale d'un boost de sprint (ms) */
export const ENDURANCE_SPRINT_MIN_DURATION = 1000;

/** Coût d'activation d'un sprint (points) */
export const ENDURANCE_SPRINT_ACTIVATION_COST = 5;

/** Seuil zone verte (> 60% = performance optimale) */
export const ENDURANCE_ZONE_GREEN_THRESHOLD = 0.6;

/** Seuil zone jaune (30-60% = performance réduite) */
export const ENDURANCE_ZONE_YELLOW_THRESHOLD = 0.3;

/** Seuil zone rouge (< 30% = performance très réduite) */
export const ENDURANCE_ZONE_RED_THRESHOLD = 0.0;

/** Multiplicateur de vitesse max en zone verte */
export const ENDURANCE_SPEED_MULTIPLIER_GREEN = 1.0;

/** Multiplicateur de vitesse max en zone jaune */
export const ENDURANCE_SPEED_MULTIPLIER_YELLOW = 0.8;

/** Multiplicateur de vitesse max en zone rouge */
export const ENDURANCE_SPEED_MULTIPLIER_RED = 0.5;

/** Couleurs des zones d'endurance */
export const ENDURANCE_ZONE_COLORS = {
  GREEN: '#4CAF50',   // Vert
  YELLOW: '#FFC107',  // Jaune
  RED: '#F44336',     // Rouge
} as const;

// ============================================================================
// SYSTÈME D'ÉQUILIBRE
// ============================================================================

/** Valeur minimale d'équilibre */
export const BALANCE_MIN = -100;

/** Valeur maximale d'équilibre */
export const BALANCE_MAX = 100;

/** Valeur initiale d'équilibre (parfaitement centré) */
export const BALANCE_INITIAL = 0;

/** Taux de récupération automatique vers l'équilibre (points/seconde) */
export const BALANCE_RECOVERY_RATE = 20;

/** Seuil pour considérer l'équilibre comme critique (valeur absolue) */
export const BALANCE_CRITICAL_THRESHOLD = 80;

/** Seuil pour déclencher une chute (valeur absolue) */
export const BALANCE_FALL_THRESHOLD = 95;

/** Durée minimale entre deux perturbations d'équilibre (ms) */
export const BALANCE_PERTURBATION_COOLDOWN = 500;

/** Magnitude de perturbation pour un obstacle (points) */
export const BALANCE_PERTURBATION_OBSTACLE = 30;

/** Magnitude de perturbation pour un virage serré (points) */
export const BALANCE_PERTURBATION_SHARP_TURN = 20;

/** Magnitude de perturbation pour terrain difficile (points) */
export const BALANCE_PERTURBATION_TERRAIN = 15;

/** Magnitude de perturbation pour collision (points) */
export const BALANCE_PERTURBATION_COLLISION = 40;

/** Magnitude de perturbation pour atterrissage (points) */
export const BALANCE_PERTURBATION_LANDING = 25;

/** Seuils des niveaux d'équilibre (valeur absolue) */
export const BALANCE_LEVEL_BALANCED_THRESHOLD = 20;
export const BALANCE_LEVEL_SLIGHTLY_THRESHOLD = 50;
export const BALANCE_LEVEL_VERY_THRESHOLD = 80;

/** Intensité de l'oscillation visuelle selon le niveau (0-1) */
export const BALANCE_OSCILLATION_INTENSITY = {
  BALANCED: 0,
  SLIGHTLY: 0.3,
  VERY: 0.6,
  CRITICAL: 1.0,
} as const;

/** Vitesse angulaire de l'oscillation (radians/seconde) */
export const BALANCE_OSCILLATION_SPEED = 5;

/** Couleurs des niveaux d'équilibre */
export const BALANCE_LEVEL_COLORS = {
  BALANCED: '#4CAF50',       // Vert
  SLIGHTLY: '#FFC107',       // Jaune
  VERY: '#FF9800',           // Orange
  CRITICAL: '#F44336',       // Rouge
} as const;

// ============================================================================
// INTERFACE UTILISATEUR - BARRES
// ============================================================================

/** Largeur des barres d'endurance et d'équilibre */
export const UI_BAR_WIDTH = 200;

/** Hauteur des barres */
export const UI_BAR_HEIGHT = 20;

/** Espacement entre les barres */
export const UI_BAR_SPACING = 10;

/** Position X des barres (depuis le bord gauche) */
export const UI_BAR_X = 20;

/** Position Y de la première barre (depuis le haut) */
export const UI_BAR_Y = 60;

/** Épaisseur du contour des barres */
export const UI_BAR_BORDER_WIDTH = 2;

/** Couleur du contour des barres */
export const UI_BAR_BORDER_COLOR = 0xFFFFFF;

/** Couleur de fond des barres */
export const UI_BAR_BACKGROUND_COLOR = 0x333333;

/** Opacité du fond des barres (0-1) */
export const UI_BAR_BACKGROUND_ALPHA = 0.8;

// ============================================================================
// DÉVELOPPEMENT
// ============================================================================

/** Activer le mode debug (affichage des informations de débogage) */
export const DEBUG_MODE = true;

/** Afficher les FPS */
export const SHOW_FPS = true;

/** Afficher les collisions */
export const SHOW_COLLISIONS = false;
