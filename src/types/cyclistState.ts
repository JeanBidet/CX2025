/**
 * Cyclist State Types and Interfaces
 *
 * Defines the State Pattern implementation for cyclist behavior management.
 * Each state represents a distinct mode of operation with specific physics,
 * animations, and input handling.
 */

import type { Cyclist } from '@entities/Cyclist';
import type { ICommand } from '../types/ICommand';

/**
 * Enum representing all possible cyclist states
 */
export enum StateType {
  RIDING = 'RIDING',       // Normal cycling state
  CARRYING = 'CARRYING',   // Walking with bike (portage)
  REMOUNTING = 'REMOUNTING', // Transitional state getting back on bike
  CRASHED = 'CRASHED'      // Fallen state after losing balance
}

/**
 * Interface for all cyclist states
 * Implements the State Pattern with strict type safety
 */
export interface ICyclistState {
  /**
   * State type identifier
   */
  readonly type: StateType;

  /**
   * Called when entering this state
   * Used to initialize state-specific properties, animations, and physics
   *
   * @param cyclist - The cyclist entity entering this state
   */
  enter(cyclist: Cyclist): void;

  /**
   * Called when exiting this state
   * Used to clean up state-specific resources and reset properties
   *
   * @param cyclist - The cyclist entity exiting this state
   */
  exit(cyclist: Cyclist): void;

  /**
   * Called every frame while in this state
   * Handles state-specific behavior and updates
   *
   * @param cyclist - The cyclist entity being updated
   * @param delta - Time elapsed since last frame in milliseconds
   */
  update(cyclist: Cyclist, delta: number): void;

  /**
   * Handles input commands in the context of this state
   * Some states may ignore certain commands (e.g., CRASHED ignores movement)
   *
   * @param cyclist - The cyclist entity receiving input
   * @param command - The command to execute
   */
  handleInput(cyclist: Cyclist, command: ICommand): void;

  /**
   * Validates whether a transition to a new state is allowed
   * Enforces state machine coherence and prevents invalid transitions
   *
   * @param newState - The state type to transition to
   * @returns true if transition is allowed, false otherwise
   */
  canTransitionTo(newState: StateType): boolean;
}

/**
 * Transition history entry for debugging and analytics
 */
export interface StateTransition {
  readonly fromState: StateType;
  readonly toState: StateType;
  readonly timestamp: number;
  reason?: string | undefined;
}

/**
 * Configuration for state-specific physics properties
 */
export interface StatePhysicsConfig {
  readonly maxVelocity: number;
  readonly drag: number;
  readonly immovable: boolean;
  readonly allowGravity: boolean;
}

/**
 * Configuration for state-specific animation properties
 */
export interface StateAnimationConfig {
  readonly animationKey: string;
  readonly loop: boolean;
  readonly frameRate?: number;
}
