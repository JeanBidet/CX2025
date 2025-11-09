import Phaser from 'phaser';
import {
  GAME_HEIGHT,
  SHOW_FPS,
  FPS_X,
  FPS_Y,
  FPS_COLOR,
  FPS_FONT_SIZE,
  TRACK_LENGTH,
  UI_BAR_X,
  UI_BAR_Y,
  UI_BAR_SPACING,
  UI_BAR_HEIGHT,
} from '@config/constants';
import { Cyclist } from '@entities/Cyclist';
import { MovementComponent, InputComponentNew } from '@components/index';
import { EnduranceComponent } from '@components/EnduranceComponent';
import { BalanceComponent } from '@components/BalanceComponent';
import { InputHandler } from '@/systems/InputHandler';
import { TerrainManager } from '@/systems/TerrainManager';
import { TerrainTileGenerator } from '@/utils/TerrainTileGenerator';
import { MapGenerator } from '@/utils/MapGenerator';
import type { TerrainMapConfig } from '@/types/terrain';
import { CyclistAnimationGenerator } from '@/utils/CyclistAnimationGenerator';
import { StateMachineComponent } from '@components/StateMachineComponent';
import { StateType } from '../types/cyclistState';
import { EventBus } from '@/patterns/observer';
import { EnduranceBar, BalanceBar } from '@/ui';
import { BalanceObserver } from '@/observers';

/**
 * Scène principale de course.
 * Gère la logique du jeu, le rendu et les interactions.
 *
 * Cette scène utilise les trois méthodes principales du cycle de vie Phaser :
 * - preload() : Chargement des assets (images, sons, etc.)
 * - create() : Initialisation de la scène et création des GameObjects
 * - update() : Logique exécutée à chaque frame (60 FPS)
 */
export class RaceScene extends Phaser.Scene {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Texte affichant les FPS */
  private fpsText?: Phaser.GameObjects.Text;

  /** Groupes Phaser pour organisation des GameObjects */
  private cyclistsGroup?: Phaser.GameObjects.Group;
  private obstaclesGroup?: Phaser.GameObjects.Group;

  /** Le cycliste du joueur */
  private player?: Cyclist;

  /** Gestionnaire d'input avec Command Pattern */
  private inputHandler?: InputHandler;

  /** Gestionnaire du terrain avec Factory Pattern et Tilemaps */
  private terrainManager?: TerrainManager;

  /** EventBus global pour communication inter-composants via Observer Pattern */
  private eventBus: EventBus;

  /** UI Bars */
  private enduranceBar?: EnduranceBar;
  private balanceBar?: BalanceBar;

  // ============================================================================
  // CONSTRUCTEUR
  // ============================================================================

  constructor() {
    super({ key: 'RaceScene' });

    // Créer l'EventBus global pour cette scène
    this.eventBus = new EventBus();
  }

  // ============================================================================
  // CYCLE DE VIE PHASER
  // ============================================================================

  /**
   * Charge tous les assets nécessaires avant le démarrage de la scène.
   * Cette méthode est appelée automatiquement par Phaser.
   *
   * Pour l'instant, on génère les textures de terrain programmatiquement.
   */
  preload(): void {
    console.log('[RaceScene] Preload - Chargement des assets');

    // Générer les textures de terrain programmatiquement
    // (Dans un vrai jeu, on chargerait des images avec this.load.image)
    TerrainTileGenerator.generateAll(this, 32);

    // Generate cyclist animation textures (procédurales pour fallback)
    CyclistAnimationGenerator.generateAll(this, true); // For player

    // Charger les 4 sprites réels du cycliste individuellement
    // Ces images représentent les frames de l'animation de pédalage
    this.load.image('cyclist-frame-0', 'assets/sprites/cyclist-frame-0.png');
    this.load.image('cyclist-frame-1', 'assets/sprites/cyclist-frame-1.png');
    this.load.image('cyclist-frame-2', 'assets/sprites/cyclist-frame-2.png');
    this.load.image('cyclist-frame-3', 'assets/sprites/cyclist-frame-3.png');

    console.log('[RaceScene] Sprites réels du cycliste chargés');

    // Les autres assets seront chargés ici dans les prompts suivants
    // Exemple :
    // this.load.image('obstacle', 'assets/sprites/obstacle.png');
    // this.load.audio('bgm', 'assets/sounds/race-music.mp3');
  }

