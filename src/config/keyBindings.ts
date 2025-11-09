import Phaser from 'phaser';

/**
 * Type d'action possible dans le jeu.
 * Chaque action sera associée à une ou plusieurs touches.
 */
export enum GameAction {
  ACCELERATE = 'ACCELERATE',
  BRAKE = 'BRAKE',
  TURN_LEFT = 'TURN_LEFT',
  TURN_RIGHT = 'TURN_RIGHT',
  SPRINT = 'SPRINT',
  JUMP = 'JUMP', // Pour les prompts suivants
  DISMOUNT = 'DISMOUNT', // Pour les prompts suivants
}

/**
 * Configuration d'un schéma de contrôle.
 * Map les actions de jeu aux KeyCodes Phaser.
 */
export type KeyBindingScheme = {
  [key in GameAction]: number[];
};

/**
 * Schéma de contrôle par défaut (Flèches + modificateurs).
 *
 * Organisation :
 * - Flèches directionnelles pour le mouvement
 * - SHIFT pour le sprint
 * - ESPACE pour le saut (à venir)
 */
export const DEFAULT_KEY_BINDINGS: KeyBindingScheme = {
  [GameAction.ACCELERATE]: [Phaser.Input.Keyboard.KeyCodes.UP],
  [GameAction.BRAKE]: [Phaser.Input.Keyboard.KeyCodes.DOWN],
  [GameAction.TURN_LEFT]: [Phaser.Input.Keyboard.KeyCodes.LEFT],
  [GameAction.TURN_RIGHT]: [Phaser.Input.Keyboard.KeyCodes.RIGHT],
  [GameAction.SPRINT]: [Phaser.Input.Keyboard.KeyCodes.SHIFT],
  [GameAction.JUMP]: [Phaser.Input.Keyboard.KeyCodes.SPACE],
  [GameAction.DISMOUNT]: [Phaser.Input.Keyboard.KeyCodes.CTRL],
};

/**
 * Schéma de contrôle alternatif (WASD + modificateurs).
 *
 * Pour les joueurs préférant WASD aux flèches.
 */
export const WASD_KEY_BINDINGS: KeyBindingScheme = {
  [GameAction.ACCELERATE]: [Phaser.Input.Keyboard.KeyCodes.W],
  [GameAction.BRAKE]: [Phaser.Input.Keyboard.KeyCodes.S],
  [GameAction.TURN_LEFT]: [Phaser.Input.Keyboard.KeyCodes.A],
  [GameAction.TURN_RIGHT]: [Phaser.Input.Keyboard.KeyCodes.D],
  [GameAction.SPRINT]: [Phaser.Input.Keyboard.KeyCodes.SHIFT],
  [GameAction.JUMP]: [Phaser.Input.Keyboard.KeyCodes.SPACE],
  [GameAction.DISMOUNT]: [Phaser.Input.Keyboard.KeyCodes.CTRL],
};

/**
 * Schéma de contrôle hybride (Flèches OU WASD).
 *
 * Accepte les deux types d'input pour plus de flexibilité.
 */
export const HYBRID_KEY_BINDINGS: KeyBindingScheme = {
  [GameAction.ACCELERATE]: [
    Phaser.Input.Keyboard.KeyCodes.UP,
    Phaser.Input.Keyboard.KeyCodes.W,
  ],
  [GameAction.BRAKE]: [
    Phaser.Input.Keyboard.KeyCodes.DOWN,
    Phaser.Input.Keyboard.KeyCodes.S,
  ],
  [GameAction.TURN_LEFT]: [
    Phaser.Input.Keyboard.KeyCodes.LEFT,
    Phaser.Input.Keyboard.KeyCodes.A,
  ],
  [GameAction.TURN_RIGHT]: [
    Phaser.Input.Keyboard.KeyCodes.RIGHT,
    Phaser.Input.Keyboard.KeyCodes.D,
  ],
  [GameAction.SPRINT]: [Phaser.Input.Keyboard.KeyCodes.SHIFT],
  [GameAction.JUMP]: [Phaser.Input.Keyboard.KeyCodes.SPACE],
  [GameAction.DISMOUNT]: [Phaser.Input.Keyboard.KeyCodes.CTRL],
};

/**
 * Schéma actif par défaut.
 * Peut être changé dynamiquement dans le jeu.
 */
export let ACTIVE_KEY_BINDINGS: KeyBindingScheme = HYBRID_KEY_BINDINGS;

/**
 * Change le schéma de contrôle actif.
 *
 * @param scheme - Le nouveau schéma à utiliser
 */
export function setActiveKeyBindings(scheme: KeyBindingScheme): void {
  ACTIVE_KEY_BINDINGS = scheme;
  console.log('[KeyBindings] Schéma de contrôle mis à jour');
}

/**
 * Réinitialise le schéma de contrôle au schéma hybride par défaut.
 */
export function resetKeyBindings(): void {
  ACTIVE_KEY_BINDINGS = HYBRID_KEY_BINDINGS;
  console.log('[KeyBindings] Schéma de contrôle réinitialisé');
}
