/**
 * StateMachineComponent - Manages cyclist state transitions
 *
 * Implements the State Pattern with a finite state machine (FSM).
 * Features:
 * - Manages all cyclist states (RIDING, CARRYING, REMOUNTING, CRASHED)
 * - Enforces valid state transitions
 * - Maintains transition history for debugging
 * - Delegates update and input handling to current state
 * - Provides clean API for state queries and changes
 */

import { BaseComponent } from './BaseComponent';
import type { Cyclist } from '@entities/Cyclist';
import type { ICommand } from '../types/ICommand';
import {
  StateType,
  type ICyclistState,
  type StateTransition,
} from '../types/cyclistState';
import { RidingState } from '@patterns/states/RidingState';
import { CarryingState } from '@patterns/states/CarryingState';
import { RemountingState } from '@patterns/states/RemountingState';
import { CrashedState } from '@patterns/states/CrashedState';

export class StateMachineComponent extends BaseComponent {
  // Map of all available states
  private states: Map<StateType, ICyclistState>;

  // Current active state
  private currentState!: ICyclistState;

  // Transition history for debugging and analytics
  private transitionHistory: StateTransition[] = [];

  // Maximum history length to prevent memory issues
  private readonly MAX_HISTORY_LENGTH = 50;

  // Flag to prevent recursive state changes
  private isTransitioning = false;

  private cyclist: Cyclist;

  constructor(owner: Phaser.GameObjects.GameObject, initialState: StateType = StateType.RIDING) {
    super(owner);
    this.cyclist = owner as Cyclist;

    // Initialize all states
    this.states = new Map<StateType, ICyclistState>([
      [StateType.RIDING, new RidingState()],
      [StateType.CARRYING, new CarryingState()],
      [StateType.REMOUNTING, new RemountingState()],
      [StateType.CRASHED, new CrashedState()],
    ]);

    // Set initial state
    this.initializeState(initialState);
  }

  /**
   * Initialize the state machine with a starting state
   */
  private initializeState(stateType: StateType): void {
    const state = this.states.get(stateType);
    if (!state) {
      console.error(`[StateMachine] State ${stateType} not found`);
      return;
    }

    this.currentState = state;
    this.currentState.enter(this.cyclist);

    // Add initial state to history
    this.addTransitionToHistory({
      fromState: stateType, // First transition has same from/to
      toState: stateType,
      timestamp: Date.now(),
      reason: 'Initial state',
    });
  }

  /**
   * Update the current state
   * Called every frame from the entity's update loop
   */
  public update(_time: number, delta: number): void {
    if (this.currentState) {
      this.currentState.update(this.cyclist, delta);
    }
  }

  /**
   * Handle input through the current state
   * Allows states to filter or modify input behavior
   */
  public handleInput(command: ICommand): void {
    if (this.currentState) {
      this.currentState.handleInput(this.cyclist, command);
    }
  }

  /**
   * Change to a new state
   * Validates transition, calls exit/enter, and logs transition
   *
   * @param newStateType - The state to transition to
   * @param reason - Optional reason for debugging
   * @returns true if transition was successful, false otherwise
   */
  public changeState(newStateType: StateType, reason?: string): boolean {
    // Prevent recursive state changes
    if (this.isTransitioning) {
      console.warn(`[StateMachine] Cannot change state during transition`);
      return false;
    }

    // Check if already in this state
    if (this.currentState.type === newStateType) {
      console.warn(`[StateMachine] Already in state ${newStateType}`);
      return false;
    }

    // Validate transition is allowed
    if (!this.currentState.canTransitionTo(newStateType)) {
      console.warn(
        `[StateMachine] Invalid transition from ${this.currentState.type} to ${newStateType}`
      );
      return false;
    }

    // Get the new state
    const newState = this.states.get(newStateType);
    if (!newState) {
      console.error(`[StateMachine] State ${newStateType} not found`);
      return false;
    }

    // Perform transition
    this.isTransitioning = true;

    const oldStateType = this.currentState.type;

    // Exit old state
    this.currentState.exit(this.cyclist);

    // Switch to new state
    this.currentState = newState;

    // Enter new state
    this.currentState.enter(this.cyclist);

    this.isTransitioning = false;


    // Log transition
    const transition: StateTransition = {

      fromState: oldStateType,
      toState: newStateType,
      timestamp: Date.now(),
      ...(reason !== undefined && { reason }),
    };
    this.addTransitionToHistory(transition);

    console.log(`[StateMachine] Transitioned from ${oldStateType} to ${newStateType}`, reason || '');

    return true;
  }

  /**
   * Get the current state type
   */
  public getCurrentState(): StateType {
    return this.currentState.type;
  }

  /**
   * Check if currently in a specific state
   */
  public isInState(stateType: StateType): boolean {
    return this.currentState.type === stateType;
  }

  /**
   * Check if transition to a state is valid from current state
   */
  public canTransitionTo(stateType: StateType): boolean {
    return this.currentState.canTransitionTo(stateType);
  }

  /**
   * Get transition history
   * Useful for debugging and analytics
   */
  public getTransitionHistory(): readonly StateTransition[] {
    return [...this.transitionHistory];
  }

  /**
   * Get the last N transitions
   */
  public getRecentTransitions(count: number): readonly StateTransition[] {
    const start = Math.max(0, this.transitionHistory.length - count);
    return this.transitionHistory.slice(start);
  }

  /**
   * Clear transition history
   */
  public clearHistory(): void {
    this.transitionHistory = [];
  }

  /**
   * Add a transition to history
   * Maintains maximum history length
   */
  private addTransitionToHistory(transition: StateTransition): void {
    this.transitionHistory.push(transition);

    // Trim history if it exceeds maximum length
    if (this.transitionHistory.length > this.MAX_HISTORY_LENGTH) {
      this.transitionHistory.shift();
    }
  }

  /**
   * Get formatted debug info about current state and recent transitions
   */
  public getDebugInfo(): string {
    const recent = this.getRecentTransitions(5);
    const lines = [
      `Current State: ${this.currentState.type}`,
      `Recent Transitions (${recent.length}):`,
    ];

    recent.forEach((t, i) => {
      const time = new Date(t.timestamp).toLocaleTimeString();
      lines.push(`  ${i + 1}. ${t.fromState} → ${t.toState} (${time}) ${t.reason || ''}`);
    });

    return lines.join('\n');
  }

  /**
   * Clean up when component is destroyed
   */
  public destroy(): void {
    // Exit current state
    if (this.currentState) {
      this.currentState.exit(this.cyclist);
    }

    // Clear references
    this.states.clear();
    this.transitionHistory = [];

    super.destroy();
  }
}
