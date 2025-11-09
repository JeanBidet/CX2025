import Phaser from 'phaser';
import type { IComponent } from '@/types/IComponent';

/**
 * Classe de base abstraite pour tous les composants métier.
 * Implémente l'interface IComponent avec des méthodes par défaut.
 *
 * Les composants concrets héritent de cette classe et surchargent
 * uniquement les méthodes dont ils ont besoin.
 *
 * @abstract
 */
export abstract class BaseComponent implements IComponent {
  /**
   * Référence au GameObject Phaser propriétaire de ce composant.
   */
  public readonly owner: Phaser.GameObjects.GameObject;

  /**
   * Indique si le composant est actif.
   * Un composant inactif ne sera pas mis à jour.
   */
  protected active: boolean = true;

  /**
   * Crée un nouveau composant.
   *
   * @param owner - Le GameObject Phaser qui possède ce composant
   */
  constructor(owner: Phaser.GameObjects.GameObject) {
    this.owner = owner;
  }

  // ============================================================================
  // INTERFACE ICOMPONENT
  // ============================================================================

  /**
   * Initialise le composant après sa création.
   * Implémentation par défaut : ne fait rien.
   * Les classes filles peuvent surcharger cette méthode.
   */
  init(): void {
    // Implémentation par défaut vide
  }

  /**
   * Logique exécutée avant le update principal.
   * Implémentation par défaut : ne fait rien.
   * Les classes filles peuvent surcharger cette méthode.
   *
   * @param _time - Temps total écoulé depuis le début du jeu (ms)
   * @param _delta - Temps écoulé depuis la dernière frame (ms)
   */
  preUpdate(_time: number, _delta: number): void {
    // Implémentation par défaut vide
  }

  /**
   * Logique principale du composant, appelée chaque frame.
   * Implémentation par défaut : ne fait rien.
   * Les classes filles DOIVENT surcharger cette méthode.
   *
   * @param time - Temps total écoulé depuis le début du jeu (ms)
   * @param delta - Temps écoulé depuis la dernière frame (ms)
   */
  abstract update(time: number, delta: number): void;

  /**
   * Nettoie le composant avant sa destruction.
   * Implémentation par défaut : ne fait rien.
   * Les classes filles peuvent surcharger cette méthode.
   */
  destroy(): void {
    // Implémentation par défaut vide
  }

  // ============================================================================
  // MÉTHODES UTILITAIRES
  // ============================================================================

  /**
   * Active le composant.
   * Un composant actif est mis à jour chaque frame.
   */
  public setActive(active: boolean): void {
    this.active = active;
  }

  /**
   * Vérifie si le composant est actif.
   */
  public isActive(): boolean {
    return this.active;
  }

  /**
   * Récupère le propriétaire castée en type spécifique.
   * Utile pour accéder aux propriétés spécifiques du GameObject.
   *
   * @template T - Type du GameObject attendu
   * @returns Le propriétaire casté en type T
   */
  protected getOwnerAs<T extends Phaser.GameObjects.GameObject>(): T {
    return this.owner as T;
  }
}
