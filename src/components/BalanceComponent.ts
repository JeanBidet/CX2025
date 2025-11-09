import { BaseComponent } from './BaseComponent';
import type { Cyclist } from '@entities/Cyclist';
import type { EventBus } from '@/patterns/observer';
import type {
  BalanceState,
  BalanceLevel,
  BalanceLevelConfig,
  BalancePerturbation,
  BalanceEventPayload,
} from '@/types/balance';
import { BalanceEventType, BalancePerturbationType } from '@/types/balance';
import {
  BALANCE_MIN,
  BALANCE_MAX,
  BALANCE_INITIAL,
  BALANCE_RECOVERY_RATE,
  BALANCE_CRITICAL_THRESHOLD,
  BALANCE_FALL_THRESHOLD,
  BALANCE_PERTURBATION_COOLDOWN,
  BALANCE_LEVEL_BALANCED_THRESHOLD,
  BALANCE_LEVEL_SLIGHTLY_THRESHOLD,
  BALANCE_LEVEL_VERY_THRESHOLD,
  BALANCE_OSCILLATION_INTENSITY,
  BALANCE_LEVEL_COLORS,
  BALANCE_OSCILLATION_SPEED,
} from '@config/constants';

/**
 * Composant gérant l'équilibre du cycliste.
 *
 * Responsabilités :
 * - Gérer la barre d'équilibre (-100 à +100, 0 = équilibré)
 * - Récupération automatique vers l'équilibre
 * - Appliquer des perturbations (obstacles, virages, terrain)
 * - Calculer le niveau de déséquilibre (équilibré/légèrement/très/critique)
 * - Détecter la chute si déséquilibre trop important
 * - Fournir les données pour l'oscillation visuelle du sprite
 * - Émission d'événements via Observer Pattern
 *
 * @example
 * ```typescript
 * const balance = new BalanceComponent(cyclist, eventBus);
 * cyclist.addComponent(balance);
 *
 * // Appliquer une perturbation
 * balance.applyPerturbation({
 *   type: BalancePerturbationType.OBSTACLE,
 *   magnitude: 30,
 *   direction: 1,
 * });
 *
 * // Vérifier l'oscillation pour le rendu
 * const oscillation = balance.getOscillationAngle(time);
 * ```
 */
export class BalanceComponent extends BaseComponent {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Référence au cycliste (typée) */
  private cyclist: Cyclist;

  /** EventBus pour émettre les événements */
  private eventBus?: EventBus;

  /** État actuel de l'équilibre */
  private state: BalanceState;

  /** Niveau d'équilibre actuel */
  private currentLevel: BalanceLevel;

  /** Configuration des niveaux d'équilibre */
  private readonly levelConfigs: Record<BalanceLevel, BalanceLevelConfig>;

  /** Timestamp de la dernière perturbation (pour cooldown) */
  private lastPerturbationTime: number = 0;

  /** Accumulateur de temps pour l'oscillation */
  private oscillationTime: number = 0;

  // ============================================================================
  // CONSTRUCTEUR
  // ============================================================================

  /**
   * Crée un nouveau composant d'équilibre.
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
      current: BALANCE_INITIAL,
      min: BALANCE_MIN,
      max: BALANCE_MAX,
      recoveryRate: BALANCE_RECOVERY_RATE,
      isFalling: false,
      direction: 0,
    };

    // Configuration des niveaux avec couleurs et intensités
    this.levelConfigs = {
      BALANCED: {
        threshold: BALANCE_LEVEL_BALANCED_THRESHOLD,
        color: BALANCE_LEVEL_COLORS.BALANCED,
        oscillationIntensity: BALANCE_OSCILLATION_INTENSITY.BALANCED,
        recoveryModifier: 1.0,
      },
      SLIGHTLY_UNBALANCED: {
        threshold: BALANCE_LEVEL_SLIGHTLY_THRESHOLD,
        color: BALANCE_LEVEL_COLORS.SLIGHTLY,
        oscillationIntensity: BALANCE_OSCILLATION_INTENSITY.SLIGHTLY,
        recoveryModifier: 0.9,
      },
      VERY_UNBALANCED: {
        threshold: BALANCE_LEVEL_VERY_THRESHOLD,
        color: BALANCE_LEVEL_COLORS.VERY,
        oscillationIntensity: BALANCE_OSCILLATION_INTENSITY.VERY,
        recoveryModifier: 0.7,
      },
      CRITICAL: {
        threshold: BALANCE_CRITICAL_THRESHOLD,
        color: BALANCE_LEVEL_COLORS.CRITICAL,
        oscillationIntensity: BALANCE_OSCILLATION_INTENSITY.CRITICAL,
        recoveryModifier: 0.5,
      },
    };

    // Déterminer le niveau initial
    this.currentLevel = this.calculateLevel();
  }

  // ============================================================================
  // INITIALISATION
  // ============================================================================

  /**
   * Initialise le composant.
   */
  init(): void {
    console.log('[BalanceComponent] Initialisé');
    this.emitEvent(BalanceEventType.CHANGED);
  }

