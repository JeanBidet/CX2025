import { BaseComponent } from './BaseComponent';
import type { Cyclist } from '@entities/Cyclist';
import type { EventBus } from '@/patterns/observer';
import type {
  EnduranceState,
  EnduranceZone,
  EnduranceZoneConfig,
  EnduranceEventPayload,
} from '@/types/endurance';
import { EnduranceEventType } from '@/types/endurance';
import {
  ENDURANCE_MAX,
  ENDURANCE_INITIAL,
  ENDURANCE_DRAIN_RATE_BASE,
  ENDURANCE_DRAIN_RATE_ACCELERATE,
  ENDURANCE_DRAIN_RATE_SPRINT,
  ENDURANCE_RECOVERY_RATE,
  ENDURANCE_REST_SPEED_THRESHOLD,
  ENDURANCE_SPRINT_ACTIVATION_COST,
  ENDURANCE_ZONE_GREEN_THRESHOLD,
  ENDURANCE_ZONE_YELLOW_THRESHOLD,
  ENDURANCE_ZONE_COLORS,
  ENDURANCE_SPEED_MULTIPLIER_GREEN,
  ENDURANCE_SPEED_MULTIPLIER_YELLOW,
  ENDURANCE_SPEED_MULTIPLIER_RED,
} from '@config/constants';

/**
 * Composant gérant l'endurance du cycliste.
 *
 * Responsabilités :
 * - Gérer la barre d'endurance (0-100)
 * - Dégradation progressive pendant l'effort (accélération, sprint)
 * - Récupération automatique au repos
 * - Calcul de la zone d'endurance (verte/jaune/rouge)
 * - Calcul du multiplicateur de vitesse selon la zone
 * - Émission d'événements via Observer Pattern
 *
 * @example
 * ```typescript
 * const endurance = new EnduranceComponent(cyclist, eventBus);
 * cyclist.addComponent(endurance);
 *
 * // Pendant l'accélération
 * endurance.drainAccelerate(delta);
 *
 * // Pendant le sprint
 * if (endurance.canSprint()) {
 *   endurance.activateSprint();
 * }
 *
 * // Récupération automatique au repos
 * // (géré automatiquement dans update())
 * ```
 */
export class EnduranceComponent extends BaseComponent {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Référence au cycliste (typée) */
  private cyclist: Cyclist;

  /** EventBus pour émettre les événements */
  private eventBus?: EventBus;

  /** État actuel de l'endurance */
  private state: EnduranceState;

  /** Zone d'endurance actuelle */
  private currentZone: EnduranceZone;

  /** Configuration des zones d'endurance */
  private readonly zoneConfigs: Record<EnduranceZone, EnduranceZoneConfig>;

  /** Indique si le cycliste est en train de sprinter */
  private isSprinting: boolean = false;

  /** Indique si le cycliste est en train d'accélérer */
  private isAccelerating: boolean = false;

  // ============================================================================
  // CONSTRUCTEUR
  // ============================================================================

  /**
   * Crée un nouveau composant d'endurance.
   *
   * @param owner - Le cycliste propriétaire
   * @param eventBus - EventBus pour émettre les événements (optionnel)
   */
  constructor(owner: Phaser.GameObjects.GameObject, eventBus?: EventBus) {
    super(owner);
    this.cyclist = owner as Cyclist;
    this.eventBus = eventBus;

    // Initialiser l'état
    this.state = {
      current: ENDURANCE_INITIAL,
      max: ENDURANCE_MAX,
      drainRate: 0,
      recoveryRate: ENDURANCE_RECOVERY_RATE,
      isExhausted: false,
      isRecovering: false,
    };

    // Configuration des zones avec couleurs et multiplicateurs
    this.zoneConfigs = {
      GREEN: {
        threshold: ENDURANCE_ZONE_GREEN_THRESHOLD,
        color: ENDURANCE_ZONE_COLORS.GREEN,
        speedMultiplier: ENDURANCE_SPEED_MULTIPLIER_GREEN,
      },
      YELLOW: {
        threshold: ENDURANCE_ZONE_YELLOW_THRESHOLD,
        color: ENDURANCE_ZONE_COLORS.YELLOW,
        speedMultiplier: ENDURANCE_SPEED_MULTIPLIER_YELLOW,
      },
      RED: {
        threshold: 0,
        color: ENDURANCE_ZONE_COLORS.RED,
        speedMultiplier: ENDURANCE_SPEED_MULTIPLIER_RED,
      },
    };

    // Déterminer la zone initiale
    this.currentZone = this.calculateZone();
  }

