/**
 * Interface pour le pattern State.
 * Permet à un objet de modifier son comportement lorsque son état interne change.
 * L'objet semblera avoir changé de classe.
 *
 * @template TContext - Type du contexte qui possède cet état
 *
 * @example
 * ```typescript
 * class RidingState implements IState<Cyclist> {
 *   enter(context: Cyclist): void {
 *     console.log('Début du pédalage');
 *   }
 *
 *   update(context: Cyclist, delta: number): void {
 *     // Logique de pédalage
 *   }
 *
 *   exit(context: Cyclist): void {
 *     console.log('Fin du pédalage');
 *   }
 * }
 * ```
 */
export interface IState<TContext> {
  /**
   * Appelé lors de l'entrée dans cet état.
   * Initialise les comportements spécifiques à l'état.
   *
   * @param context - Le contexte qui possède cet état
   */
  enter(context: TContext): void;

  /**
   * Logique exécutée chaque frame tant que l'état est actif.
   *
   * @param context - Le contexte qui possède cet état
   * @param delta - Temps écoulé depuis la dernière frame (ms)
   */
  update(context: TContext, delta: number): void;

  /**
   * Appelé lors de la sortie de cet état.
   * Nettoie les comportements spécifiques à l'état.
   *
   * @param context - Le contexte qui possède cet état
   */
  exit(context: TContext): void;
}
