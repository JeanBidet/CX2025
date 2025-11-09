import type { Cyclist } from '@entities/Cyclist';

/**
 * Interface spécialisée pour les commandes de jeu.
 *
 * Extension du pattern Command adapté au contexte du jeu :
 * - Prend une entité cible (Cyclist)
 * - Intègre le delta time pour calculs indépendants du framerate
 * - Optionnel : support undo pour replay/debug
 *
 * Avantages du Command Pattern :
 * 1. **Découplage** : Sépare l'invocation (input) de l'exécution (action)
 * 2. **Testabilité** : Chaque commande testable indépendamment
 * 3. **Extensibilité** : Nouvelles commandes sans modifier l'existant (Open/Closed)
 * 4. **Replay** : Enregistrer et rejouer des séquences de commandes
 * 5. **IA** : L'IA peut utiliser les mêmes commandes que le joueur
 * 6. **Remapping** : Changer les touches sans toucher à la logique
 *
 * @example
 * ```typescript
 * class AccelerateCommand implements IGameCommand {
 *   execute(cyclist: Cyclist, deltaTime: number): void {
 *     const body = cyclist.getBody();
 *     const angle = cyclist.rotation;
 *     const force = 300; // Accélération
 *
 *     body.setAcceleration(
 *       Math.cos(angle) * force,
 *       Math.sin(angle) * force
 *     );
 *   }
 * }
 *
 * // Utilisation
 * const command = new AccelerateCommand();
 * command.execute(player, delta);
 * ```
 */
export interface IGameCommand {
  /**
   * Exécute la commande sur l'entité cible.
   *
   * @param entity - Le cycliste sur lequel appliquer la commande
   * @param deltaTime - Temps écoulé depuis la dernière frame (ms)
   */
  execute(entity: Cyclist, deltaTime: number): void;

  /**
   * Annule l'exécution de la commande (optionnel).
   *
   * Utilisé pour :
   * - Systèmes de replay (rembobinage)
   * - Debug (visualisation des actions)
   * - Systèmes d'aide (montrer ce qui se passerait)
   *
   * @param entity - Le cycliste sur lequel annuler la commande
   * @param deltaTime - Temps de l'annulation
   */
  undo?(entity: Cyclist, deltaTime: number): void;

  /**
   * Nom de la commande (optionnel, utile pour le debug).
   */
  readonly name?: string;

  /**
   * Priorité de la commande (optionnel).
   * Utilisé pour résoudre les conflits quand plusieurs commandes sont actives.
   * Valeur plus élevée = priorité plus haute.
   */
  readonly priority?: number;
}
