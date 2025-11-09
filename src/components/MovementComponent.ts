import Phaser from 'phaser';
import { BaseComponent } from './BaseComponent';
import { Cyclist } from '@entities/Cyclist';
import { EnduranceComponent } from './EnduranceComponent';
import { BalanceComponent } from './BalanceComponent';
import type { TerrainManager } from '@/systems/TerrainManager';
import type { TerrainData } from '@/types/terrain';
import { TerrainType } from '@/types/enums';
import {
  CYCLIST_ACCELERATION,
  CYCLIST_BRAKE_ACCELERATION,
  CYCLIST_MAX_SPEED,
  CYCLIST_SPRINT_MAX_SPEED,
  CYCLIST_DRAG,
  BALANCE_PERTURBATION_TERRAIN,
} from '@config/constants';

/**
 * Composant gérant la physique du mouvement d'un cycliste.
 *
 * Responsabilités :
 * - Appliquer les forces d'accélération et de freinage
 * - Gérer la vitesse maximale selon le contexte (normal/sprint)
 * - Calculer les forces selon la direction du cycliste
 * - S'assurer que le mouvement est fluide et réaliste
 *
 * Le MovementComponent ne gère PAS les inputs directement.
 * Il expose des méthodes publiques (accelerate, brake, sprint)
 * qui sont appelées par l'InputComponent ou l'AIComponent.
 *
 * @example
 * ```typescript
 * const movement = new MovementComponent(cyclist);
 * cyclist.addComponent(movement);
 *
 * // Dans l'InputComponent ou AIComponent
 * movement.accelerate();
 * movement.setSprinting(true);
 * ```
 */
export class MovementComponent extends BaseComponent {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Référence au cycliste (typée) */
  private cyclist: Cyclist;

  /** Gestionnaire de terrain pour requêter les données du sol */
  private terrainManager?: TerrainManager;

  /** Terrain actuel sous le cycliste */
  private currentTerrain?: TerrainData;

  /** Indique si le cycliste est en train de sprinter */
  private isSprinting: boolean = false;

  /** Indique si on accélère actuellement */
  private isAccelerating: boolean = false;

  /** Indique si on freine actuellement */
  private isBraking: boolean = false;

  /** Multiplicateur de terrain (1.0 = normal, < 1.0 = terrain difficile) */
  private terrainMultiplier: number = 1.0;

  /** Compteur pour limiter la fréquence des requêtes terrain */
  private terrainQueryCounter: number = 0;

  /** Fréquence de requête terrain (tous les N frames) */
  private readonly TERRAIN_QUERY_FREQUENCY = 5;

  /** Fréquence de perturbation d'équilibre sur terrain difficile (ms) */
  private readonly TERRAIN_PERTURBATION_FREQUENCY = 800;

  /** Timestamp de la dernière perturbation de terrain */
  private lastTerrainPerturbation: number = 0;

  // ============================================================================
  // CONSTRUCTEUR
  // ============================================================================

  /**
   * Crée un nouveau composant de mouvement.
   *
   * @param owner - Le cycliste propriétaire
   * @param terrainManager - Gestionnaire de terrain (optionnel)
   */
  constructor(owner: Phaser.GameObjects.GameObject, terrainManager?: TerrainManager) {
    super(owner);
    this.cyclist = owner as Cyclist;

    if (terrainManager) {
      this.terrainManager = terrainManager;
    }
  }

  // ============================================================================
  // INITIALISATION
  // ============================================================================

  /**
   * Initialise le composant.
   */
  init(): void {
    console.log('[MovementComponent] Initialisé');
  }

  // ============================================================================
  // UPDATE
  // ============================================================================

  /**
   * Met à jour le mouvement chaque frame.
   *
   * @param _time - Temps total écoulé (non utilisé ici)
   * @param _delta - Temps écoulé depuis la dernière frame (ms)
   */
  update(_time: number, _delta: number): void {
    if (!this.active) {
      return;
    }

    const deltaSeconds = _delta / 1000;

    // Mettre à jour le terrain actuel (pas à chaque frame pour optimiser)
    this.updateCurrentTerrain();

    // Appliquer les effets du terrain sur la physique
    this.applyTerrainEffects();

    // Appliquer les perturbations d'équilibre liées au terrain
    this.applyTerrainBalancePerturbations(_time);

    // Mettre à jour la vitesse maximale selon le mode
    this.updateMaxVelocity();

    // Appliquer l'accélération si nécessaire
    if (this.isAccelerating) {
      this.applyAcceleration();

      // Drain l'endurance pendant l'accélération
      const enduranceComponent = this.cyclist.getComponent(EnduranceComponent);
      if (enduranceComponent && !enduranceComponent.isExhausted()) {
        enduranceComponent.drainAccelerate(deltaSeconds);
      }
    }

    // Drain l'endurance pendant le sprint
    if (this.isSprinting) {
      const enduranceComponent = this.cyclist.getComponent(EnduranceComponent);
      if (enduranceComponent) {
        enduranceComponent.drainSprint(deltaSeconds);
      }
    }

    // Appliquer le freinage si nécessaire
    if (this.isBraking) {
      this.applyBraking();
    }
  }

