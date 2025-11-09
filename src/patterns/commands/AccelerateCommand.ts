import type { IGameCommand } from '../../types/IGameCommand';
import type { Cyclist } from '@entities/Cyclist';
import { CYCLIST_ACCELERATION } from '@config/constants';

/**
 * Commande d'accélération du cycliste.
 *
 * Applique une force d'accélération dans la direction actuelle du cycliste.
 * Utilise le body Phaser Arcade pour appliquer la physique.
 *
 * Principe du Command Pattern :
 * - Cette classe encapsule l'ACTION d'accélérer
 * - Elle peut être invoquée par l'input joueur OU l'IA
 * - Elle est testable indépendamment
 * - Elle peut être enregistrée pour replay
 *
 * @example
 * ```typescript
 * const accelerate = new AccelerateCommand();
 * accelerate.execute(cyclist, delta);
 * ```
 */
export class AccelerateCommand implements IGameCommand {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Nom de la commande pour le debug */
  public readonly name = 'Accelerate';

  /** Priorité de la commande (plus élevée = plus prioritaire) */
  public readonly priority = 10;

  /** Force d'accélération (pixels/seconde²) */
  private readonly accelerationForce: number;

  // ============================================================================
  // CONSTRUCTEUR
  // ============================================================================

  /**
   * Crée une nouvelle commande d'accélération.
   *
   * @param customForce - Force personnalisée (optionnel, utilise la constante par défaut)
   */
  constructor(customForce?: number) {
    this.accelerationForce = customForce ?? CYCLIST_ACCELERATION;
  }

  // ============================================================================
  // EXÉCUTION
  // ============================================================================

  /**
   * Exécute la commande d'accélération.
   *
   * @param entity - Le cycliste à accélérer
   * @param _deltaTime - Temps écoulé (non utilisé ici, Phaser gère le delta automatiquement)
   */
  execute(entity: Cyclist, _deltaTime: number): void {
    // Récupérer le body physique
    const body = entity.getBody();

    // Récupérer l'angle actuel du cycliste (en radians)
    const angle = entity.rotation;

    // Calculer les composantes X et Y de l'accélération
    // Math.cos(angle) = direction horizontale
    // Math.sin(angle) = direction verticale
    const forceX = Math.cos(angle) * this.accelerationForce;
    const forceY = Math.sin(angle) * this.accelerationForce;

    // Appliquer l'accélération au body Phaser
    // Phaser intègre automatiquement : velocity += acceleration * delta
    body.setAcceleration(forceX, forceY);
  }

  /**
   * Annule l'accélération (optionnel, pour replay/debug).
   *
   * @param entity - Le cycliste
   * @param _deltaTime - Temps écoulé
   */
  undo(entity: Cyclist, _deltaTime: number): void {
    // Pour annuler, on met simplement l'accélération à 0
    const body = entity.getBody();
    body.setAcceleration(0, 0);
  }
}
