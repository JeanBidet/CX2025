import Phaser from 'phaser';
import type { IObservable, IObserver } from './IObserver';

/**
 * EventBus centralisé utilisant Phaser.Events.EventEmitter.
 *
 * Permet la communication découplée entre composants via Observer Pattern.
 * Utilise Phaser EventEmitter en interne pour bénéficier des optimisations Phaser.
 *
 * @example
 * ```typescript
 * // Créer un EventBus
 * const eventBus = new EventBus();
 *
 * // Créer un observer
 * const observer: IObserver = {
 *   notify(event, payload) {
 *     console.log(`Événement ${event}:`, payload);
 *   }
 * };
 *
 * // S'abonner
 * eventBus.addObserver('player:scored', observer);
 *
 * // Émettre
 * eventBus.notifyObservers('player:scored', { points: 100 });
 * ```
 */
export class EventBus implements IObservable {
  /** Émetteur Phaser sous-jacent */
  private emitter: Phaser.Events.EventEmitter;

  /** Map pour garder trace des observers et leurs callbacks */
  private observerCallbacks: Map<string, Map<IObserver, Function>>;

  constructor() {
    this.emitter = new Phaser.Events.EventEmitter();
    this.observerCallbacks = new Map();
  }

  /**
   * Ajoute un observateur pour un événement.
   *
   * @param event - Type d'événement
   * @param observer - Observateur à ajouter
   */
  addObserver(event: string, observer: IObserver): void {
    // Créer le callback wrapper
    const callback = (payload: any) => {
      observer.notify(event, payload);
    };

    // Stocker la relation observer -> callback
    if (!this.observerCallbacks.has(event)) {
      this.observerCallbacks.set(event, new Map());
    }
    this.observerCallbacks.get(event)!.set(observer, callback);

    // S'abonner à l'événement Phaser
    this.emitter.on(event, callback);
  }

  /**
   * Retire un observateur pour un événement.
   *
   * @param event - Type d'événement
   * @param observer - Observateur à retirer
   */
  removeObserver(event: string, observer: IObserver): void {
    const eventObservers = this.observerCallbacks.get(event);
    if (!eventObservers) {
      return;
    }

    const callback = eventObservers.get(observer);
    if (callback) {
      this.emitter.off(event, callback as any);
      eventObservers.delete(observer);
    }
  }

  /**
   * Notifie tous les observateurs d'un événement.
   *
   * @param event - Type d'événement
   * @param payload - Données à transmettre
   */
  notifyObservers(event: string, payload: any): void {
    this.emitter.emit(event, payload);
  }

  /**
   * Retire tous les observateurs d'un événement.
   *
   * @param event - Type d'événement (optionnel, si omis retire tous les événements)
   */
  removeAllObservers(event?: string): void {
    if (event) {
      this.emitter.removeAllListeners(event);
      this.observerCallbacks.delete(event);
    } else {
      this.emitter.removeAllListeners();
      this.observerCallbacks.clear();
    }
  }

  /**
   * Vérifie si un événement a des observateurs.
   *
   * @param event - Type d'événement
   * @returns true si au moins un observateur existe
   */
  hasObservers(event: string): boolean {
    return this.emitter.listenerCount(event) > 0;
  }

  /**
   * Détruit l'EventBus et nettoie toutes les ressources.
   */
  destroy(): void {
    this.removeAllObservers();
    this.emitter.destroy();
  }
}

/**
 * EventBus global pour l'application.
 * Utilisez cette instance pour la communication inter-composants globale.
 */
export const globalEventBus = new EventBus();