  // ============================================================================
  // MÉTHODES PUBLIQUES (appelées par InputComponent ou AIComponent)
  // ============================================================================

  /**
   * Démarre l'accélération.
   */
  public accelerate(): void {
    this.isAccelerating = true;
  }

  /**
   * Arrête l'accélération.
   * Arrête le drain d'endurance.
   */
  public stopAccelerating(): void {
    this.isAccelerating = false;

    // Arrêter le drain d'endurance
    const enduranceComponent = this.cyclist.getComponent(EnduranceComponent);
    if (enduranceComponent) {
      enduranceComponent.stopDrainAccelerate();
    }
  }

  /**
   * Démarre le freinage.
   */
  public brake(): void {
    this.isBraking = true;
  }

  /**
   * Arrête le freinage.
   */
  public stopBraking(): void {
    this.isBraking = false;
  }

  /**
   * Active ou désactive le sprint.
   *
   * @param sprinting - true pour sprinter, false pour arrêter
   */
  public setSprinting(sprinting: boolean): void {
    this.isSprinting = sprinting;
    console.log(`[MovementComponent] Sprint: ${sprinting}`);
  }

  /**
   * Définit le multiplicateur de terrain.
   * Sera utilisé dans les prompts suivants pour gérer la boue, le sable, etc.
   *
   * @param multiplier - Multiplicateur (1.0 = normal, < 1.0 = plus difficile)
   */
  public setTerrainMultiplier(multiplier: number): void {
    this.terrainMultiplier = Phaser.Math.Clamp(multiplier, 0.1, 1.0);
  }

  /**
   * Récupère la vitesse actuelle (scalaire).
   *
   * @returns Vitesse en pixels/seconde
   */
  public getSpeed(): number {
    const body = this.cyclist.getBody();
    return Math.sqrt(body.velocity.x ** 2 + body.velocity.y ** 2);
  }

  /**
   * Récupère le terrain actuel sous le cycliste.
   *
   * @returns Données du terrain ou undefined
   */
  public getCurrentTerrain(): TerrainData | undefined {
    return this.currentTerrain;
  }

  /**
   * Vérifie si le cycliste est en mouvement.
   *
   * @param threshold - Seuil de vitesse minimale (défaut: 1 px/s)
   * @returns true si en mouvement
   */
  public isMoving(threshold: number = 1): boolean {
    return this.getSpeed() > threshold;
  }

  // ============================================================================
  // MÉTHODES PRIVÉES
  // ============================================================================

  /**
   * Applique l'accélération dans la direction du cycliste.
   *
   * La rotation du sprite est convertie en angle de mouvement Phaser
   * en utilisant la constante SPRITE_ANGLE_OFFSET définie dans Cyclist.
   *
   * Formule : angle_mouvement = rotation_sprite - SPRITE_ANGLE_OFFSET
   */
  private applyAcceleration(): void {
    const body = this.cyclist.getBody();

    // Calculer l'accélération effective (avec multiplicateur de terrain)
    const effectiveAcceleration = CYCLIST_ACCELERATION * this.terrainMultiplier;

    // Récupérer l'angle du cycliste et appliquer l'offset de correction
    // Cela convertit la rotation du sprite en angle de mouvement Phaser
    const angle = this.cyclist.rotation - Cyclist.SPRITE_ANGLE_OFFSET;

    // Calculer la force d'accélération dans la direction du cycliste
    // Math.cos et Math.sin pour convertir l'angle en vecteur directionnel
    const forceX = Math.cos(angle) * effectiveAcceleration;
    const forceY = Math.sin(angle) * effectiveAcceleration;

    // Appliquer l'accélération au body
    // Phaser intègre automatiquement : velocity += acceleration * delta
    body.setAcceleration(forceX, forceY);
  }

  /**
   * Applique le freinage en réduisant la vitesse.
   */
  private applyBraking(): void {
    const body = this.cyclist.getBody();

    // Récupérer la vélocité actuelle
    const velocity = body.velocity;

    // Si la vitesse est très faible, arrêter complètement
    if (Math.abs(velocity.x) < 10 && Math.abs(velocity.y) < 10) {
      body.setVelocity(0, 0);
      body.setAcceleration(0, 0);
      return;
    }

    // Calculer la direction inverse du mouvement (pour freiner dans le sens opposé)
    const speed = Math.sqrt(velocity.x ** 2 + velocity.y ** 2);
    if (speed === 0) {
      return;
    }

    // Vecteur unitaire de la direction (normalisé)
    const dirX = velocity.x / speed;
    const dirY = velocity.y / speed;

    // Appliquer une force de freinage dans la direction opposée
    const brakeForceX = -dirX * CYCLIST_BRAKE_ACCELERATION;
    const brakeForceY = -dirY * CYCLIST_BRAKE_ACCELERATION;

    body.setAcceleration(brakeForceX, brakeForceY);
  }

