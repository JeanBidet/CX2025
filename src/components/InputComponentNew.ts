import Phaser from 'phaser';
import { BaseComponent } from './BaseComponent';
import type { Cyclist } from '@entities/Cyclist';
import type { InputHandler } from '@/systems/InputHandler';
import type { IGameCommand } from '../types/IGameCommand';
import { GameAction } from '@config/keyBindings';
import { MovementComponent } from './MovementComponent';

/**
 * Composant d'input refactorisé avec le Command Pattern.
 *
 * Responsabilités :
 * - Récupère les commandes actives depuis l'InputHandler
 * - Exécute ces commandes sur le cycliste propriétaire
 * - Gère les priorités si plusieurs commandes conflictuelles
 *
 * Avantages du Command Pattern :
 * 1. **Découplage** : Ne connaît pas les touches, seulement les commandes
 * 2. **Testabilité** : On peut injecter des commandes mock pour tester
 * 3. **Réutilisabilité** : L'IA peut utiliser le même composant avec d'autres commandes
 * 4. **Extensibilité** : Ajout de nouvelles commandes sans modifier ce code
 *
 * @example
 * ```typescript
 * const cyclist = new Cyclist(scene, x, y, true);
 * const inputHandler = new InputHandler(scene);
 * const inputComponent = new InputComponentNew(cyclist, inputHandler);
 * cyclist.addComponent(inputComponent);
 *
 * // Dans update
 * inputComponent.update(time, delta); // Exécute automatiquement les commandes
 * ```
 */
export class InputComponentNew extends BaseComponent {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Référence au cycliste (typée) */
  private cyclist: Cyclist;

  /** Référence à l'InputHandler partagé */
  private inputHandler: InputHandler;

  /** Liste des commandes à exécuter ce frame (cache) */
  private commandsToExecute: IGameCommand[] = [];

  // ============================================================================
  // CONSTRUCTEUR
  // ============================================================================

  /**
   * Crée un nouveau composant d'input basé sur les commandes.
   *
   * @param owner - Le cycliste propriétaire
   * @param inputHandler - Le gestionnaire d'input partagé
   */
  constructor(owner: Phaser.GameObjects.GameObject, inputHandler: InputHandler) {
    super(owner);
    this.cyclist = owner as Cyclist;
    this.inputHandler = inputHandler;
  }

  // ============================================================================
  // INITIALISATION
  // ============================================================================

  /**
   * Initialise le composant.
   */
  init(): void {
    console.log('[InputComponentNew] Initialisé avec Command Pattern');
  }

  // ============================================================================
  // UPDATE
  // ============================================================================

  /**
   * Récupère et exécute les commandes actives chaque frame.
   *
   * @param _time - Temps total écoulé (non utilisé)
   * @param delta - Temps écoulé depuis la dernière frame (ms)
   */
  update(_time: number, delta: number): void {
    if (!this.active) {
      return;
    }

    // Récupérer les commandes actives depuis l'InputHandler
    this.commandsToExecute = this.inputHandler.getActiveCommands();

    // Trier par priorité (décroissante)
    this.commandsToExecute.sort((a, b) => {
      const priorityA = a.priority ?? 0;
      const priorityB = b.priority ?? 0;
      return priorityB - priorityA; // Décroissant
    });

    // Exécuter toutes les commandes
    this.commandsToExecute.forEach(command => {
      command.execute(this.cyclist, delta);
    });

    // S'il n'y a pas de commande d'accélération ou de freinage,
    // réinitialiser l'accélération (pour laisser le drag agir)
    if (!this.hasMovementCommand()) {
      this.resetAcceleration();
    }

    // Gérer le relâchement du sprint (désactivation)
    this.handleSprintRelease();
  }

  // ============================================================================
  // MÉTHODES PRIVÉES
  // ============================================================================

  /**
   * Vérifie si une commande de mouvement (accélération/freinage) est active.
   *
   * @returns true si au moins une commande de mouvement est présente
   */
  private hasMovementCommand(): boolean {
    return this.commandsToExecute.some(
      cmd => cmd.name === 'Accelerate' || cmd.name === 'Brake'
    );
  }

  /**
   * Réinitialise l'accélération à 0 (pour laisser le drag agir).
   */
  private resetAcceleration(): void {
    const body = this.cyclist.getBody();
    body.setAcceleration(0, 0);
  }

  /**
   * Gère le relâchement de la touche de sprint.
   *
   * Quand SPRINT est relâché, on désactive le sprint dans le MovementComponent.
   * Ceci est nécessaire car SprintCommand n'est plus dans la liste des commandes
   * actives quand la touche est relâchée, donc le sprint resterait actif sinon.
   */
  private handleSprintRelease(): void {
    // Vérifier si SPRINT vient d'être relâché
    if (this.inputHandler.isActionJustReleased(GameAction.SPRINT)) {
      // Récupérer le MovementComponent
      const movement = this.cyclist.getComponent(MovementComponent);

      if (movement) {
        // Désactiver le sprint
        movement.setSprinting(false);
      }
    }
  }

  // ============================================================================
  // MÉTHODES PUBLIQUES
  // ============================================================================

  /**
   * Active ou désactive les contrôles.
   *
   * @param enabled - true pour activer, false pour désactiver
   */
  public setEnabled(enabled: boolean): void {
    this.setActive(enabled);

    // Si désactivé, réinitialiser l'accélération
    if (!enabled) {
      this.resetAcceleration();
    }
  }

  /**
   * Récupère la référence à l'InputHandler.
   *
   * @returns L'InputHandler
   */
  public getInputHandler(): InputHandler {
    return this.inputHandler;
  }

  // ============================================================================
  // DESTRUCTION
  // ============================================================================

  /**
   * Nettoie le composant.
   */
  destroy(): void {
    this.resetAcceleration();
    this.commandsToExecute = [];
    console.log('[InputComponentNew] Détruit');
  }
}
