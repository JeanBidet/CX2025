/**
 * RemountingState - Transitional state for getting back on bike
 *
 * Represents the brief moment when the cyclist is mounting the bike.
 * Features:
 * - Temporary state with fixed duration
 * - Blocks most input during animation
 * - Uses Phaser timer for automatic transition
 * - Plays mounting animation
 * - Automatically transitions to RIDING when complete
 */

import type { Cyclist } from '@entities/Cyclist';
import type { ICommand } from '../../types/ICommand';
import { StateMachineComponent } from '../../components/StateMachineComponent';
import { StateType, type ICyclistState } from '../../types/cyclistState';

export class RemountingState implements ICyclistState {
  public readonly type = StateType.REMOUNTING;

  // Remounting duration in milliseconds
  private readonly REMOUNT_DURATION = 1000; // 1 second to remount

  // Reference to the timer event
  private remountTimer?: Phaser.Time.TimerEvent;

  /**
   * Enter remounting state
   * Starts timer and plays animation
   */
  public enter(cyclist: Cyclist): void {
    const body = cyclist.getBody();
    const scene = cyclist.scene;

    // Slow down significantly during remount
    body.setMaxVelocity(40); // Very slow during remount
    body.setDrag(800); // High drag to slow down quickly
    body.setImmovable(false);

    // Play remounting animation
    if (cyclist.anims && cyclist.anims.exists('player_remount') || cyclist.anims.exists('ai_remount')) {
      cyclist.play(cyclist.getIsPlayer() ? 'player_remount' : 'ai_remount', true);
    }

    // Visual feedback - yellow tint during remount
    cyclist.setTint(0xffffaa);

    // Set up timer for automatic transition to RIDING
    this.remountTimer = scene.time.addEvent({
      delay: this.REMOUNT_DURATION,
      callback: () => {
        // Transition to RIDING state after timer completes
        // This will be handled by the StateMachineComponent
        const stateMachine = cyclist.getComponent(StateMachineComponent);
        if (stateMachine) {
          stateMachine.changeState(StateType.RIDING);
        }
      },
      callbackScope: this,
    });
  }

  /**
   * Exit remounting state
   * Clean up timer and visual effects
   */
  public exit(cyclist: Cyclist): void {
    // Clean up timer if it exists
    if (this.remountTimer) {
      this.remountTimer.remove();
      delete this.remountTimer;
    }

    // Remove visual indicators
    cyclist.clearTint();
  }

  /**
   * Update remounting state
   * Not much happens here - timer handles the transition
   */
  public update(_cyclist: Cyclist, _delta: number): void {
    // Timer handles the transition automatically
    // Could add visual effects or progress indicator here
  }

  /**
   * Handle input during remounting
   * Most inputs are blocked during this transitional state
   */
  public handleInput(_cyclist: Cyclist, _command: ICommand): void {
    // Block most inputs during remounting
    // Player must wait for the animation to complete
    // Commands are simply ignored
  }

  /**
   * Validate state transitions from REMOUNTING
   * Automatically transitions to RIDING after timer
   * Can be interrupted by CRASHED if something goes wrong
   */
  public canTransitionTo(newState: StateType): boolean {
    switch (newState) {
      case StateType.RIDING:
        return true; // Automatic transition after timer
      case StateType.CARRYING:
        return false; // Can't dismount while mounting
      case StateType.REMOUNTING:
        return false; // Already remounting
      case StateType.CRASHED:
        return true; // Could crash during remount attempt
      default:
        return false;
    }
  }
}
