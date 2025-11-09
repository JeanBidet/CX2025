import type { IGameCommand } from '../../types/IGameCommand';
import type { Cyclist } from '@entities/Cyclist';
import { CYCLIST_BRAKE_ACCELERATION } from '@config/constants';

/**
 * Commande de freinage du cycliste.
 *
 * Applique une force de freinage dans la direction opposée au mouvement.
 * Ralentit progressivement le cycliste jusqu'à l'arrêt complet.
 *
 * Différence avec simplement relâcher l'accélération :
 * - Relâcher : le drag naturel ralentit le cycliste
 * - Freiner : force active appliquée pour ralentir plus vite
 *
 * @example
 * ```typescript
 * const brake = new BrakeCommand();
 * brake.execute(cyclist, delta);
 * ```
 */
export class BrakeCommand implements IGameCommand {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Nom de la commande pour le debug */
  public readonly name = 'Brake';

  /** Priorité de la commande */
  public readonly priority = 15; // Plus prioritaire que l'accélération

  /** Force de freinage (pixels/seconde²) */
  private readonly brakeForce: number;

  /** Seuil de vitesse minimale avant arrêt complet (pixels/seconde) */
  private readonly stopThreshold = 10;

  // ============================================================================
  // CONSTRUCTEUR
  // ============================================================================

  /**
   * Crée une nouvelle commande de freinage.
   *
   * @param customForce - Force personnalisée (optionnel)
   */
  constructor(customForce?: number) {
    this.brakeForce = customForce ?? CYCLIST_BRAKE_ACCELERATION;
  }

  // ============================================================================
  // EXÉCUTION
  // ============================================================================

  /**
   * Exécute la commande de freinage.
   *
   * @param entity - Le cycliste à freiner
   * @param _deltaTime - Temps écoulé
   */
  execute(entity: Cyclist, _deltaTime: number): void {
    const body = entity.getBody();
    const velocity = body.velocity;

    // Calculer la vitesse actuelle (scalaire)
    const speed = Math.sqrt(velocity.x ** 2 + velocity.y ** 2);

    // Si la vitesse est très faible, arrêt complet
    if (speed < this.stopThreshold) {
      body.setVelocity(0, 0);
      body.setAcceleration(0, 0);
      return;
    }

    // Calculer la direction du mouvement (vecteur unitaire)
    const dirX = velocity.x / speed;
    const dirY = velocity.y / speed;

    // Appliquer une force de freinage dans la direction opposée
    const brakeForceX = -dirX * this.brakeForce;
    const brakeForceY = -dirY * this.brakeForce;

    body.setAcceleration(brakeForceX, brakeForceY);
  }

  /**
   * Annule le freinage.
   *
   * @param entity - Le cycliste
   * @param _deltaTime - Temps écoulé
   */
  undo(entity: Cyclist, _deltaTime: number): void {
    const body = entity.getBody();
    body.setAcceleration(0, 0);
  }
}
