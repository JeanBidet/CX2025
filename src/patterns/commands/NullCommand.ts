import type { IGameCommand } from '../../types/IGameCommand';
import type { Cyclist } from '@entities/Cyclist';

/**
 * Commande nulle (Null Object Pattern).
 *
 * Une commande qui ne fait rien. Utile pour :
 * - Éviter les vérifications null dans le code
 * - Avoir un comportement par défaut "ne rien faire"
 * - Simplifier la logique des input handlers
 *
 * Au lieu de :
 * ```typescript
 * if (command !== null) {
 *   command.execute(entity, delta);
 * }
 * ```
 *
 * On peut faire :
 * ```typescript
 * command.execute(entity, delta); // Fonctionne toujours
 * ```
 *
 * @example
 * ```typescript
 * const noAction = new NullCommand();
 * noAction.execute(cyclist, delta); // Ne fait rien
 * ```
 */
export class NullCommand implements IGameCommand {
  /** Instance singleton (une seule instance nécessaire) */
  private static instance: NullCommand;

  /** Nom de la commande */
  public readonly name = 'Null';

  /** Priorité de la commande */
  public readonly priority = 0;

  // ============================================================================
  // CONSTRUCTEUR PRIVÉ (SINGLETON)
  // ============================================================================

  private constructor() {
    // Constructeur privé pour forcer l'utilisation de getInstance()
  }

  /**
   * Récupère l'instance unique de NullCommand.
   */
  public static getInstance(): NullCommand {
    if (!NullCommand.instance) {
      NullCommand.instance = new NullCommand();
    }
    return NullCommand.instance;
  }

  // ============================================================================
  // EXÉCUTION (NE FAIT RIEN)
  // ============================================================================

  /**
   * Exécute la commande (ne fait rien).
   */
  execute(_entity: Cyclist, _deltaTime: number): void {
    // Intentionnellement vide
  }

  /**
   * Annule la commande (ne fait rien).
   */
  undo?(_entity: Cyclist, _deltaTime: number): void {
    // Intentionnellement vide
  }
}