  // ============================================================================
  // UPDATE
  // ============================================================================

  /**
   * Met à jour l'équilibre chaque frame.
   *
   * Gère la récupération automatique vers l'équilibre (0).
   *
   * @param _time - Temps total écoulé (ms)
   * @param delta - Temps écoulé depuis la dernière frame (ms)
   */
  update(_time: number, delta: number): void {
    if (!this.active) {
      return;
    }

    const deltaSeconds = delta / 1000;

    // Incrémenter le temps d'oscillation
    this.oscillationTime += delta;

    // Récupération automatique vers l'équilibre
    this.recoverToCenter(deltaSeconds);

    // Vérifier si chute imminente
    this.checkFalling();
  }

  // ============================================================================
  // MÉTHODES PUBLIQUES - PERTURBATIONS
  // ============================================================================

  /**
   * Applique une perturbation d'équilibre.
   *
   * @param perturbation - Configuration de la perturbation
   * @returns true si la perturbation a été appliquée
   */
  public applyPerturbation(perturbation: BalancePerturbation): boolean {
    // Vérifier le cooldown
    const now = Date.now();
    if (now - this.lastPerturbationTime < BALANCE_PERTURBATION_COOLDOWN) {
      return false;
    }

    this.lastPerturbationTime = now;

    // Déterminer la direction
    let direction = perturbation.direction ?? 0;
    if (direction === 0) {
      // Direction aléatoire si non spécifiée
      direction = Math.random() > 0.5 ? 1 : -1;
    }

    // Appliquer la magnitude avec la direction
    const previousValue = this.state.current;
    const change = perturbation.magnitude * direction;
    this.state.current = Math.max(
      this.state.min,
      Math.min(this.state.max, this.state.current + change)
    );

    // Mettre à jour la direction du déséquilibre
    this.updateDirection();

    if (this.state.current !== previousValue) {
      this.checkLevelChange();
      this.emitEvent(BalanceEventType.PERTURBED, { perturbation });
      this.emitEvent(BalanceEventType.CHANGED);

      console.log(
        `[BalanceComponent] Perturbation ${perturbation.type}: ${change.toFixed(1)} (nouvelle valeur: ${this.state.current.toFixed(1)})`
      );
    }

    return true;
  }

  /**
   * Applique une perturbation par obstacle.
   *
   * @param magnitude - Magnitude de la perturbation (optionnel, utilise la constante par défaut)
   * @param direction - Direction (optionnel, aléatoire par défaut)
   */
  public perturbObstacle(magnitude?: number, direction?: number): void {
    this.applyPerturbation({
      type: BalancePerturbationType.OBSTACLE,
      magnitude: magnitude ?? require('@config/constants').BALANCE_PERTURBATION_OBSTACLE,
      direction,
    });
  }

  /**
   * Applique une perturbation par virage serré.
   *
   * @param magnitude - Magnitude de la perturbation (optionnel)
   * @param direction - Direction du virage (-1 = gauche, +1 = droite)
   */
  public perturbSharpTurn(magnitude?: number, direction?: number): void {
    this.applyPerturbation({
      type: BalancePerturbationType.SHARP_TURN,
      magnitude: magnitude ?? require('@config/constants').BALANCE_PERTURBATION_SHARP_TURN,
      direction,
    });
  }

