import type { IObserver } from '@/patterns/observer';
import type { BalanceEventPayload } from '@/types/balance';
import { BalanceEventType } from '@/types/balance';
import type { Cyclist } from '@entities/Cyclist';
import { StateMachineComponent } from '@components/StateMachineComponent';
import { BalanceComponent } from '@components/BalanceComponent';
import { StateType } from '@/types/cyclistState';

/**
 * Observateur qui écoute les événements d'équilibre et déclenche
 * les transitions d'état appropriées (notamment la chute).
 *
 * Connecte le BalanceComponent au StateMachineComponent via Observer Pattern.
 *
 * @example
 * ```typescript
 * // Dans RaceScene.createPlayer()
 * const balanceObserver = new BalanceObserver(this.player, eventBus);
 * ```
 */
export class BalanceObserver implements IObserver<BalanceEventPayload> {
  /** Référence au cycliste */
  private cyclist: Cyclist;

  /**
   * Crée un observateur d'équilibre.
   *
   * @param cyclist - Le cycliste à observer
   * @param eventBus - EventBus pour s'abonner aux événements
   */
  constructor(cyclist: Cyclist, eventBus: import('@/patterns/observer').EventBus) {
    this.cyclist = cyclist;

    // S'abonner aux événements d'équilibre
    eventBus.addObserver(BalanceEventType.FALLING, this);
    eventBus.addObserver(BalanceEventType.RECOVERED, this);
  }

  /**
   * Méthode appelée par l'EventBus lors d'un événement d'équilibre.
   *
   * @param event - Type d'événement
   * @param payload - Données de l'événement
   */
  notify(event: string, payload: BalanceEventPayload): void {
    switch (event) {
      case BalanceEventType.FALLING:
        this.handleFalling();
        break;

      case BalanceEventType.RECOVERED:
        this.handleRecovered();
        break;

      default:
        break;
    }
  }

  /**
   * Gère la chute du cycliste.
   * Déclenche la transition vers le CRASHED state.
   */
  private handleFalling(): void {
    const stateMachine = this.cyclist.getComponent(StateMachineComponent);
    if (!stateMachine) {
      console.warn('[BalanceObserver] StateMachineComponent non trouvé');
      return;
    }

    // Vérifier qu'on n'est pas déjà en train de crasher
    if (stateMachine.isInState(StateType.CRASHED)) {
      return;
    }

    // Transition vers CRASHED
    const success = stateMachine.changeState(StateType.CRASHED, 'Balance fall threshold exceeded');

    if (success) {
      console.log('[BalanceObserver] Chute détectée! Transition vers CRASHED');
    }
  }

  /**
   * Gère la récupération de l'équilibre.
   * Pour l'instant, ne fait rien de spécial.
   */
  private handleRecovered(): void {
    // L'équilibre est récupéré
    // On pourrait ajouter un effet visuel ou audio ici
    console.log('[BalanceObserver] Équilibre récupéré');
  }
}
