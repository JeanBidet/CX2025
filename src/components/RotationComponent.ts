import Phaser from 'phaser';
import { BaseComponent } from './BaseComponent';

/**
 * Composant exemple qui fait tourner un GameObject.
 *
 * Démontre :
 * - Comment créer un composant métier
 * - Comment hériter de BaseComponent
 * - Comment accéder aux propriétés du GameObject propriétaire
 * - Comment implémenter la logique de mise à jour
 *
 * @example
 * ```typescript
 * // Dans une scène Phaser
 * const sprite = this.add.sprite(100, 100, 'key');
 * const rotationComponent = new RotationComponent(sprite, 90); // 90 degrés/seconde
 * rotationComponent.init();
 *
 * // Dans le update de la scène
 * rotationComponent.update(time, delta);
 * ```
 */
export class RotationComponent extends BaseComponent {
  /**
   * Vitesse de rotation en degrés par seconde.
   */
  private rotationSpeed: number;

  /**
   * Crée un nouveau composant de rotation.
   *
   * @param owner - Le GameObject qui sera tourné
   * @param rotationSpeed - Vitesse de rotation en degrés/seconde (défaut: 45)
   */
  constructor(owner: Phaser.GameObjects.GameObject, rotationSpeed: number = 45) {
    super(owner);
    this.rotationSpeed = rotationSpeed;
  }

  /**
   * Initialise le composant.
   * Dans ce cas, log simplement l'initialisation.
   */
  init(): void {
    console.log(`[RotationComponent] Initialisé avec vitesse: ${this.rotationSpeed}°/s`);
  }

  /**
   * Met à jour la rotation du GameObject chaque frame.
   *
   * @param _time - Temps total écoulé depuis le début du jeu (ms)
   * @param delta - Temps écoulé depuis la dernière frame (ms)
   */
  update(_time: number, delta: number): void {
    if (!this.active) {
      return;
    }

    // Accéder au GameObject propriétaire avec les propriétés Sprite
    const sprite = this.getOwnerAs<Phaser.GameObjects.Sprite>();

    // Convertir la vitesse de degrés/seconde en radians/frame
    // delta est en millisecondes, donc on divise par 1000
    const rotationDelta = Phaser.Math.DegToRad(this.rotationSpeed * (delta / 1000));

    // Appliquer la rotation
    sprite.rotation += rotationDelta;
  }

  /**
   * Nettoie le composant.
   */
  destroy(): void {
    console.log('[RotationComponent] Détruit');
  }

  /**
   * Modifie la vitesse de rotation.
   *
   * @param speed - Nouvelle vitesse en degrés/seconde
   */
  public setRotationSpeed(speed: number): void {
    this.rotationSpeed = speed;
  }

  /**
   * Récupère la vitesse de rotation actuelle.
   *
   * @returns Vitesse en degrés/seconde
   */
  public getRotationSpeed(): number {
    return this.rotationSpeed;
  }
}
