/**
 * Observer Pattern exports.
 *
 * Fournit les interfaces et implémentations pour le pattern Observer
 * permettant une communication découplée entre composants.
 */

export { IObserver, IObservable } from './IObserver';
export { EventBus, globalEventBus } from './EventBus';