  // ============================================================================
  // INITIALISATION
  // ============================================================================

  /**
   * Initialise le composant.
   */
  init(): void {
    console.log('[EnduranceComponent] Initialisé');
    this.emitEvent(EnduranceEventType.CHANGED);
  }

  // ============================================================================
  // UPDATE
  // ============================================================================

  /**
   * Met à jour l'endurance chaque frame.
   *
   * Gère la récupération automatique au repos.
   *
   * @param _time - Temps total écoulé (ms)
   * @param delta - Temps écoulé depuis la dernière frame (ms)
   */
  update(_time: number, delta: number): void {
    if (!this.active) {
      return;
    }

    const deltaSeconds = delta / 1000;

    // Vérifier si le cycliste est au repos
    const movement = this.cyclist.getComponent(require('./MovementComponent').MovementComponent);
    const isResting = movement ? movement.getSpeed() < ENDURANCE_REST_SPEED_THRESHOLD : false;

    // Récupération automatique au repos
    if (isResting && !this.state.isExhausted) {
      this.recover(deltaSeconds);
    }

    // Vérifier si épuisé
    if (this.state.current <= 0 && !this.state.isExhausted) {
      this.state.isExhausted = true;
      this.emitEvent(EnduranceEventType.EXHAUSTED);
      console.log('[EnduranceComponent] Cycliste épuisé!');
    } else if (this.state.current > 0 && this.state.isExhausted) {
      this.state.isExhausted = false;
    }
  }

  // ============================================================================
  // MÉTHODES PUBLIQUES - DRAIN
  // ============================================================================

  /**
   * Drain l'endurance pendant l'accélération normale.
   *
   * @param deltaSeconds - Temps écoulé (secondes)
   */
  public drainAccelerate(deltaSeconds: number): void {
    if (this.state.isExhausted) {
      return;
    }

    const drain = ENDURANCE_DRAIN_RATE_ACCELERATE * deltaSeconds;
    this.drain(drain);
    this.isAccelerating = true;
  }

  /**
   * Drain l'endurance pendant le sprint.
   *
   * @param deltaSeconds - Temps écoulé (secondes)
   */
  public drainSprint(deltaSeconds: number): void {
    if (this.state.isExhausted) {
      // Désactiver le sprint si épuisé
      if (this.isSprinting) {
        this.deactivateSprint();
      }
      return;
    }

    const drain = ENDURANCE_DRAIN_RATE_SPRINT * deltaSeconds;
    this.drain(drain);
  }

  /**
   * Drain l'endurance d'une quantité arbitraire.
   *
   * @param amount - Quantité à drainer
   */
  public drain(amount: number): void {
    const previousValue = this.state.current;
    this.state.current = Math.max(0, this.state.current - amount);
    this.state.drainRate = amount;

    if (this.state.current !== previousValue) {
      this.checkZoneChange();
      this.emitEvent(EnduranceEventType.CHANGED);
    }
  }

  /**
   * Arrête le drain d'accélération.
   */
  public stopDrainAccelerate(): void {
    this.isAccelerating = false;
    this.state.drainRate = 0;
  }

  // ============================================================================
  // MÉTHODES PUBLIQUES - RÉCUPÉRATION
  // ============================================================================

  /**
   * Récupère de l'endurance.
   *
   * @param deltaSeconds - Temps écoulé (secondes)
   */
  public recover(deltaSeconds: number): void {
    if (this.state.current >= this.state.max) {
      this.state.isRecovering = false;
      return;
    }

    if (!this.state.isRecovering) {
      this.state.isRecovering = true;
      this.emitEvent(EnduranceEventType.RECOVERY_STARTED);
    }

    const previousValue = this.state.current;
    const recovery = this.state.recoveryRate * deltaSeconds;
    this.state.current = Math.min(this.state.max, this.state.current + recovery);

    if (this.state.current !== previousValue) {
      this.checkZoneChange();
      this.emitEvent(EnduranceEventType.CHANGED);
    }

    // Vérifier si récupération complète
    if (this.state.current >= this.state.max) {
      this.state.isRecovering = false;
      this.emitEvent(EnduranceEventType.RECOVERY_COMPLETED);
      console.log('[EnduranceComponent] Récupération complète');
    }
  }

  // ============================================================================
  // MÉTHODES PUBLIQUES - SPRINT
  // ============================================================================

  /**
   * Vérifie si le cycliste peut sprinter.
   *
   * @returns true si le sprint est possible
   */
  public canSprint(): boolean {
    return this.state.current >= ENDURANCE_SPRINT_ACTIVATION_COST && !this.state.isExhausted;
  }

