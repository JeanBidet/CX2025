/**
 * Interface pour l'Observer Pattern.
 * Définit le contrat pour les observateurs qui écoutent les événements.
 */

/**
 * Observateur générique.
 * @template T - Type du payload de l'événement
 */
export interface IObserver<T = any> {
  /**
   * Méthode appelée lorsque l'événement observé se produit.
   * @param event - Type de l'événement
   * @param payload - Données associées à l'événement
   */
  notify(event: string, payload: T): void;
}

/**
 * Subject observable (émetteur d'événements).
 */
export interface IObservable {
  /**
   * Ajoute un observateur pour un type d'événement.
   * @param event - Type d'événement à observer
   * @param observer - Observateur à ajouter
   */
  addObserver(event: string, observer: IObserver): void;

  /**
   * Retire un observateur pour un type d'événement.
   * @param event - Type d'événement
   * @param observer - Observateur à retirer
   */
  removeObserver(event: string, observer: IObserver): void;

  /**
   * Notifie tous les observateurs d'un événement.
   * @param event - Type d'événement
   * @param payload - Données à transmettre
   */
  notifyObservers(event: string, payload: any): void;
}
