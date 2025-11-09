/**
 * Types de terrain dans le jeu de cyclo-cross.
 * Chaque terrain affecte différemment la vitesse et l'endurance.
 */
export enum TerrainType {
  /** Asphalte - Terrain rapide et facile */
  ASPHALT = 'ASPHALT',

  /** Herbe - Terrain modéré, réduit légèrement la vitesse */
  GRASS = 'GRASS',

  /** Boue - Terrain difficile, réduit fortement la vitesse et augmente la consommation d'endurance */
  MUD = 'MUD',

  /** Sable - Terrain très difficile, glissant et épuisant */
  SAND = 'SAND',

  /** Gravier - Terrain instable, affecte l'équilibre */
  GRAVEL = 'GRAVEL',
}

/**
 * États possibles pour un cycliste.
 * Utilisé avec le pattern State.
 */
export enum CyclistState {
  /** En train de pédaler normalement */
  RIDING = 'riding',

  /** En train de sprinter (vitesse maximale, consommation d'endurance élevée) */
  SPRINTING = 'sprinting',

  /** Portage du vélo (obstacles non cyclables) */
  CARRYING = 'carrying',

  /** Chute ou perte d'équilibre */
  FALLEN = 'fallen',

  /** Récupération d'endurance */
  RECOVERING = 'recovering',

  /** Course terminée */
  FINISHED = 'finished',
}

/**
 * Types d'obstacles sur le parcours.
 */
export enum ObstacleType {
  /** Haie basse - peut être sautée */
  LOW_BARRIER = 'low_barrier',

  /** Haie haute - nécessite portage du vélo */
  HIGH_BARRIER = 'high_barrier',

  /** Escaliers - nécessite portage */
  STAIRS = 'stairs',

  /** Tronc d'arbre - peut être sauté ou porté */
  LOG = 'log',

  /** Flaque de boue profonde */
  DEEP_MUD = 'deep_mud',
}

/**
 * Difficulté de l'IA.
 */
export enum AIDifficulty {
  /** IA facile - fait plus d'erreurs, moins rapide */
  EASY = 'easy',

  /** IA normale - équilibrée */
  NORMAL = 'normal',

  /** IA difficile - très compétitive, peu d'erreurs */
  HARD = 'hard',
}

/**
 * Types de commandes pour le pattern Command.
 */
export enum CommandType {
  ACCELERATE = 'accelerate',
  BRAKE = 'brake',
  JUMP = 'jump',
  CARRY_BIKE = 'carry_bike',
  SPRINT = 'sprint',
}