  /**
   * Met à jour le terrain actuel sous le cycliste.
   * Utilise un compteur pour ne pas requêter à chaque frame (optimisation).
   */
  private updateCurrentTerrain(): void {
    // Incrémenter le compteur
    this.terrainQueryCounter++;

    // Requêter le terrain seulement tous les N frames
    if (this.terrainQueryCounter >= this.TERRAIN_QUERY_FREQUENCY) {
      this.terrainQueryCounter = 0;

      if (this.terrainManager) {
        const terrain = this.terrainManager.getTerrainUnder(this.cyclist);
        if (terrain) {
          this.currentTerrain = terrain;
        }
      }
    }
  }

  /**
   * Applique les effets du terrain sur la physique.
   */
  private applyTerrainEffects(): void {
    if (!this.currentTerrain) {
      return;
    }

    const body = this.cyclist.getBody();

    // 1. Appliquer le multiplicateur de vitesse du terrain
    this.terrainMultiplier = this.currentTerrain.speedMultiplier;

    // 2. Appliquer le drag du terrain
    const effectiveDrag = CYCLIST_DRAG * this.currentTerrain.dragMultiplier;
    body.setDrag(effectiveDrag * 10000); // Multiplier car Phaser utilise de grandes valeurs

    // 3. L'adhérence (grip) affectera la rotation dans les prompts suivants
    // Pour l'instant, elle est stockée mais pas utilisée
  }

  /**
   * Met à jour la vitesse maximale selon le mode (normal/sprint).
   * Prend en compte l'endurance du cycliste (zone verte/jaune/rouge).
   */
  private updateMaxVelocity(): void {
    const body = this.cyclist.getBody();
    const maxSpeed = this.isSprinting ? CYCLIST_SPRINT_MAX_SPEED : CYCLIST_MAX_SPEED;

    // Récupérer le multiplicateur d'endurance
    const enduranceComponent = this.cyclist.getComponent(EnduranceComponent);
    const enduranceMultiplier = enduranceComponent ? enduranceComponent.getSpeedMultiplier() : 1.0;

    // Appliquer les multiplicateurs de terrain ET d'endurance
    const effectiveMaxSpeed = maxSpeed * this.terrainMultiplier * enduranceMultiplier;

    body.setMaxVelocity(effectiveMaxSpeed, effectiveMaxSpeed);
  }

  /**
   * Applique des perturbations d'équilibre selon le terrain.
   * Les terrains difficiles (boue, sable) perturbent l'équilibre du cycliste.
   *
   * @param time - Temps actuel (ms)
   */
  private applyTerrainBalancePerturbations(time: number): void {
    // Vérifier si on est en mouvement
    if (!this.isMoving(10)) {
      return;
    }

    // Vérifier le cooldown
    if (time - this.lastTerrainPerturbation < this.TERRAIN_PERTURBATION_FREQUENCY) {
      return;
    }

    // Vérifier le terrain actuel
    if (!this.currentTerrain) {
      return;
    }

    // Seuls certains terrains perturbent l'équilibre
    const perturbingTerrains = [
      TerrainType.MUD,
      TerrainType.SAND,
      TerrainType.GRAVEL,
    ];

    if (!perturbingTerrains.includes(this.currentTerrain.type)) {
      return;
    }

    // Récupérer le composant d'équilibre
    const balanceComponent = this.cyclist.getComponent(BalanceComponent);
    if (!balanceComponent) {
      return;
    }

    // Appliquer une perturbation selon le type de terrain
    let magnitude = BALANCE_PERTURBATION_TERRAIN;

    // Ajuster la magnitude selon le terrain
    switch (this.currentTerrain.type) {
      case TerrainType.MUD:
        magnitude *= 1.2; // Boue perturbe plus
        break;
      case TerrainType.SAND:
        magnitude *= 1.5; // Sable perturbe beaucoup plus
        break;
      case TerrainType.GRAVEL:
        magnitude *= 0.8; // Gravier perturbe moins
        break;
    }

    // Appliquer la perturbation
    balanceComponent.perturbTerrain(magnitude);
    this.lastTerrainPerturbation = time;
  }

  // ============================================================================
  // DESTRUCTION
  // ============================================================================

  /**
   * Nettoie le composant.
   */
  destroy(): void {
    // Réinitialiser les états
    this.isAccelerating = false;
    this.isBraking = false;
    this.isSprinting = false;

    // Arrêter l'accélération du body
    const body = this.cyclist.getBody();
    if (body) {
      body.setAcceleration(0, 0);
    }

    console.log('[MovementComponent] Détruit');
  }
}
