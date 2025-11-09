import Phaser from 'phaser';
import type { IObserver } from '@/patterns/observer';
import type { BalanceEventPayload } from '@/types/balance';
import { BalanceEventType } from '@/types/balance';
import {
  UI_BAR_WIDTH,
  UI_BAR_HEIGHT,
  UI_BAR_BORDER_WIDTH,
  UI_BAR_BORDER_COLOR,
  UI_BAR_BACKGROUND_COLOR,
  UI_BAR_BACKGROUND_ALPHA,
  BALANCE_LEVEL_COLORS,
} from '@config/constants';

/**
 * Barre d'équilibre UI.
 *
 * Affiche visuellement l'équilibre du cycliste avec :
 * - Une barre centrale représentant l'équilibre (-100 à +100)
 * - Indicateur se déplaçant vers la gauche (déséquilibre gauche) ou droite (déséquilibre droite)
 * - Couleur changeant selon le niveau (vert/jaune/orange/rouge)
 * - Zone centrale (équilibré) marquée
 * - Un label "Équilibre"
 *
 * Utilise l'Observer Pattern pour s'auto-mettre à jour.
 *
 * @example
 * ```typescript
 * // Dans RaceScene.create()
 * const balanceBar = new BalanceBar(this, 20, 90, eventBus);
 * this.add.existing(balanceBar);
 * ```
 */
export class BalanceBar extends Phaser.GameObjects.Container implements IObserver {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Graphics pour le fond */
  private background: Phaser.GameObjects.Graphics;

  /** Graphics pour l'indicateur de balance */
  private indicator: Phaser.GameObjects.Graphics;

  /** Graphics pour la zone centrale */
  private centerZone: Phaser.GameObjects.Graphics;

  /** Graphics pour le contour */
  private border: Phaser.GameObjects.Graphics;

  /** Texte du label */
  private labelText: Phaser.GameObjects.Text;

  /** Texte de la direction */
  private directionText: Phaser.GameObjects.Text;

  /** Valeur actuelle (-100 à +100) */
  private currentValue: number = 0;

  /** Couleur actuelle de l'indicateur */
  private currentColor: string = BALANCE_LEVEL_COLORS.BALANCED;

  // ============================================================================
  // CONSTRUCTEUR
  // ============================================================================

  /**
   * Crée une nouvelle barre d'équilibre.
   *
   * @param scene - Scène Phaser propriétaire
   * @param x - Position X
   * @param y - Position Y
   * @param eventBus - EventBus pour s'abonner aux événements (optionnel)
   */
  constructor(
    scene: Phaser.Scene,
    x: number,
    y: number,
    eventBus?: import('@/patterns/observer').EventBus
  ) {
    super(scene, x, y);

    // Créer les éléments graphiques
    this.background = scene.add.graphics();
    this.centerZone = scene.add.graphics();
    this.indicator = scene.add.graphics();
    this.border = scene.add.graphics();

    // Créer les textes
    this.labelText = scene.add.text(0, -25, 'ÉQUILIBRE', {
      fontSize: '14px',
      fontFamily: 'Arial',
      color: '#FFFFFF',
      fontStyle: 'bold',
    });

    this.directionText = scene.add.text(UI_BAR_WIDTH / 2, UI_BAR_HEIGHT + 15, 'ÉQUILIBRÉ', {
      fontSize: '12px',
      fontFamily: 'Arial',
      color: '#4CAF50',
      fontStyle: 'bold',
    });
    this.directionText.setOrigin(0.5, 0);

    // Ajouter les éléments au container (ordre de rendu important)
    this.add([
      this.background,
      this.centerZone,
      this.indicator,
      this.border,
      this.labelText,
      this.directionText,
    ]);

    // Dessiner l'état initial
    this.draw();

    // S'abonner aux événements si EventBus fourni
    if (eventBus) {
      eventBus.addObserver(BalanceEventType.CHANGED, this);
      eventBus.addObserver(BalanceEventType.LEVEL_CHANGED, this);
    }

    // Fixer en haut à gauche de la caméra
    this.setScrollFactor(0);
  }

  // ============================================================================
  // OBSERVER PATTERN
  // ============================================================================