  /**
   * Applique une perturbation par terrain difficile.
   *
   * @param magnitude - Magnitude de la perturbation (optionnel)
   */
  public perturbTerrain(magnitude?: number): void {
    this.applyPerturbation({
      type: BalancePerturbationType.DIFFICULT_TERRAIN,
      magnitude: magnitude ?? require('@config/constants').BALANCE_PERTURBATION_TERRAIN,
    });
  }

  /**
   * Applique une perturbation par collision.
   *
   * @param magnitude - Magnitude de la perturbation (optionnel)
   * @param direction - Direction de l'impact
   */
  public perturbCollision(magnitude?: number, direction?: number): void {
    this.applyPerturbation({
      type: BalancePerturbationType.COLLISION,
      magnitude: magnitude ?? require('@config/constants').BALANCE_PERTURBATION_COLLISION,
      direction,
    });
  }

  /**
   * Applique une perturbation par atterrissage.
   *
   * @param magnitude - Magnitude de la perturbation (optionnel)
   */
  public perturbLanding(magnitude?: number): void {
    this.applyPerturbation({
      type: BalancePerturbationType.LANDING,
      magnitude: magnitude ?? require('@config/constants').BALANCE_PERTURBATION_LANDING,
    });
  }

  // ============================================================================
  // MÉTHODES PUBLIQUES - RÉCUPÉRATION
  // ============================================================================

  /**
   * Récupère progressivement l'équilibre vers le centre (0).
   *
   * @param deltaSeconds - Temps écoulé (secondes)
   */
  public recoverToCenter(deltaSeconds: number): void {
    if (Math.abs(this.state.current) < 0.1) {
      // Déjà équilibré
      if (this.state.current !== 0) {
        this.state.current = 0;
        this.updateDirection();
        this.checkLevelChange();
        this.emitEvent(BalanceEventType.RECOVERED);
        this.emitEvent(BalanceEventType.CHANGED);
      }
      return;
    }

    const previousValue = this.state.current;

    // Appliquer le modificateur de récupération selon le niveau
    const levelConfig = this.getLevelConfig();
    const effectiveRecoveryRate = this.state.recoveryRate * levelConfig.recoveryModifier;

    // Récupérer vers 0
    if (this.state.current > 0) {
      this.state.current = Math.max(0, this.state.current - effectiveRecoveryRate * deltaSeconds);
    } else if (this.state.current < 0) {
      this.state.current = Math.min(0, this.state.current + effectiveRecoveryRate * deltaSeconds);
    }

    // Mettre à jour la direction
    this.updateDirection();

    if (this.state.current !== previousValue) {
      this.checkLevelChange();
      this.emitEvent(BalanceEventType.CHANGED);
    }
  }

  /**
   * Réinitialise l'équilibre à 0 (équilibré).
   * Utilisé après une chute pour remettre le cycliste d'aplomb.
   */
  public reset(): void {
    this.state.current = BALANCE_INITIAL;
    this.state.isFalling = false;
    this.updateDirection();
    this.checkLevelChange();
    this.emitEvent(BalanceEventType.RECOVERED);
    this.emitEvent(BalanceEventType.CHANGED);
    console.log('[BalanceComponent] Équilibre réinitialisé');
  }

  // ============================================================================
  // MÉTHODES PUBLIQUES - GETTERS
  // ============================================================================

  /**
   * Récupère l'état actuel de l'équilibre.
   *
   * @returns État d'équilibre
   */
  public getState(): Readonly<BalanceState> {
    return { ...this.state };
  }

  /**
   * Récupère la valeur actuelle d'équilibre.
   *
   * @returns Valeur actuelle (-100 à +100)
   */
  public getCurrent(): number {
    return this.state.current;
  }

  /**
   * Récupère la valeur absolue de l'équilibre.
   *
   * @returns Valeur absolue (0 à 100)
   */
  public getAbsolute(): number {
    return Math.abs(this.state.current);
  }

  /**
   * Récupère le niveau d'équilibre actuel.
   *
   * @returns Niveau actuel
   */
  public getLevel(): BalanceLevel {
    return this.currentLevel;
  }

  /**
   * Récupère la configuration du niveau actuel.
   *
   * @returns Configuration de niveau
   */
  public getLevelConfig(): BalanceLevelConfig {
    return this.levelConfigs[this.currentLevel];
  }

