import Phaser from 'phaser';
import { BaseComponent } from './BaseComponent';
import { MovementComponent } from './MovementComponent';
import type { Cyclist } from '@entities/Cyclist';

/**
 * Composant gérant les entrées clavier du joueur.
 *
 * Responsabilités :
 * - Capturer les touches du clavier via Phaser Input
 * - Traduire les inputs en actions (accélérer, freiner, tourner, sprinter)
 * - Communiquer avec le MovementComponent pour appliquer les actions
 *
 * Séparation des responsabilités :
 * - InputComponent : lit les touches et décide QUOI faire
 * - MovementComponent : applique COMMENT le faire (physique)
 * - RotationComponent : gère la rotation du cycliste
 *
 * @example
 * ```typescript
 * const cyclist = new Cyclist(scene, x, y, true);
 * const movement = new MovementComponent(cyclist);
 * const input = new InputComponent(cyclist, scene);
 *
 * cyclist.addComponent(movement);
 * cyclist.addComponent(input);
 * ```
 */
export class InputComponent extends BaseComponent {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Référence au cycliste (typée) */
  private cyclist: Cyclist;

  /** Référence à la scène pour accéder à l'input */
  private scene: Phaser.Scene;

  /** Touches configurées */
  private keys: {
    up: Phaser.Input.Keyboard.Key;
    down: Phaser.Input.Keyboard.Key;
    left: Phaser.Input.Keyboard.Key;
    right: Phaser.Input.Keyboard.Key;
    sprint: Phaser.Input.Keyboard.Key;
  };

  /** Référence au composant de mouvement */
  private movementComponent?: MovementComponent;

  /** Vitesse de rotation actuelle (degrés/seconde) */
  private rotationSpeed: number = 0;

  // ============================================================================
  // CONSTRUCTEUR
  // ============================================================================

  /**
   * Crée un nouveau composant d'input.
   *
   * @param owner - Le cycliste propriétaire
   * @param scene - La scène Phaser (pour accéder à l'input)
   */
  constructor(owner: Phaser.GameObjects.GameObject, scene: Phaser.Scene) {
    super(owner);
    this.cyclist = owner as Cyclist;
    this.scene = scene;

    // Configurer les touches du clavier
    this.keys = this.setupKeys();
  }

  // ============================================================================
  // INITIALISATION
  // ============================================================================

  /**
   * Initialise le composant.
   */
  init(): void {
    // Récupérer la référence au MovementComponent
    const movement = this.cyclist.getComponent(MovementComponent);

    if (!movement) {
      console.warn('[InputComponent] MovementComponent non trouvé sur le cycliste');
    } else {
      this.movementComponent = movement;
    }

    console.log('[InputComponent] Initialisé - Touches: Flèches + Shift pour sprint');
  }

  /**
   * Configure les touches du clavier.
   *
   * @returns Objet contenant les touches configurées
   */
  private setupKeys(): {
    up: Phaser.Input.Keyboard.Key;
    down: Phaser.Input.Keyboard.Key;
    left: Phaser.Input.Keyboard.Key;
    right: Phaser.Input.Keyboard.Key;
    sprint: Phaser.Input.Keyboard.Key;
  } {
    const keyboard = this.scene.input.keyboard;

    if (!keyboard) {
      throw new Error('[InputComponent] Clavier non disponible');
    }

    return {
      up: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.UP),
      down: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.DOWN),
      left: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.LEFT),
      right: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.RIGHT),
      sprint: keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SHIFT),
    };
  }

  // ============================================================================
  // UPDATE
  // ============================================================================

  /**
   * Lit les inputs et les traduit en actions.
   *
   * @param _time - Temps total écoulé (non utilisé)
   * @param delta - Temps écoulé depuis la dernière frame (ms)
   */
  update(_time: number, delta: number): void {
    if (!this.active || !this.movementComponent) {
      return;
    }

    // Convertir delta en secondes
    const deltaSeconds = delta / 1000;

    // Gérer l'accélération et le freinage
    this.handleForwardBackward();

    // Gérer la rotation
    this.handleRotation(deltaSeconds);

    // Gérer le sprint
    this.handleSprint();
  }

  // ============================================================================
  // GESTION DES INPUTS
  // ============================================================================

  /**
   * Gère l'accélération (avant) et le freinage (arrière).
   */
  private handleForwardBackward(): void {
    if (!this.movementComponent) return;

    const upPressed = this.keys.up.isDown;
    const downPressed = this.keys.down.isDown;

    if (upPressed && !downPressed) {
      // Accélérer
      this.movementComponent.accelerate();
      this.movementComponent.stopBraking();
    } else if (downPressed && !upPressed) {
      // Freiner
      this.movementComponent.brake();
      this.movementComponent.stopAccelerating();
    } else {
      // Aucune touche ou les deux : arrêter les deux actions
      this.movementComponent.stopAccelerating();
      this.movementComponent.stopBraking();
    }
  }

  /**
   * Gère la rotation du cycliste (gauche/droite).
   *
   * @param deltaSeconds - Delta time en secondes
   */
  private handleRotation(deltaSeconds: number): void {
    const leftPressed = this.keys.left.isDown;
    const rightPressed = this.keys.right.isDown;

    // Déterminer la direction de rotation
    let targetRotationSpeed = 0;

    if (leftPressed && !rightPressed) {
      targetRotationSpeed = -180; // Rotation à gauche (degrés/seconde)
    } else if (rightPressed && !leftPressed) {
      targetRotationSpeed = 180; // Rotation à droite (degrés/seconde)
    }

    // Interpolation douce de la vitesse de rotation
    const lerpFactor = 0.2;
    this.rotationSpeed = Phaser.Math.Linear(
      this.rotationSpeed,
      targetRotationSpeed,
      lerpFactor
    );

    // Appliquer la rotation au cycliste
    if (Math.abs(this.rotationSpeed) > 1) {
      const rotationDelta = Phaser.Math.DegToRad(this.rotationSpeed * deltaSeconds);
      this.cyclist.rotation += rotationDelta;
    }
  }

  /**
   * Gère le sprint (touche Shift).
   */
  private handleSprint(): void {
    if (!this.movementComponent) return;

    const sprintPressed = this.keys.sprint.isDown;
    this.movementComponent.setSprinting(sprintPressed);
  }

  // ============================================================================
  // MÉTHODES PUBLIQUES
  // ============================================================================

  /**
   * Vérifie si une touche spécifique est pressée.
   *
   * @param key - Nom de la touche ('up', 'down', 'left', 'right', 'sprint')
   * @returns true si la touche est pressée
   */
  public isKeyDown(key: 'up' | 'down' | 'left' | 'right' | 'sprint'): boolean {
    return this.keys[key].isDown;
  }

  /**
   * Active ou désactive les contrôles.
   *
   * @param enabled - true pour activer, false pour désactiver
   */
  public setEnabled(enabled: boolean): void {
    this.setActive(enabled);

    // Réinitialiser les états quand on désactive
    if (!enabled && this.movementComponent) {
      this.movementComponent.stopAccelerating();
      this.movementComponent.stopBraking();
      this.movementComponent.setSprinting(false);
      this.rotationSpeed = 0;
    }
  }

  // ============================================================================
  // DESTRUCTION
  // ============================================================================

  /**
   * Nettoie le composant.
   */
  destroy(): void {
    // Arrêter toutes les actions
    if (this.movementComponent) {
      this.movementComponent.stopAccelerating();
      this.movementComponent.stopBraking();
      this.movementComponent.setSprinting(false);
    }

    this.rotationSpeed = 0;

    console.log('[InputComponent] Détruit');
  }
}
