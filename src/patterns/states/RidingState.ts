/**
 * RidingState - Normal cycling state
 *
 * Represents the cyclist riding the bike normally.
 * Features:
 * - Full acceleration and steering control
 * - Normal stamina consumption
 * - Balance management active
 * - Can transition to CARRYING (dismount) or CRASHED (lose balance)
 */

import type { Cyclist } from '@entities/Cyclist';
import type { ICommand } from '../../types/ICommand';
import { StateType, type ICyclistState } from '../../types/cyclistState';

export class RidingState implements ICyclistState {
  public readonly type = StateType.RIDING;

  /**
   * Enter riding state
   * Sets up normal cycling physics and animation
   */
  public enter(cyclist: Cyclist): void {
    const body = cyclist.getBody();

    // Restore normal physics properties
    body.setMaxVelocity(200); // Normal max velocity
    body.setImmovable(false);
    body.setAllowGravity(false);

    // Play riding animation
    if (cyclist.anims && cyclist.anims.exists('player_ride') || cyclist.anims.exists('ai_ride')) {
      cyclist.play(cyclist.getIsPlayer() ? 'player_ride' : 'ai_ride', true);
    }

    // Reset any visual effects from previous states
    cyclist.clearTint();
    cyclist.setAlpha(1.0);
    cyclist.setAngle(0);
  }

  /**
   * Exit riding state
   * Clean up before transitioning to another state
   */
  public exit(_cyclist: Cyclist): void {
    // Cleanup if needed
    // Most cleanup happens in the enter() of the next state
  }

  /**
   * Update riding state each frame
   * Handles stamina consumption and balance checks
   */
  public update(cyclist: Cyclist, _delta: number): void {
    // Stamina consumption is handled by MovementComponent
    // Balance checks could trigger CRASHED transition
    // This is where you'd check if balance reaches 0

    const body = cyclist.getBody();
    const velocity = body.velocity;
    const speed = Math.sqrt(velocity.x * velocity.x + velocity.y * velocity.y);

    // Visual feedback based on speed
    if (speed > 150) {
      // High speed - could add particle effects or animation speed adjustments
      if (cyclist.anims && cyclist.anims.currentAnim) {
        cyclist.anims.currentAnim.frameRate = 12;
      }
    } else if (speed > 50) {
      // Normal speed
      if (cyclist.anims && cyclist.anims.currentAnim) {
        cyclist.anims.currentAnim.frameRate = 8;
      }
    } else {
      // Low speed
      if (cyclist.anims && cyclist.anims.currentAnim) {
        cyclist.anims.currentAnim.frameRate = 4;
      }
    }
  }

  /**
   * Handle input commands while riding
   * All movement commands are processed normally
   */
  public handleInput(_cyclist: Cyclist, command: ICommand): void {
    // Execute the command normally
    command.execute();
  }

  /**
   * Validate state transitions from RIDING
   * Can transition to CARRYING (dismount) or CRASHED (lose balance)
   */
  public canTransitionTo(newState: StateType): boolean {
    switch (newState) {
      case StateType.RIDING:
        return false; // Already in RIDING state
      case StateType.CARRYING:
        return true; // Can dismount voluntarily
      case StateType.CRASHED:
        return true; // Can crash if balance reaches 0
      case StateType.REMOUNTING:
        return false; // Can't remount while already riding
      default:
        return false;
    }
  }
}
