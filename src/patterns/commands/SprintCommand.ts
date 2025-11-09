import type { IGameCommand } from '../../types/IGameCommand';
import type { Cyclist } from '@entities/Cyclist';
import { MovementComponent } from '@components/MovementComponent';
import { EnduranceComponent } from '@components/EnduranceComponent';

/**
 * Commande pour activer/désactiver le sprint.
 *
 * Le sprint augmente la vitesse maximale du cycliste mais consomme de l'endurance.
 * Le sprint ne peut être activé que si le cycliste a suffisamment d'endurance.
 *
 * Cette commande est un peu différente car elle modifie un état
 * plutôt que d'appliquer une force directe.
 *
 * @example
 * ```typescript
 * const sprint = new SprintCommand(true); // Activer
 * sprint.execute(cyclist, delta);
 *
 * const stopSprint = new SprintCommand(false); // Désactiver
 * stopSprint.execute(cyclist, delta);
 * ```
 */
export class SprintCommand implements IGameCommand {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Nom de la commande */
  public readonly name: string;

  /** Priorité de la commande */
  public readonly priority = 20; // Très prioritaire

  /** État du sprint (actif ou non) */
  private readonly sprintActive: boolean;

  // ============================================================================
  // CONSTRUCTEUR
  // ============================================================================

  /**
   * Crée une nouvelle commande de sprint.
   *
   * @param activate - true pour activer le sprint, false pour le désactiver
   */
  constructor(activate: boolean = true) {
    this.sprintActive = activate;
    this.name = activate ? 'SprintOn' : 'SprintOff';
  }

  // ============================================================================
  // EXÉCUTION
  // ============================================================================

  /**
   * Exécute la commande de sprint.
   *
   * @param entity - Le cycliste
   * @param _deltaTime - Temps écoulé
   */
  execute(entity: Cyclist, _deltaTime: number): void {
    // Récupérer les composants nécessaires
    const movement = entity.getComponent(MovementComponent);
    const endurance = entity.getComponent(EnduranceComponent);

    if (!movement) {
      console.warn('[SprintCommand] MovementComponent non trouvé');
      return;
    }

    if (this.sprintActive) {
      // Activer le sprint
      if (endurance) {
        // Vérifier si le sprint est possible (assez d'endurance)
        if (endurance.canSprint()) {
          const activated = endurance.activateSprint();
          if (activated) {
            movement.setSprinting(true);
          }
        } else {
          // Pas assez d'endurance pour sprinter
          console.log('[SprintCommand] Endurance insuffisante pour sprinter');
        }
      } else {
        // Pas de système d'endurance, activer le sprint directement
        movement.setSprinting(true);
      }
    } else {
      // Désactiver le sprint
      movement.setSprinting(false);
      if (endurance) {
        endurance.deactivateSprint();
      }
    }
  }

  /**
   * Annule la commande de sprint.
   *
   * @param entity - Le cycliste
   * @param _deltaTime - Temps écoulé
   */
  undo(entity: Cyclist, _deltaTime: number): void {
    const movement = entity.getComponent(MovementComponent);
    const endurance = entity.getComponent(EnduranceComponent);

    if (movement) {
      // Inverser l'état
      movement.setSprinting(!this.sprintActive);

      if (endurance) {
        if (!this.sprintActive) {
          // On annule une désactivation → activer
          endurance.activateSprint();
        } else {
          // On annule une activation → désactiver
          endurance.deactivateSprint();
        }
      }
    }
  }
}