  /**
   * Méthode appelée par l'EventBus lors d'un événement d'équilibre.
   *
   * @param event - Type d'événement
   * @param payload - Données de l'événement
   */
  notify(event: string, payload: BalanceEventPayload): void {
    // Mettre à jour la valeur
    this.currentValue = payload.state.current;

    // Mettre à jour la couleur selon le niveau
    if (payload.level) {
      switch (payload.level) {
        case 'BALANCED':
          this.currentColor = BALANCE_LEVEL_COLORS.BALANCED;
          this.directionText.setText('ÉQUILIBRÉ');
          this.directionText.setColor('#4CAF50');
          break;
        case 'SLIGHTLY_UNBALANCED':
          this.currentColor = BALANCE_LEVEL_COLORS.SLIGHTLY;
          this.updateDirectionText();
          break;
        case 'VERY_UNBALANCED':
          this.currentColor = BALANCE_LEVEL_COLORS.VERY;
          this.updateDirectionText();
          break;
        case 'CRITICAL':
          this.currentColor = BALANCE_LEVEL_COLORS.CRITICAL;
          this.directionText.setText('CRITIQUE!');
          this.directionText.setColor('#F44336');
          break;
      }
    }

    // Redessiner
    this.draw();
  }

  // ============================================================================
  // RENDU
  // ============================================================================

  /**
   * Met à jour le texte de direction selon la valeur.
   */
  private updateDirectionText(): void {
    if (this.currentValue > 0) {
      this.directionText.setText('DROITE →');
      this.directionText.setColor(this.currentColor);
    } else if (this.currentValue < 0) {
      this.directionText.setText('← GAUCHE');
      this.directionText.setColor(this.currentColor);
    } else {
      this.directionText.setText('ÉQUILIBRÉ');
      this.directionText.setColor('#4CAF50');
    }
  }

  /**
   * Dessine la barre d'équilibre.
   */
  private draw(): void {
    // Effacer les graphics précédents
    this.background.clear();
    this.centerZone.clear();
    this.indicator.clear();
    this.border.clear();

    // Dessiner le fond
    this.background.fillStyle(UI_BAR_BACKGROUND_COLOR, UI_BAR_BACKGROUND_ALPHA);
    this.background.fillRect(0, 0, UI_BAR_WIDTH, UI_BAR_HEIGHT);

    // Dessiner la zone centrale (équilibre parfait)
    const centerZoneWidth = UI_BAR_WIDTH * 0.2; // 20% de la barre = zone équilibrée
    const centerZoneX = (UI_BAR_WIDTH - centerZoneWidth) / 2;
    this.centerZone.fillStyle(0x4CAF50, 0.2); // Vert semi-transparent
    this.centerZone.fillRect(centerZoneX, 0, centerZoneWidth, UI_BAR_HEIGHT);

    // Calculer la position de l'indicateur
    // -100 = tout à gauche, 0 = centre, +100 = tout à droite
    const normalizedValue = (this.currentValue + 100) / 200; // Normaliser de -100..100 à 0..1
    const indicatorX = normalizedValue * UI_BAR_WIDTH;
    const indicatorWidth = 4; // Largeur de l'indicateur

    // Dessiner l'indicateur
    const colorHex = parseInt(this.currentColor.replace('#', ''), 16);
    this.indicator.fillStyle(colorHex, 1);
    this.indicator.fillRect(indicatorX - indicatorWidth / 2, 0, indicatorWidth, UI_BAR_HEIGHT);

    // Dessiner le contour
    this.border.lineStyle(UI_BAR_BORDER_WIDTH, UI_BAR_BORDER_COLOR, 1);
    this.border.strokeRect(0, 0, UI_BAR_WIDTH, UI_BAR_HEIGHT);

    // Ligne centrale
    this.border.lineStyle(1, 0xFFFFFF, 0.5);
    this.border.lineBetween(UI_BAR_WIDTH / 2, 0, UI_BAR_WIDTH / 2, UI_BAR_HEIGHT);
  }

  /**
   * Met à jour manuellement la barre (si pas d'EventBus).
   *
   * @param value - Nouvelle valeur (-100 à +100)
   * @param color - Couleur (optionnel)
   */
  public updateValue(value: number, color?: string): void {
    this.currentValue = Phaser.Math.Clamp(value, -100, 100);

    if (color) {
      this.currentColor = color;
    }

    this.updateDirectionText();
    this.draw();
  }

  // ============================================================================
  // DESTRUCTION
  // ============================================================================

  /**
   * Détruit la barre et nettoie les ressources.
   */
  destroy(fromScene?: boolean): void {
    this.background.destroy();
    this.centerZone.destroy();
    this.indicator.destroy();
    this.border.destroy();
    this.labelText.destroy();
    this.directionText.destroy();

    super.destroy(fromScene);
  }
}