  /**
   * Calcule l'angle d'oscillation pour le rendu visuel.
   *
   * @param time - Temps actuel (ms) (optionnel, utilise le temps interne si omis)
   * @returns Angle d'oscillation (radians)
   */
  public getOscillationAngle(time?: number): number {
    const t = time ?? this.oscillationTime;

    // Intensité selon le niveau de déséquilibre
    const intensity = this.getLevelConfig().oscillationIntensity;

    if (intensity === 0) {
      return 0;
    }

    // Oscillation sinusoïdale
    const angle = Math.sin(t * BALANCE_OSCILLATION_SPEED * 0.001) * intensity * 0.1;

    // Appliquer la direction du déséquilibre
    return angle * this.state.direction;
  }

  /**
   * Vérifie si le cycliste est en train de tomber.
   *
   * @returns true si en train de tomber
   */
  public isFalling_(): boolean {
    return this.state.isFalling;
  }

  /**
   * Vérifie si l'équilibre est critique.
   *
   * @returns true si critique
   */
  public isCritical(): boolean {
    return this.getAbsolute() >= BALANCE_CRITICAL_THRESHOLD;
  }

  /**
   * Vérifie si l'équilibre est équilibré.
   *
   * @returns true si équilibré
   */
  public isBalanced(): boolean {
    return this.currentLevel === 'BALANCED';
  }

  // ============================================================================
  // MÉTHODES PRIVÉES
  // ============================================================================

  /**
   * Met à jour la direction du déséquilibre.
   */
  private updateDirection(): void {
    if (this.state.current > 0) {
      this.state.direction = 1;
    } else if (this.state.current < 0) {
      this.state.direction = -1;
    } else {
      this.state.direction = 0;
    }
  }

  /**
   * Calcule le niveau d'équilibre selon la valeur actuelle.
   *
   * @returns Niveau calculé
   */
  private calculateLevel(): BalanceLevel {
    const absolute = this.getAbsolute();

    if (absolute >= BALANCE_LEVEL_VERY_THRESHOLD) {
      return 'CRITICAL';
    } else if (absolute >= BALANCE_LEVEL_SLIGHTLY_THRESHOLD) {
      return 'VERY_UNBALANCED';
    } else if (absolute >= BALANCE_LEVEL_BALANCED_THRESHOLD) {
      return 'SLIGHTLY_UNBALANCED';
    } else {
      return 'BALANCED';
    }
  }

  /**
   * Vérifie si le niveau a changé et émet l'événement approprié.
   */
  private checkLevelChange(): void {
    const newLevel = this.calculateLevel();

    if (newLevel !== this.currentLevel) {
      const previousLevel = this.currentLevel;
      this.currentLevel = newLevel;

      this.emitEvent(BalanceEventType.LEVEL_CHANGED, {
        level: newLevel,
        previousLevel,
      });

      // Événement spécial si passage en critique
      if (newLevel === 'CRITICAL') {
        this.emitEvent(BalanceEventType.CRITICAL);
        console.log('[BalanceComponent] CRITIQUE! Risque de chute!');
      }

      console.log(`[BalanceComponent] Niveau changé: ${previousLevel} -> ${newLevel}`);
    }
  }

  /**
   * Vérifie si le cycliste doit tomber.
   */
  private checkFalling(): void {
    const shouldFall = this.getAbsolute() >= BALANCE_FALL_THRESHOLD;

    if (shouldFall && !this.state.isFalling) {
      this.state.isFalling = true;
      this.emitEvent(BalanceEventType.FALLING);
      console.log('[BalanceComponent] CHUTE!');
    }
  }

  /**
   * Émet un événement via l'EventBus.
   *
   * @param event - Type d'événement
   * @param additionalPayload - Données additionnelles (optionnel)
   */
  private emitEvent(event: BalanceEventType, additionalPayload?: Partial<BalanceEventPayload>): void {
    if (!this.eventBus) {
      return;
    }

    const payload: BalanceEventPayload = {
      state: this.getState(),
      level: this.currentLevel,
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
    console.log('[BalanceComponent] Détruit');
  }
}
