/**
 * CrashedState - Fallen state after losing balance
 *
 * Represents the cyclist on the ground after a crash.
 * Features:
 * - Complete immobilization
 * - Dramatic visual effects (rotation tween, flash, particles)
 * - Timer before can attempt remount
 * - Blocks all input during crash
 * - Automatically transitions to REMOUNTING after recovery time
 */

import type { Cyclist } from '@entities/Cyclist';
import type { ICommand } from '../../types/ICommand';
import { StateMachineComponent } from '../../components/StateMachineComponent';
import { StateType, type ICyclistState } from '../../types/cyclistState';

export class CrashedState implements ICyclistState {
  public readonly type = StateType.CRASHED;

  // Crash state constants
  private readonly CRASH_DURATION = 2000; // 2 seconds on ground
  private readonly CRASH_ROTATION_ANGLE = 90; // Rotate 90 degrees when crashed
  private readonly CRASH_ROTATION_DURATION = 300; // Rotation animation duration

  // References to Phaser objects
  private crashTimer?: Phaser.Time.TimerEvent;
  private rotationTween?: Phaser.Tweens.Tween;
  private flashTween?: Phaser.Tweens.Tween;

  /**
   * Enter crashed state
   * Applies dramatic visual effects and immobilizes cyclist
   */
  public enter(cyclist: Cyclist): void {
    const body = cyclist.getBody();
    const scene = cyclist.scene;

    // Complete immobilization
    body.setVelocity(0, 0);
    body.setAcceleration(0, 0);
    body.setMaxVelocity(0);
    body.setImmovable(true);

    // Play crash animation if available
    if (cyclist.anims && cyclist.anims.exists('player_crash') || cyclist.anims.exists('ai_crash')) {
      cyclist.play(cyclist.getIsPlayer() ? 'player_crash' : 'ai_crash', true);
    }

    // Visual effect 1: Rotation tween (bike falls over)
    this.rotationTween = scene.tweens.add({
      targets: cyclist,
      angle: this.CRASH_ROTATION_ANGLE,
      duration: this.CRASH_ROTATION_DURATION,
      ease: 'Cubic.easeOut',
      onComplete: () => {
        delete this.rotationTween;
      },
    });

    // Visual effect 2: Red flash effect
    this.flashTween = scene.tweens.add({
      targets: cyclist,
      tint: 0xff0000, // Red tint
      alpha: 0.7,
      duration: 200,
      yoyo: true,
      repeat: 3,
      onComplete: () => {
        cyclist.clearTint();
        cyclist.setAlpha(1.0);
        delete this.flashTween;
      },
    });

    // Visual effect 3: Dust particles (if particle system exists)
    this.emitCrashParticles(cyclist);

    // Set timer for recovery
    this.crashTimer = scene.time.addEvent({
      delay: this.CRASH_DURATION,
      callback: () => {
        // Transition to REMOUNTING state after recovery time
        const stateMachine = cyclist.getComponent(StateMachineComponent);
        if (stateMachine) {
          stateMachine.changeState(StateType.REMOUNTING);
        }
      },
      callbackScope: this,
    });
  }

  /**
   * Exit crashed state
   * Clean up timers, tweens, and visual effects
   */
  public exit(cyclist: Cyclist): void {
    // Clean up timer
    if (this.crashTimer) {
      this.crashTimer.remove();
      delete this.crashTimer;
    }

    // Clean up rotation tween
    if (this.rotationTween) {
      this.rotationTween.stop();
      delete this.rotationTween;
    }

    // Clean up flash tween
    if (this.flashTween) {
      this.flashTween.stop();
      delete this.flashTween;
    }

    // Reset visual properties
    cyclist.clearTint();
    cyclist.setAlpha(1.0);
    cyclist.setAngle(0); // Reset rotation

    // Reset physics
    const body = cyclist.getBody();
    body.setImmovable(false);
    body.setMaxVelocity(200); // Will be overridden by next state
  }

  /**
   * Update crashed state
   * Cyclist is immobile, waiting for recovery timer
   */
  public update(_cyclist: Cyclist, _delta: number): void {
    // Nothing to update - timer handles recovery
    // Could add visual effects like blinking or shaking here
  }

  /**
   * Handle input during crash
   * All inputs are blocked while crashed
   */
  public handleInput(_cyclist: Cyclist, _command: ICommand): void {
    // Block all inputs during crash
    // Player must wait for recovery timer
  }

  /**
   * Validate state transitions from CRASHED
   * Can only transition to REMOUNTING after recovery time
   */
  public canTransitionTo(newState: StateType): boolean {
    switch (newState) {
      case StateType.RIDING:
        return false; // Must go through REMOUNTING first
      case StateType.CARRYING:
        return false; // Must recover first
      case StateType.REMOUNTING:
        return true; // Automatic transition after recovery
      case StateType.CRASHED:
        return false; // Already crashed
      default:
        return false;
    }
  }

  /**
   * Emit dust/debris particles when crashing
   * Creates a visual impact effect
   */
  private emitCrashParticles(cyclist: Cyclist): void {
    const scene = cyclist.scene;

    // Create temporary graphics for particles if no particle system exists
    // Using a simple particle emitter if available in the scene
    if (scene.add.particles) {
      // Create a simple particle effect at crash location
      const particles = scene.add.particles(cyclist.x, cyclist.y, 'terrain_tileset', {
        speed: { min: 50, max: 150 },
        angle: { min: 0, max: 360 },
        scale: { start: 0.3, end: 0 },
        alpha: { start: 0.8, end: 0 },
        lifespan: 600,
        quantity: 15,
        blendMode: Phaser.BlendModes.ADD,
        tint: 0x888888, // Gray dust
      });

      // Destroy particle emitter after emission
      scene.time.delayedCall(700, () => {
        particles.destroy();
      });
    }
  }
}
