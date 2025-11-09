/**
 * Interface pour le pattern Command.
 * Encapsule une action/requête comme un objet, permettant de :
 * - Paramétrer des clients avec différentes requêtes
 * - Mettre en file d'attente des requêtes
 * - Supporter l'annulation (undo/redo)
 *
 * @example
 * ```typescript
 * class AccelerateCommand implements ICommand {
 *   constructor(private cyclist: Cyclist, private amount: number) {}
 *
 *   execute(): void {
 *     this.cyclist.accelerate(this.amount);
 *   }
 *
 *   undo(): void {
 *     this.cyclist.decelerate(this.amount);
 *   }
 * }
 * ```
 */
export interface ICommand {
  /**
   * Exécute la commande.
   */
  execute(): void;

  /**
   * Annule l'exécution de la commande (optionnel).
   * Permet l'implémentation de mécanismes undo/redo.
   */
  undo?(): void;
}
