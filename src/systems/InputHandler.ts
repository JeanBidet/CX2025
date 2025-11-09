import Phaser from 'phaser';
import type { IGameCommand } from '../types/IGameCommand';
import { GameAction, type KeyBindingScheme, ACTIVE_KEY_BINDINGS } from '@config/keyBindings';
import {
  AccelerateCommand,
  BrakeCommand,
  TurnLeftCommand,
  TurnRightCommand,
  SprintCommand,
  NullCommand,
} from '../patterns/commands';

/**
 * Gestionnaire d'input basé sur le Command Pattern.
 *
 * Responsabilités :
 * - Map les touches Phaser aux actions de jeu
 * - Map les actions aux commandes concrètes
 * - Retourne les commandes actives à chaque frame
 * - Permet le remapping dynamique des touches
 *
 * Avantages :
 * - Découplage total entre input et logique métier
 * - Remapping des touches sans modifier le code
 * - Testabilité (on peut injecter des commandes mock)
 * - Réutilisabilité (IA peut utiliser les mêmes commandes)
 * - Replay (enregistrement de séquences de commandes)
 *
 * @example
 * ```typescript
 * // Dans RaceScene.create()
 * const inputHandler = new InputHandler(this);
 *
 * // Dans RaceScene.update()
 * const commands = inputHandler.getActiveCommands();
 * commands.forEach(cmd => cmd.execute(player, delta));
 * ```
 */
export class InputHandler {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Référence à la scène Phaser */
  private scene: Phaser.Scene;

  /** Map des touches Phaser créées */
  private keys: Map<number, Phaser.Input.Keyboard.Key>;

  /** Map action → commande */
  private commandMap: Map<GameAction, IGameCommand>;

  /** Schéma de contrôle actuel */
  private keyBindings: KeyBindingScheme;

  /** Commandes actives (réutilisées pour éviter allocations) */
  private activeCommands: IGameCommand[] = [];

  // ============================================================================
  // CONSTRUCTEUR
  // ============================================================================

  /**
   * Crée un nouveau gestionnaire d'input.
   *
   * @param scene - La scène Phaser propriétaire
   * @param customBindings - Schéma de contrôle personnalisé (optionnel)
   */
  constructor(scene: Phaser.Scene, customBindings?: KeyBindingScheme) {
    this.scene = scene;
    this.keys = new Map();
    this.commandMap = new Map();
    this.keyBindings = customBindings ?? ACTIVE_KEY_BINDINGS;

    // Initialiser les commandes
    this.initializeCommands();

    // Enregistrer les touches Phaser
    this.registerKeys();

    console.log('[InputHandler] Initialisé avec', this.commandMap.size, 'commandes');
  }

  // ============================================================================
  // INITIALISATION
  // ============================================================================

  /**
   * Initialise la map action → commande.
   *
   * Ici, on crée les instances de commandes et on les associe aux actions.
   * C'est ici qu'on peut configurer les paramètres des commandes.
   */
  private initializeCommands(): void {
    this.commandMap.set(GameAction.ACCELERATE, new AccelerateCommand());
    this.commandMap.set(GameAction.BRAKE, new BrakeCommand());
    this.commandMap.set(GameAction.TURN_LEFT, new TurnLeftCommand());
    this.commandMap.set(GameAction.TURN_RIGHT, new TurnRightCommand());
    this.commandMap.set(GameAction.SPRINT, new SprintCommand(true));

    // Actions futures (pas encore implémentées)
    this.commandMap.set(GameAction.JUMP, NullCommand.getInstance());
    this.commandMap.set(GameAction.DISMOUNT, NullCommand.getInstance());
  }

