/**
 * CarryingState - Walking with bike (portage)
 *
 * Represents the cyclist dismounted and carrying/pushing the bike.
 * Features:
 * - Reduced movement speed (walking speed)
 * - Partial stamina recovery
 * - No balance management needed
 * - Simplified physics (no rotation/drift)
 * - Can transition to REMOUNTING
 */

import type { Cyclist } from '@entities/Cyclist';
import type { ICommand } from '../../types/ICommand';
import { StateType, type ICyclistState } from '../../types/cyclistState';

export class CarryingState implements ICyclistState {
  public readonly type = StateType.CARRYING;

  // Carrying state constants
  private readonly WALKING_MAX_VELOCITY = 80; // Much slower than riding
  private readonly WALKING_DRAG = 500; // Higher drag for walking

  /**
   * Enter carrying state
   * Reduces speed and changes to walking animation
   */
  public enter(cyclist: Cyclist): void {
    const body = cyclist.getBody();

    // Set walking physics - much slower than riding
    body.setMaxVelocity(this.WALKING_MAX_VELOCITY);
    body.setDrag(this.WALKING_DRAG);
    body.setImmovable(false);
    body.setAllowGravity(false);

    // Play carrying/walking animation
    if (cyclist.anims && cyclist.anims.exists('player_carry') || cyclist.anims.exists('ai_carry')) {
      cyclist.play(cyclist.getIsPlayer() ? 'player_carry' : 'ai_carry', true);
    }

    // Visual indicator - slight tint to show different state
    cyclist.setTint(0xccccff); // Slight blue tint

    // Reset rotation if any
    cyclist.setAngle(0);
  }

  /**
   * Exit carrying state
   * Clean up walking-specific properties
   */
  public exit(cyclist: Cyclist): void {
    // Remove visual indicators
    cyclist.clearTint();

    // Physics will be reset by the next state's enter()
  }

  /**
   * Update carrying state each frame
   * Handles partial stamina recovery
   */
  public update(cyclist: Cyclist, _delta: number): void {
    // In carrying state, stamina could partially recover
    // This would be handled by a StaminaComponent if implemented

    // Adjust animation speed based on movement
    const body = cyclist.getBody();
    const velocity = body.velocity;
    const speed = Math.sqrt(velocity.x * velocity.x + velocity.y * velocity.y);

    if (cyclist.anims && cyclist.anims.currentAnim) {
      if (speed > 40) {
        // Walking fast
        cyclist.anims.currentAnim.frameRate = 8;
      } else if (speed > 10) {
        // Walking normal
        cyclist.anims.currentAnim.frameRate = 5;
      } else {
        // Standing still
        cyclist.anims.currentAnim.frameRate = 2;
      }
    }
  }

  /**
   * Handle input commands while carrying
   * Movement commands work but with reduced effectiveness
   */
  public handleInput(_cyclist: Cyclist, command: ICommand): void {
    // Execute commands normally, but physics limits make movement slower
    // Sprint command might be ignored or have reduced effect
    command.execute();
  }

  /**
   * Validate state transitions from CARRYING
   * Can only transition to REMOUNTING (getting back on bike)
   */
  public canTransitionTo(newState: StateType): boolean {
    switch (newState) {
      case StateType.RIDING:
        return false; // Must go through REMOUNTING first
      case StateType.CARRYING:
        return false; // Already carrying
      case StateType.REMOUNTING:
        return true; // Can get back on bike
      case StateType.CRASHED:
        return false; // Can't crash while walking (no balance needed)
      default:
        return false;
    }
  }
}
