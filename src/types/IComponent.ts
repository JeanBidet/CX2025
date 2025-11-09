import Phaser from 'phaser';

/**
 * Interface définissant le contrat pour tous les composants métier.
 * Les composants sont attachés aux GameObjects Phaser et encapsulent
 * la logique métier tout en séparant les préoccupations du rendu.
 *
 * @example
 * ```typescript
 * class StaminaComponent implements IComponent {
 *   constructor(private owner: Phaser.GameObjects.GameObject) {}
 *
 *   init(): void {
 *     // Initialisation du composant
 *   }
 *
 *   preUpdate(time: number, delta: number): void {
 *     // Logique avant update
 *   }
 *
 *   update(time: number, delta: number): void {
 *     // Logique principale
 *   }
 *
 *   destroy(): void {
 *     // Nettoyage
 *   }
 * }
 * ```
 */
export interface IComponent {
  /**
   * Référence au GameObject Phaser propriétaire de ce composant.
   * Le composant ne doit interagir qu'avec son propriétaire.
   */
  readonly owner: Phaser.GameObjects.GameObject;

  /**
   * Initialise le composant après sa création.
   * Appelé une seule fois lors de l'ajout du composant.
   */
  init(): void;

  /**
   * Logique exécutée avant le update principal.
   * Utile pour les calculs préparatoires.
   *
   * @param time - Temps total écoulé depuis le début du jeu (ms)
   * @param delta - Temps écoulé depuis la dernière frame (ms)
   */
  preUpdate(time: number, delta: number): void;

  /**
   * Logique principale du composant, appelée chaque frame.
   *
   * @param time - Temps total écoulé depuis le début du jeu (ms)
   * @param delta - Temps écoulé depuis la dernière frame (ms)
   */
  update(time: number, delta: number): void;

  /**
   * Nettoie le composant avant sa destruction.
   * Libère les ressources, désabonne les événements, etc.
   */
  destroy(): void;
}
