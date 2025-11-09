import Phaser from 'phaser';
import type { IObserver } from '@/patterns/observer';
import type { EnduranceEventPayload } from '@/types/endurance';
import { EnduranceEventType } from '@/types/endurance';
import {
  UI_BAR_WIDTH,
  UI_BAR_HEIGHT,
  UI_BAR_BORDER_WIDTH,
  UI_BAR_BORDER_COLOR,
  UI_BAR_BACKGROUND_COLOR,
  UI_BAR_BACKGROUND_ALPHA,
  ENDURANCE_ZONE_COLORS,
} from '@config/constants';

/**
 * Barre d'endurance UI.
 *
 * Affiche visuellement l'endurance du cycliste avec :
 * - Une barre colorée selon la zone (verte/jaune/rouge)
 * - Un fond semi-transparent
 * - Un contour blanc
 * - Un label "Endurance"
 * - La valeur numérique
 *
 * Utilise l'Observer Pattern pour s'auto-mettre à jour.
 *
 * @example
 * ```typescript
 * // Dans RaceScene.create()
 * const enduranceBar = new EnduranceBar(this, 20, 60, eventBus);
 * this.add.existing(enduranceBar);
 * ```
 */
export class EnduranceBar extends Phaser.GameObjects.Container implements IObserver {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Graphics pour le fond */
  private background: Phaser.GameObjects.Graphics;

  /** Graphics pour la barre de remplissage */
  private fillBar: Phaser.GameObjects.Graphics;

  /** Graphics pour le contour */
  private border: Phaser.GameObjects.Graphics;

  /** Texte du label */
  private labelText: Phaser.GameObjects.Text;

  /** Texte de la valeur */
  private valueText: Phaser.GameObjects.Text;

  /** Valeur actuelle (0-100) */
  private currentValue: number = 100;

  /** Pourcentage actuel (0-1) */
  private currentPercentage: number = 1;

  /** Couleur actuelle de la barre */
  private currentColor: string = ENDURANCE_ZONE_COLORS.GREEN;

  // ============================================================================
  // CONSTRUCTEUR
  // ============================================================================

  /**
   * Crée une nouvelle barre d'endurance.
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
    this.fillBar = scene.add.graphics();
    this.border = scene.add.graphics();

    // Créer les textes
    this.labelText = scene.add.text(0, -25, 'ENDURANCE', {
      fontSize: '14px',
      fontFamily: 'Arial',
      color: '#FFFFFF',
      fontStyle: 'bold',
    });

    this.valueText = scene.add.text(UI_BAR_WIDTH + 10, 0, '100', {
      fontSize: '16px',
      fontFamily: 'Arial',
      color: '#FFFFFF',
      fontStyle: 'bold',
    });
    this.valueText.setOrigin(0, 0.5);

    // Ajouter les éléments au container
    this.add([this.background, this.fillBar, this.border, this.labelText, this.valueText]);

    // Dessiner l'état initial
    this.draw();

    // S'abonner aux événements si EventBus fourni
    if (eventBus) {
      eventBus.addObserver(EnduranceEventType.CHANGED, this);
      eventBus.addObserver(EnduranceEventType.ZONE_CHANGED, this);
    }

    // Fixer en haut à gauche de la caméra
    this.setScrollFactor(0);
  }

  // ============================================================================
  // OBSERVER PATTERN
  // ============================================================================

  /**
   * Méthode appelée par l'EventBus lors d'un événement d'endurance.
   *
   * @param event - Type d'événement
   * @param payload - Données de l'événement
   */
  notify(event: string, payload: EnduranceEventPayload): void {
    // Mettre à jour les valeurs
    this.currentValue = payload.state.current;
    this.currentPercentage = payload.state.current / payload.state.max;

    // Mettre à jour la couleur selon la zone
    if (payload.zone) {
      switch (payload.zone) {
        case 'GREEN':
          this.currentColor = ENDURANCE_ZONE_COLORS.GREEN;
          break;
        case 'YELLOW':
          this.currentColor = ENDURANCE_ZONE_COLORS.YELLOW;
          break;
        case 'RED':
          this.currentColor = ENDURANCE_ZONE_COLORS.RED;
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
   * Dessine la barre d'endurance.
   */
  private draw(): void {
    // Effacer les graphics précédents
    this.background.clear();
    this.fillBar.clear();
    this.border.clear();

    // Dessiner le fond
    this.background.fillStyle(UI_BAR_BACKGROUND_COLOR, UI_BAR_BACKGROUND_ALPHA);
    this.background.fillRect(0, 0, UI_BAR_WIDTH, UI_BAR_HEIGHT);

    // Dessiner la barre de remplissage
    const fillWidth = UI_BAR_WIDTH * this.currentPercentage;
    const colorHex = parseInt(this.currentColor.replace('#', ''), 16);
    this.fillBar.fillStyle(colorHex, 1);
    this.fillBar.fillRect(0, 0, fillWidth, UI_BAR_HEIGHT);

    // Dessiner le contour
    this.border.lineStyle(UI_BAR_BORDER_WIDTH, UI_BAR_BORDER_COLOR, 1);
    this.border.strokeRect(0, 0, UI_BAR_WIDTH, UI_BAR_HEIGHT);

    // Mettre à jour le texte de valeur
    this.valueText.setText(Math.ceil(this.currentValue).toString());
  }

  /**
   * Met à jour manuellement la barre (si pas d'EventBus).
   *
   * @param value - Nouvelle valeur (0-100)
   * @param max - Valeur maximale (optionnel, défaut: 100)
   * @param color - Couleur (optionnel)
   */
  public updateValue(value: number, max: number = 100, color?: string): void {
    this.currentValue = value;
    this.currentPercentage = value / max;

    if (color) {
      this.currentColor = color;
    }

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
    this.fillBar.destroy();
    this.border.destroy();
    this.labelText.destroy();
    this.valueText.destroy();

    super.destroy(fromScene);
  }
}
