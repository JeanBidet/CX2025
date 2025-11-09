import { TerrainType, ObstacleType, AIDifficulty } from './enums';

/**
 * Statistiques d'un cycliste.
 * Définit les capacités de base d'un coureur.
 */
export interface CyclistStats {
  /** Vitesse maximale (pixels/seconde) */
  maxSpeed: number;

  /** Accélération (pixels/seconde²) */
  acceleration: number;

  /** Endurance maximale (0-100) */
  maxStamina: number;

  /** Vitesse de récupération de l'endurance (points/seconde) */
  staminaRecoveryRate: number;

  /** Capacité d'équilibre (0-100) - affecte la résistance aux chutes */
  balance: number;

  /** Force de saut (pixels) */
  jumpPower: number;

  /** Vitesse de sprint (multiplicateur de maxSpeed) */
  sprintMultiplier: number;
}

/**
 * Données de configuration d'un terrain.
 */
export interface TerrainData {
  /** Type de terrain */
  type: TerrainType;

  /** Multiplicateur de vitesse (0-1) */
  speedMultiplier: number;

  /** Consommation d'endurance par seconde */
  staminaDrain: number;

  /** Couleur pour le rendu (format hex) */
  color: string;

  /** Affecte l'équilibre (true = terrain instable) */
  affectsBalance: boolean;
}

/**
 * Données d'un obstacle.
 */
export interface ObstacleData {
  /** Type d'obstacle */
  type: ObstacleType;

  /** Position X dans le monde */
  x: number;

  /** Position Y dans le monde */
  y: number;

  /** Largeur de l'obstacle */
  width: number;

  /** Hauteur de l'obstacle */
  height: number;

  /** Peut être sauté (true) ou nécessite portage (false) */
  jumpable: boolean;

  /** Vitesse minimale requise pour sauter (si jumpable) */
  minJumpSpeed?: number;
}

/**
 * Configuration d'un adversaire IA.
 */
export interface AIConfig {
  /** Nom de l'adversaire */
  name: string;

  /** Difficulté de l'IA */
  difficulty: AIDifficulty;

  /** Statistiques du cycliste IA */
  stats: CyclistStats;

  /** Couleur du maillot (format hex) */
  jerseyColor: string;

  /** Position de départ */
  startPosition: number;
}

/**
 * Résultat de course d'un cycliste.
 */
export interface RaceResult {
  /** Nom du cycliste */
  name: string;

  /** Temps total (millisecondes) */
  time: number;

  /** Position finale (1 = premier) */
  position: number;

  /** Est-ce le joueur ? */
  isPlayer: boolean;
}

/**
 * Configuration globale d'une course.
 */
export interface RaceConfig {
  /** Longueur totale du parcours (pixels) */
  trackLength: number;

  /** Nombre de tours */
  laps: number;

  /** Configuration des adversaires IA */
  opponents: AIConfig[];

  /** Distribution des terrains sur le parcours */
  terrainDistribution: TerrainType[];

  /** Liste des obstacles sur le parcours */
  obstacles: ObstacleData[];
}
