/**
 * Types et interfaces pour le système d'équilibre.
 * L'équilibre représente la stabilité du cycliste sur le vélo.
 */

/**
 * État d'équilibre du cycliste.
 */
export interface BalanceState {
  /** Valeur actuelle d'équilibre (-100 à +100, 0 = parfaitement équilibré) */
  current: number;

  /** Valeur minimale (généralement -100) */
  min: number;

  /** Valeur maximale (généralement +100) */
  max: number;

  /** Taux de récupération vers l'équilibre (points/seconde) */
  recoveryRate: number;

  /** Indique si le cycliste est déséquilibré au point de tomber */
  isFalling: boolean;

  /** Direction du déséquilibre (-1 = gauche, 0 = centré, +1 = droite) */
  direction: number;
}

/**
 * Niveaux de déséquilibre.
 */
export enum BalanceLevel {
  /** Équilibré: -20 à +20 */
  BALANCED = 'BALANCED',

  /** Légèrement déséquilibré: 20-50 ou -20 à -50 */
  SLIGHTLY_UNBALANCED = 'SLIGHTLY_UNBALANCED',

  /** Très déséquilibré: 50-80 ou -50 à -80 */
  VERY_UNBALANCED = 'VERY_UNBALANCED',

  /** Critique: > 80 ou < -80 (risque de chute) */
  CRITICAL = 'CRITICAL',
}

/**
 * Configuration des niveaux d'équilibre.
 */
export interface BalanceLevelConfig {
  /** Seuil minimal (valeur absolue) */
  threshold: number;

  /** Couleur de l'indicateur visuel */
  color: string;

  /** Intensité de l'oscillation visuelle (0-1) */
  oscillationIntensity: number;

  /** Vitesse de récupération modifiée */
  recoveryModifier: number;
}

/**
 * Types de perturbations d'équilibre.
 */
export enum BalancePerturbationType {
  /** Obstacle frappé */
  OBSTACLE = 'OBSTACLE',

  /** Virage serré à haute vitesse */
  SHARP_TURN = 'SHARP_TURN',

  /** Terrain difficile (boue, sable) */
  DIFFICULT_TERRAIN = 'DIFFICULT_TERRAIN',

  /** Collision avec autre cycliste */
  COLLISION = 'COLLISION',

  /** Atterrissage après saut */
  LANDING = 'LANDING',
}

/**
 * Configuration d'une perturbation d'équilibre.
 */
export interface BalancePerturbation {
  /** Type de perturbation */
  type: BalancePerturbationType;

  /** Magnitude de la perturbation (-100 à +100) */
  magnitude: number;

  /** Durée de la perturbation (ms) */
  duration?: number;

  /** Direction de la perturbation (-1 = gauche, +1 = droite, 0 = aléatoire) */
  direction?: number;
}

/**
 * Événements liés à l'équilibre.
 */
export enum BalanceEventType {
  /** Équilibre modifié */
  CHANGED = 'balance:changed',

  /** Niveau d'équilibre changé */
  LEVEL_CHANGED = 'balance:level_changed',

  /** Perturbation appliquée */
  PERTURBED = 'balance:perturbed',

  /** Équilibre critique (risque de chute) */
  CRITICAL = 'balance:critical',

  /** Chute déclenchée */
  FALLING = 'balance:falling',

  /** Équilibre récupéré */
  RECOVERED = 'balance:recovered',
}

/**
 * Payload pour les événements d'équilibre.
 */
export interface BalanceEventPayload {
  /** État actuel de l'équilibre */
  state: BalanceState;

  /** Niveau actuel */
  level?: BalanceLevel;

  /** Niveau précédent (pour LEVEL_CHANGED) */
  previousLevel?: BalanceLevel;

  /** Perturbation appliquée (pour PERTURBED) */
  perturbation?: BalancePerturbation;
}