  /**
   * Active le sprint.
   *
   * @returns true si le sprint a été activé
   */
  public activateSprint(): boolean {
    if (!this.canSprint() || this.isSprinting) {
      return false;
    }

    // Coût d'activation
    this.drain(ENDURANCE_SPRINT_ACTIVATION_COST);

    this.isSprinting = true;
    this.emitEvent(EnduranceEventType.SPRINT_ACTIVATED);
    console.log('[EnduranceComponent] Sprint activé');

    return true;
  }

  /**
   * Désactive le sprint.
   */
  public deactivateSprint(): void {
    if (!this.isSprinting) {
      return;
    }

    this.isSprinting = false;
    this.emitEvent(EnduranceEventType.SPRINT_DEACTIVATED);
    console.log('[EnduranceComponent] Sprint désactivé');
  }

  /**
   * Vérifie si le cycliste est en train de sprinter.
   *
   * @returns true si en sprint
   */
  public isSprinting_(): boolean {
    return this.isSprinting;
  }

  // ============================================================================
  // MÉTHODES PUBLIQUES - GETTERS
  // ============================================================================

  /**
   * Récupère l'état actuel de l'endurance.
   *
   * @returns État d'endurance
   */
  public getState(): Readonly<EnduranceState> {
    return { ...this.state };
  }

  /**
   * Récupère la valeur actuelle d'endurance.
   *
   * @returns Valeur actuelle (0-100)
   */
  public getCurrent(): number {
    return this.state.current;
  }

  /**
   * Récupère le pourcentage d'endurance.
   *
   * @returns Pourcentage (0-1)
   */
  public getPercentage(): number {
    return this.state.current / this.state.max;
  }

  /**
   * Récupère la zone d'endurance actuelle.
   *
   * @returns Zone actuelle
   */
  public getZone(): EnduranceZone {
    return this.currentZone;
  }

  /**
   * Récupère la configuration de la zone actuelle.
   *
   * @returns Configuration de zone
   */
  public getZoneConfig(): EnduranceZoneConfig {
    return this.zoneConfigs[this.currentZone];
  }

  /**
   * Récupère le multiplicateur de vitesse selon la zone actuelle.
   *
   * @returns Multiplicateur (0-1)
   */
  public getSpeedMultiplier(): number {
    return this.getZoneConfig().speedMultiplier;
  }

  /**
   * Vérifie si le cycliste est épuisé.
   *
   * @returns true si épuisé
   */
  public isExhausted(): boolean {
    return this.state.isExhausted;
  }

  /**
   * Vérifie si le cycliste est en récupération.
   *
   * @returns true si en récupération
   */
  public isRecovering_(): boolean {
    return this.state.isRecovering;
  }

  // ============================================================================
  // MÉTHODES PRIVÉES
  // ============================================================================

  /**
   * Calcule la zone d'endurance selon la valeur actuelle.
   *
   * @returns Zone calculée
   */
  private calculateZone(): EnduranceZone {
    const percentage = this.getPercentage();

    if (percentage >= ENDURANCE_ZONE_GREEN_THRESHOLD) {
      return 'GREEN';
    } else if (percentage >= ENDURANCE_ZONE_YELLOW_THRESHOLD) {
      return 'YELLOW';
    } else {
      return 'RED';
    }
  }

  /**
   * Vérifie si la zone a changé et émet l'événement approprié.
   */
  private checkZoneChange(): void {
    const newZone = this.calculateZone();

    if (newZone !== this.currentZone) {
      const previousZone = this.currentZone;
      this.currentZone = newZone;

      this.emitEvent(EnduranceEventType.ZONE_CHANGED, {
        zone: newZone,
        previousZone,
      });

      console.log(`[EnduranceComponent] Zone changée: ${previousZone} -> ${newZone}`);
    }
  }

  /**
   * Émet un événement via l'EventBus.
   *
   * @param event - Type d'événement
   * @param additionalPayload - Données additionnelles (optionnel)
   */
  private emitEvent(event: EnduranceEventType, additionalPayload?: Partial<EnduranceEventPayload>): void {
    if (!this.eventBus) {
      return;
    }

    const payload: EnduranceEventPayload = {
      state: this.getState(),
      zone: this.currentZone,
      ...additionalPayload,
    };

    this.eventBus.notifyObservers(event, payload);
  }

  // ============================================================================
  // DESTRUCTION
  // ============================================================================

  /**
   * Nettoie le composant.
   */
  destroy(): void {
    this.isSprinting = false;
    this.isAccelerating = false;
    console.log('[EnduranceComponent] Détruit');
  }
}
