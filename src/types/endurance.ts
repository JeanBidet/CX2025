/**
 * Types et interfaces pour le système d'endurance.
 * L'endurance représente la capacité du cycliste à maintenir son effort.
 */

/**
 * État d'endurance du cycliste.
 */
export interface EnduranceState {
  /** Valeur actuelle d'endurance (0-100) */
  current: number;

  /** Valeur maximale d'endurance (généralement 100) */
  max: number;

  /** Taux de dégradation actuel (points/seconde) */
  drainRate: number;

  /** Taux de récupération actuel (points/seconde) */
  recoveryRate: number;

  /** Indique si le cycliste est épuisé (endurance <= 0) */
  isExhausted: boolean;

  /** Indique si le cycliste est en récupération */
  isRecovering: boolean;
}

/**
 * Zones d'endurance avec codes couleur.
 */
export enum EnduranceZone {
  /** Zone verte: > 60% - Performance optimale */
  GREEN = 'GREEN',

  /** Zone jaune: 30-60% - Performance réduite */
  YELLOW = 'YELLOW',

  /** Zone rouge: < 30% - Performance très réduite */
  RED = 'RED',
}

/**
 * Configuration des zones d'endurance.
 */
export interface EnduranceZoneConfig {
  /** Seuil minimal pour cette zone (pourcentage 0-1) */
  threshold: number;

  /** Couleur associée (hex) */
  color: string;

  /** Multiplicateur de vitesse max */
  speedMultiplier: number;
}

/**
 * Événements liés à l'endurance.
 */
export enum EnduranceEventType {
  /** Endurance modifiée */
  CHANGED = 'endurance:changed',

  /** Zone d'endurance changée */
  ZONE_CHANGED = 'endurance:zone_changed',

  /** Cycliste épuisé */
  EXHAUSTED = 'endurance:exhausted',

  /** Récupération commencée */
  RECOVERY_STARTED = 'endurance:recovery_started',

  /** Récupération terminée */
  RECOVERY_COMPLETED = 'endurance:recovery_completed',

  /** Sprint activé */
  SPRINT_ACTIVATED = 'endurance:sprint_activated',

  /** Sprint désactivé */
  SPRINT_DEACTIVATED = 'endurance:sprint_deactivated',
}

/**
 * Payload pour les événements d'endurance.
 */
export interface EnduranceEventPayload {
  /** État actuel de l'endurance */
  state: EnduranceState;

  /** Zone actuelle */
  zone?: EnduranceZone;

  /** Zone précédente (pour ZONE_CHANGED) */
  previousZone?: EnduranceZone;
}
