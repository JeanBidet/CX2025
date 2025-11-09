import type { IGameCommand } from '../../types/IGameCommand';
import type { Cyclist } from '@entities/Cyclist';
import { CYCLIST_ROTATION_SPEED_LOW, CYCLIST_ROTATION_SPEED_HIGH, CYCLIST_ROTATION_SPEED_THRESHOLD } from '@config/constants';
import Phaser from 'phaser';

/**
 * Commande pour tourner vers la gauche.
 *
 * La vitesse de rotation dépend de la vitesse actuelle du cycliste :
 * - À basse vitesse : rotation rapide (rayon de braquage serré)
 * - À haute vitesse : rotation lente (rayon de braquage large)
 *
 * Simule le comportement réaliste d'un vélo.
 *
 * @example
 * ```typescript
 * const turnLeft = new TurnLeftCommand();
 * turnLeft.execute(cyclist, delta);
 * ```
 */
export class TurnLeftCommand implements IGameCommand {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Nom de la commande */
  public readonly name = 'TurnLeft';

  /** Priorité de la commande */
  public readonly priority = 5;

  // ============================================================================
  // EXÉCUTION
  // ============================================================================

  /**
   * Exécute la commande de rotation gauche.
   *
   * @param entity - Le cycliste à faire tourner
   * @param deltaTime - Temps écoulé depuis la dernière frame (ms)
   */
  execute(entity: Cyclist, deltaTime: number): void {
    const body = entity.getBody();

    // Calculer la vitesse actuelle
    const speed = Math.sqrt(body.velocity.x ** 2 + body.velocity.y ** 2);

    // Déterminer la vitesse de rotation selon la vitesse actuelle
    // Plus on va vite, plus il est difficile de tourner
    let rotationSpeed: number;
    if (speed < CYCLIST_ROTATION_SPEED_THRESHOLD) {
      rotationSpeed = CYCLIST_ROTATION_SPEED_LOW; // Rotation rapide
    } else {
      rotationSpeed = CYCLIST_ROTATION_SPEED_HIGH; // Rotation lente
    }

    // Convertir en radians et appliquer le delta time
    const rotationDelta = Phaser.Math.DegToRad(rotationSpeed * (deltaTime / 1000));

    // Tourner vers la gauche (rotation négative)
    entity.rotation -= rotationDelta;
  }

  /**
   * Annule la rotation (non implémenté pour ce type de commande).
   */
  undo?(_entity: Cyclist, _deltaTime: number): void {
    // Difficile d'annuler une rotation sans connaître l'état précédent
    // Pour un système de replay avancé, on stockerait l'angle avant rotation
  }
}