  /**
   * Initialise la scène et crée tous les GameObjects.
   * Appelée automatiquement après preload().
   */
  create(): void {
    console.log('[RaceScene] Create - Initialisation de la scène');

    // Configurer le monde physique
    this.setupPhysicsWorld();

    // Créer le terrain (AVANT la caméra pour définir les limites du monde)
    this.createTerrain();

    // Initialiser la caméra
    this.setupCamera();

    // Créer les groupes Phaser pour organisation
    this.setupGroups();

    // Créer l'InputHandler (Command Pattern)
    this.setupInputHandler();
    
    // Create cyclist animations
    this.createAnimations();

    // Créer le cycliste joueur
    this.createPlayer();

    // Créer l'interface utilisateur (barres d'endurance et d'équilibre)
    this.createUI();

    // Créer l'affichage des FPS si activé
    if (SHOW_FPS) {
      this.createFPSDisplay();
    }

    // Créer les instructions
    this.createInstructions();

    // Log de confirmation
    console.log('[RaceScene] Scène initialisée avec succès');
  }

  /**
   * Logique exécutée à chaque frame (environ 60 fois par seconde).
   * C'est ici que la logique du jeu sera implémentée.
   *
   * @param time - Temps total écoulé depuis le début du jeu (ms)
   * @param delta - Temps écoulé depuis la dernière frame (ms)
   */
  update(time: number, delta: number): void {
    // Mettre à jour l'affichage des FPS
    if (this.fpsText && SHOW_FPS) {
      const fps = Math.round(this.game.loop.actualFps);
      this.fpsText.setText(`FPS: ${fps}`);
    }

    // Mettre à jour le joueur et ses composants
    if (this.player) {
      this.player.updateComponents(time, delta);
    }

    // La logique de mise à jour des autres entités sera ajoutée ici
    // Exemple dans les prompts suivants :
    // - Détection de collisions
    // - Mise à jour de l'IA des adversaires
    // - Gestion du terrain
  }

  // ============================================================================
  // MÉTHODES D'INITIALISATION
  // ============================================================================

  /**
   * Configure le monde physique Arcade.
   */
  private setupPhysicsWorld(): void {
    // Les limites seront définies après la création du terrain
    // Désactiver la gravité (jeu en vue de dessus)
    this.physics.world.gravity.y = 0;

    console.log('[RaceScene] Monde physique configuré (limites définies après terrain)');
  }

  /**
   * Configure la caméra principale.
   */
  private setupCamera(): void {
    if (!this.terrainManager) {
      console.warn('[RaceScene] TerrainManager non initialisé, caméra avec limites par défaut');
      this.cameras.main.setBounds(0, 0, TRACK_LENGTH, GAME_HEIGHT);
    } else {
      // Limites de la caméra selon la taille de la map
      const mapSize = this.terrainManager.getMapSizeInPixels();
      this.cameras.main.setBounds(0, 0, mapSize.width, mapSize.height);
    }

    this.cameras.main.setBackgroundColor('#87CEEB'); // Ciel bleu
    console.log('[RaceScene] Caméra configurée');
  }

  /**
   * Crée les groupes Phaser pour organiser les GameObjects.
   * Les groupes facilitent la gestion collective des objets (update, collision, etc.).
   */
  private setupGroups(): void {
    this.cyclistsGroup = this.add.group();
    this.obstaclesGroup = this.add.group();
    console.log('[RaceScene] Groupes créés');
  }

