/**
 * Types et interfaces pour le système de terrain.
 *
 * Ce fichier définit toutes les structures de données nécessaires
 * pour représenter les différents types de terrain du jeu et leurs
 * propriétés physiques et visuelles.
 */

/**
 * Énumération des types de terrain disponibles.
 *
 * Chaque type de terrain a des propriétés physiques et visuelles
 * distinctes qui affectent le gameplay.
 */
export enum TerrainType {
  /** Asphalte - Surface rapide et adhérente */
  ASPHALT = 'ASPHALT',

  /** Herbe - Surface modérément rapide */
  GRASS = 'GRASS',

  /** Sable - Surface lente et peu adhérente */
  SAND = 'SAND',

  /** Boue - Surface très lente et glissante */
  MUD = 'MUD',

  /** Gravier - Surface modérément lente */
  GRAVEL = 'GRAVEL',
}

/**
 * Interface représentant les données complètes d'un type de terrain.
 *
 * Cette interface sépare les préoccupations :
 * - Propriétés physiques (speedMultiplier, grip, etc.)
 * - Propriétés visuelles (color, tint, tileIndex)
 * - Propriétés de relief (slope, camber)
 */
export interface TerrainData {
  // ============================================================================
  // IDENTIFICATION
  // ============================================================================

  /** Type du terrain */
  readonly type: TerrainType;

  /** Nom lisible du terrain */
  readonly name: string;

  /** Description du terrain */
  readonly description?: string;

  // ============================================================================
  // PROPRIÉTÉS PHYSIQUES
  // ============================================================================

  /**
   * Multiplicateur de vitesse maximale.
   * - 1.0 = vitesse normale
   * - > 1.0 = terrain rapide (ex: asphalte = 1.0)
   * - < 1.0 = terrain lent (ex: sable = 0.6)
   */
  readonly speedMultiplier: number;

  /**
   * Multiplicateur de drain d'endurance.
   * - 1.0 = drain normal
   * - > 1.0 = drain élevé (terrain difficile)
   * - < 1.0 = drain réduit (terrain facile)
   */
  readonly staminaDrainMultiplier: number;

  /**
   * Niveau d'adhérence du terrain (0-1).
   * - 1.0 = adhérence maximale (asphalte)
   * - 0.5 = adhérence moyenne (herbe)
   * - 0.2 = faible adhérence (boue, sable)
   *
   * Affecte la capacité à tourner et freiner.
   */
  readonly gripLevel: number;

  /**
   * Modificateur de drag (résistance au mouvement).
   * - 1.0 = drag normal
   * - > 1.0 = plus de résistance (ralentit plus vite)
   * - < 1.0 = moins de résistance (inertie plus longue)
   */
  readonly dragMultiplier: number;

  // ============================================================================
  // PROPRIÉTÉS DE RELIEF
  // ============================================================================

  /**
   * Pente du terrain en degrés.
   * - 0 = plat
   * - > 0 = montée
   * - < 0 = descente
   *
   * Affecte la vitesse via la composante gravitationnelle.
   */
  slope: number;

  /**
   * Dévers (inclinaison latérale) en degrés.
   * - 0 = pas de dévers
   * - > 0 = incliné vers la droite
   * - < 0 = incliné vers la gauche
   *
   * Affecte la direction du mouvement dans les virages.
   */
  camber: number;

  // ============================================================================
  // PROPRIÉTÉS VISUELLES
  // ============================================================================

  /**
   * Index de la tile dans le tileset Phaser.
   * Utilisé pour identifier visuellement le terrain.
   */
  readonly tileIndex: number;

  /**
   * Couleur du terrain en hexadécimal (pour debug/minimap).
   * Exemple : 0x333333 pour asphalte gris foncé
   */
  readonly color: number;

  /**
   * Teinte appliquée à la tile pour variation visuelle.
   * 0xffffff = pas de teinte (blanc)
   */
  readonly tint?: number;

  /**
   * Alpha (transparence) de la tile (0-1).
   * 1.0 = opaque
   */
  readonly alpha?: number;
}

/**
 * Options pour la création d'un terrain via la Factory.
 *
 * Permet de personnaliser un terrain lors de sa création
 * sans modifier les valeurs par défaut.
 */
export interface TerrainCreationOptions {
  /** Position du terrain dans le monde */
  position?: Phaser.Math.Vector2;

  /** Pente personnalisée (override) */
  slope?: number;

  /** Dévers personnalisé (override) */
  camber?: number;

  /** Teinte personnalisée (override) */
  tint?: number;

  /** Alpha personnalisé (override) */
  alpha?: number;
}

/**
 * Objet retourné par TerrainFactory contenant à la fois
 * les données du terrain et les références Phaser nécessaires.
 */
export interface TerrainInstance {
  /** Données du terrain */
  data: TerrainData;

  /** Position dans le monde */
  position: Phaser.Math.Vector2;

  /** Référence à la tile Phaser (si créée via tilemap) */
  tile?: Phaser.Tilemaps.Tile;

  /** GameObject Phaser associé (optionnel, pour rendu custom) */
  gameObject?: Phaser.GameObjects.GameObject;
}

/**
 * Configuration du tilemap pour le TerrainManager.
 */
export interface TerrainMapConfig {
  /** Largeur de la map en tiles */
  width: number;

  /** Hauteur de la map en tiles */
  height: number;

  /** Taille d'une tile en pixels */
  tileWidth: number;

  /** Hauteur d'une tile en pixels */
  tileHeight: number;

  /** Nom de la clé du tileset */
  tilesetKey: string;

  /** Nom de la clé de l'image du tileset */
  tilesetImageKey: string;
}
