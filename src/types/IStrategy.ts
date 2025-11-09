/**
 * Interface pour le pattern Strategy.
 * Définit une famille d'algorithmes, encapsule chacun d'eux et les rend interchangeables.
 * Strategy permet à l'algorithme de varier indépendamment des clients qui l'utilisent.
 *
 * @template TInput - Type des données d'entrée de la stratégie
 * @template TOutput - Type du résultat de la stratégie
 *
 * @example
 * ```typescript
 * interface AIInput {
 *   position: Phaser.Math.Vector2;
 *   obstacles: Obstacle[];
 * }
 *
 * class AggressiveStrategy implements IStrategy<AIInput, void> {
 *   execute(input: AIInput): void {
 *     // Logique d'IA agressive
 *   }
 * }
 *
 * class DefensiveStrategy implements IStrategy<AIInput, void> {
 *   execute(input: AIInput): void {
 *     // Logique d'IA défensive
 *   }
 * }
 * ```
 */
export interface IStrategy<TInput, TOutput> {
  /**
   * Exécute la stratégie avec les données fournies.
   *
   * @param input - Données d'entrée pour la stratégie
   * @returns Le résultat de l'exécution de la stratégie
   */
  execute(input: TInput): TOutput;
}