  /**
   * Crée le système de terrain avec Tilemaps et Factory Pattern.
   */
  private createTerrain(): void {
    // Configuration du tilemap
    const config: TerrainMapConfig = {
      width: 50,
      height: 30,
      tileWidth: 32,
      tileHeight: 32,
      tilesetKey: 'terrain_tileset',
      tilesetImageKey: 'terrain_tileset', // Utiliser le tileset combiné
    };

    // Créer le TerrainManager
    this.terrainManager = new TerrainManager(this, config);

    // Générer une map de test
    const mapData = MapGenerator.generateTestMap(config.width, config.height);

    // Initialiser le tilemap
    this.terrainManager.initializeMap(mapData);

    // Mettre à jour les limites du monde physique selon la map
    const mapSize = this.terrainManager.getMapSizeInPixels();
    this.physics.world.setBounds(0, 0, mapSize.width, mapSize.height);

    console.log('[RaceScene] Terrain créé avec tilemap');
  }

  /**
   * Configure l'InputHandler avec le Command Pattern.
   */
  private setupInputHandler(): void {
    this.inputHandler = new InputHandler(this);
    console.log('[RaceScene] InputHandler créé');
  }

  /**
   * Creates all cyclist animations.
   */
  private createAnimations(): void {
    // Create animations for player cyclist (procédurales pour fallback)
    CyclistAnimationGenerator.createAnimations(this, true);

    // Créer l'animation 'ride' avec les sprites réels
    this.createCyclistRideAnimation();

    console.log('[RaceScene] Animations créées');
  }

  /**
   * Crée l'animation de pédalage du cycliste avec les sprites réels.
   *
   * Cette animation utilise les 4 frames chargées depuis assets/sprites/.
   * Configuration :
   * - frameRate: 8 fps pour un pédalage naturel (ni trop rapide, ni trop lent)
   * - repeat: -1 pour boucle infinie
   * - L'ordre des frames suit un cycle de pédalage logique
   *
   * Justification du frameRate:
   * - 6 fps serait trop lent (pédalage au ralenti)
   * - 10 fps serait trop rapide (pédalage frénétique)
   * - 8 fps offre un compromis naturel et fluide
   */
  private createCyclistRideAnimation(): void {
    // Vérifier que l'animation n'existe pas déjà (évite les doublons)
    if (!this.anims.exists('ride')) {
      this.anims.create({
        key: 'ride',
        frames: [
          { key: 'cyclist-frame-0' },
          { key: 'cyclist-frame-1' },
          { key: 'cyclist-frame-2' },
          { key: 'cyclist-frame-3' },
        ],
        frameRate: 8, // 8 images par seconde pour pédalage naturel
        repeat: -1,   // Boucle infinie
      });

      console.log('[RaceScene] Animation "ride" créée avec 4 frames réelles');
    }
  }

  /**
   * Crée le cycliste joueur avec tous ses composants.
   */
  private createPlayer(): void {
    if (!this.inputHandler) {
      throw new Error('[RaceScene] InputHandler doit être créé avant le joueur');
    }

    if (!this.terrainManager) {
      throw new Error('[RaceScene] TerrainManager doit être créé avant le joueur');
    }

    // Position de départ (centre de la map)
    const mapSize = this.terrainManager.getMapSizeInPixels();
    const startX = mapSize.width / 2;
    const startY = mapSize.height / 2;

    // Créer le cycliste
    this.player = new Cyclist(this, startX, startY, true, 'Player');

    // IMPORTANT : Ajouter le cycliste à la scène pour qu'il soit visible
    this.add.existing(this.player);

    // Ajouter le cycliste au monde physique
    this.physics.add.existing(this.player);

    // Initialiser le body physique maintenant qu'il existe
    this.player.initializePhysics();

    // Ajouter les composants avec le Command Pattern et TerrainManager
    const movement = new MovementComponent(this.player, this.terrainManager);
    const input = new InputComponentNew(this.player, this.inputHandler);

    this.player.addComponent(movement);
    this.player.addComponent(input);

    // Add State Machine Component (State Pattern)
    const stateMachine = new StateMachineComponent(this.player, StateType.RIDING);
    this.player.addComponent(stateMachine);

    // Ajouter les composants Endurance et Balance avec Observer Pattern
    const endurance = new EnduranceComponent(this.player, this.eventBus);
    const balance = new BalanceComponent(this.player, this.eventBus);

    this.player.addComponent(endurance);
    this.player.addComponent(balance);

    // Créer l'observateur de chute pour connecter Balance → StateMachine
    new BalanceObserver(this.player, this.eventBus);

    // Ajouter au groupe des cyclistes
    this.cyclistsGroup?.add(this.player);

    // Configurer la caméra pour suivre le joueur
    this.setupPlayerCamera();

    console.log('[RaceScene] Joueur créé avec Command Pattern, TerrainManager et State Machine');
  }

