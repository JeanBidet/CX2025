import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT, BACKGROUND_COLOR, TARGET_FPS, GRAVITY } from './constants';

/**
 * Configuration principale de Phaser 3.
 * Définit tous les paramètres du moteur de jeu.
 *
 * @see https://photonstorm.github.io/phaser3-docs/Phaser.Types.Core.html#.GameConfig
 */
export const gameConfig: Phaser.Types.Core.GameConfig = {
  // ============================================================================
  // CONFIGURATION GÉNÉRALE
  // ============================================================================

  /**
   * Type de rendu : AUTO choisit WebGL avec fallback Canvas.
   * WebGL offre de meilleures performances pour les effets visuels.
   */
  type: Phaser.AUTO,

  /**
   * ID du conteneur HTML parent.
   * Correspond au div dans index.html.
   */
  parent: 'game-container',

  /**
   * Couleur de fond du canvas.
   */
  backgroundColor: BACKGROUND_COLOR,

  /**
   * Dimensions du canvas.
   */
  width: GAME_WIDTH,
  height: GAME_HEIGHT,

  // ============================================================================
  // SYSTÈME DE SCALE
  // ============================================================================

  /**
   * Configuration du système de scale pour la responsive.
   * FIT redimensionne le jeu pour s'adapter au conteneur tout en conservant le ratio.
   */
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
    width: GAME_WIDTH,
    height: GAME_HEIGHT,
  },

  // ============================================================================
  // PHYSIQUE ARCADE
  // ============================================================================

  /**
   * Configuration du moteur physique Arcade.
   * Plus simple et performant que Matter.js, parfait pour un jeu 2D.
   */
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: GRAVITY, x: 0 },
      debug: false, // Mettre à true pour voir les hitboxes
      fps: TARGET_FPS,
    },
  },

  // ============================================================================
  // RENDU
  // ============================================================================

  /**
   * Options de rendu pour optimiser les performances.
   */
  render: {
    antialias: true,              // Anti-aliasing pour des sprites plus lisses
    pixelArt: false,              // False car on n'utilise pas de pixel art
    roundPixels: true,            // Arrondit les positions pour éviter le flou
    transparent: false,           // Fond opaque
    clearBeforeRender: true,      // Efface le canvas avant chaque frame
    preserveDrawingBuffer: false, // Optimisation pour les screenshots
    premultipliedAlpha: true,     // Optimisation de l'alpha blending
    failIfMajorPerformanceCaveat: false,
  },

  // ============================================================================
  // AUDIO
  // ============================================================================

  /**
   * Configuration audio.
   * Sera utilisé dans les prompts suivants.
   */
  audio: {
    disableWebAudio: false,
  },

  // ============================================================================
  // SCÈNES
  // ============================================================================

  /**
   * Liste des scènes du jeu.
   * Pour l'instant, seule RaceScene est importée.
   * Les autres scènes (Menu, Results) seront ajoutées dans les prompts suivants.
   */
  scene: [], // Les scènes seront ajoutées dynamiquement

  // ============================================================================
  // FPS ET PERFORMANCES
  // ============================================================================

  /**
   * Configuration des FPS et de la boucle de jeu.
   */
  fps: {
    target: TARGET_FPS,
    forceSetTimeOut: false, // Utilise requestAnimationFrame
    smoothStep: true,       // Lisse les variations de delta time
    min: 30,                // FPS minimum avant ralentissement
    limit: TARGET_FPS,      // FPS maximum
  },

  // ============================================================================
  // OPTIONS DIVERSES
  // ============================================================================

  /**
   * Afficher le banner Phaser dans la console.
   */
  banner: {
    hidePhaser: false,
    text: '#87CEEB',
    background: [
      '#134E6F',
      '#FF6E6E',
      '#FFC93C',
      '#FFEAA7',
    ],
  },

  /**
   * Options de performance et stabilité.
   */
  autoFocus: true,           // Focus automatique sur le canvas
  disableContextMenu: true,  // Désactive le menu contextuel (clic droit)
  powerPreference: 'high-performance', // Demande GPU haute performance
};