  /**
   * Enregistre toutes les touches nécessaires auprès de Phaser.
   *
   * Parcourt le schéma de contrôle et crée les touches Phaser correspondantes.
   */
  private registerKeys(): void {
    const keyboard = this.scene.input.keyboard;
    if (!keyboard) {
      throw new Error('[InputHandler] Clavier non disponible');
    }

    // Parcourir toutes les actions
    Object.values(GameAction).forEach(action => {
      const keyCodes = this.keyBindings[action];

      // Pour chaque KeyCode associé à cette action
      keyCodes.forEach(keyCode => {
        // Si cette touche n'est pas encore enregistrée
        if (!this.keys.has(keyCode)) {
          const key = keyboard.addKey(keyCode, false); // false = pas d'émission d'événements
          this.keys.set(keyCode, key);
        }
      });
    });

    console.log('[InputHandler]', this.keys.size, 'touches enregistrées');
  }

  // ============================================================================
  // LECTURE DES INPUTS
  // ============================================================================

  /**
   * Récupère la liste des commandes actives selon les touches pressées.
   *
   * Cette méthode doit être appelée chaque frame (dans update).
   *
   * @returns Liste des commandes à exécuter
   */
  public getActiveCommands(): IGameCommand[] {
    // Vider la liste des commandes actives
    this.activeCommands.length = 0;

    // Pour chaque action, vérifier si une touche associée est pressée
    Object.values(GameAction).forEach(action => {
      if (this.isActionActive(action)) {
        const command = this.commandMap.get(action);
        if (command) {
          this.activeCommands.push(command);
        }
      }
    });

    return this.activeCommands;
  }

  /**
   * Vérifie si une action est actuellement active (touche pressée).
   *
   * @param action - L'action à vérifier
   * @returns true si au moins une touche associée est pressée
   */
  public isActionActive(action: GameAction): boolean {
    const keyCodes = this.keyBindings[action];

    // Vérifier si au moins une des touches associées est pressée
    return keyCodes.some(keyCode => {
      const key = this.keys.get(keyCode);
      return key?.isDown ?? false;
    });
  }

  /**
   * Vérifie si une action vient d'être déclenchée (touche pressée ce frame).
   *
   * @param action - L'action à vérifier
   * @returns true si au moins une touche associée vient d'être pressée
   */
  public isActionJustPressed(action: GameAction): boolean {
    const keyCodes = this.keyBindings[action];

    return keyCodes.some(keyCode => {
      const key = this.keys.get(keyCode);
      return Phaser.Input.Keyboard.JustDown(key!);
    });
  }

  /**
   * Vérifie si une action vient d'être relâchée (touche relâchée ce frame).
   *
   * @param action - L'action à vérifier
   * @returns true si au moins une touche associée vient d'être relâchée
   */
  public isActionJustReleased(action: GameAction): boolean {
    const keyCodes = this.keyBindings[action];

    return keyCodes.some(keyCode => {
      const key = this.keys.get(keyCode);
      return Phaser.Input.Keyboard.JustUp(key!);
    });
  }

  // ============================================================================
  // REMAPPING DYNAMIQUE
  // ============================================================================

  /**
   * Change le schéma de contrôle à chaud.
   *
   * @param newBindings - Le nouveau schéma de contrôle
   */
  public setKeyBindings(newBindings: KeyBindingScheme): void {
    this.keyBindings = newBindings;

    // Ré-enregistrer les touches
    this.keys.clear();
    this.registerKeys();

    console.log('[InputHandler] Schéma de contrôle mis à jour');
  }

  /**
   * Remplace la commande associée à une action.
   *
   * Utile pour customiser le comportement sans changer les touches.
   *
   * @param action - L'action à modifier
   * @param command - La nouvelle commande
   */
  public setCommand(action: GameAction, command: IGameCommand): void {
    this.commandMap.set(action, command);
    console.log(`[InputHandler] Commande '${command.name}' assignée à '${action}'`);
  }

  // ============================================================================
  // NETTOYAGE
  // ============================================================================

  /**
   * Détruit le gestionnaire d'input et libère les ressources.
   */
  public destroy(): void {
    this.keys.clear();
    this.commandMap.clear();
    this.activeCommands = [];
    console.log('[InputHandler] Détruit');
  }
}