  /**
   * Configure la caméra pour suivre le joueur de manière fluide.
   */
  private setupPlayerCamera(): void {
    if (!this.player) {
      return;
    }

    // La caméra suit le joueur
    this.cameras.main.startFollow(this.player, true, 0.1, 0.1);

    // Décalage de la caméra pour anticiper le mouvement
    this.cameras.main.setFollowOffset(-200, 0);

    // Zone morte (deadzone) pour éviter les mouvements trop brusques
    this.cameras.main.setDeadzone(100, 100);

    console.log('[RaceScene] Caméra configurée pour suivre le joueur');
  }

  /**
   * Crée l'interface utilisateur (barres d'endurance et d'équilibre).
   */
  private createUI(): void {
    // Créer la barre d'endurance
    this.enduranceBar = new EnduranceBar(this, UI_BAR_X, UI_BAR_Y, this.eventBus);
    this.add.existing(this.enduranceBar);

    // Créer la barre d'équilibre (en dessous de la barre d'endurance)
    const balanceY = UI_BAR_Y + UI_BAR_HEIGHT + UI_BAR_SPACING;
    this.balanceBar = new BalanceBar(this, UI_BAR_X, balanceY, this.eventBus);
    this.add.existing(this.balanceBar);

    console.log('[RaceScene] Interface utilisateur créée (Endurance + Équilibre)');
  }

  /**
   * Crée l'affichage des FPS en haut à gauche.
   */
  private createFPSDisplay(): void {
    this.fpsText = this.add.text(FPS_X, FPS_Y, 'FPS: 60', {
      fontSize: FPS_FONT_SIZE,
      color: FPS_COLOR,
      fontFamily: 'monospace',
      backgroundColor: '#00000080',
      padding: { x: 8, y: 4 },
    });
    this.fpsText.setScrollFactor(0); // Fixe à l'écran (ne bouge pas avec la caméra)
    this.fpsText.setDepth(1000); // Toujours au premier plan
    console.log('[RaceScene] Affichage FPS créé');
  }

  /**
   * Crée les instructions pour le joueur.
   */
  private createInstructions(): void {
    const instructions = this.add.text(
      20,
      80,
      'CONTRÔLES:\n' +
      '↑ : Accélérer\n' +
      '↓ : Freiner\n' +
      '← → : Tourner\n' +
      'SHIFT : Sprint',
      {
        fontSize: '16px',
        color: '#ffffff',
        fontFamily: 'monospace',
        backgroundColor: '#00000080',
        padding: { x: 10, y: 8 },
        lineSpacing: 4,
      }
    );
    instructions.setScrollFactor(0);
    instructions.setDepth(999);
    console.log('[RaceScene] Instructions créées');
  }

  // ============================================================================
  // GETTERS PUBLICS
  // ============================================================================

  /**
   * Retourne le groupe des cyclistes.
   */
  public getCyclistsGroup(): Phaser.GameObjects.Group | undefined {
    return this.cyclistsGroup;
  }

  /**
   * Retourne le groupe des obstacles.
   */
  public getObstaclesGroup(): Phaser.GameObjects.Group | undefined {
    return this.obstaclesGroup;
  }

  /**
   * Retourne le gestionnaire de terrain.
   */
  public getTerrainManager(): TerrainManager | undefined {
    return this.terrainManager;
  }
}
