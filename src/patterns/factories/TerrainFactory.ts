/**
 * Factory Pattern pour la création de terrains.
 *
 * Cette classe centralise toute la logique de création des terrains,
 * assurant que chaque type de terrain est créé avec les bonnes
 * propriétés physiques et visuelles.
 *
 * @example
 * ```typescript
 * // Créer un terrain asphalte
 * const asphalt = TerrainFactory.create(TerrainType.ASPHALT);
 *
 * // Créer un terrain avec options personnalisées
 * const mudWithSlope = TerrainFactory.create(TerrainType.MUD, {
 *   slope: 15,
 *   position: new Phaser.Math.Vector2(100, 200)
 * });
 * ```
 */

import { TerrainType } from '@/types/enums';
import type {
  TerrainData,
  TerrainCreationOptions,
  TerrainInstance,
} from '@/types/terrain';

/**
 * Factory pour créer des terrains avec le pattern Factory.
 *
 * Avantages du pattern Factory :
 * - Centralise la logique de création complexe
 * - Garantit la cohérence des propriétés
 * - Facilite l'ajout de nouveaux types
 * - Permet la personnalisation via options
 */
export class TerrainFactory {
  // ============================================================================
  // CONSTANTES DE CONFIGURATION
  // ============================================================================

  /** Index de tile pour chaque type de terrain */
  private static readonly TILE_INDICES = {
    [TerrainType.ASPHALT]: 0,
    [TerrainType.GRASS]: 1,
    [TerrainType.SAND]: 2,
    [TerrainType.MUD]: 3,
    [TerrainType.GRAVEL]: 4,
  };

  /** Couleurs pour chaque type de terrain (debug/minimap) */
  private static readonly COLORS = {
    [TerrainType.ASPHALT]: 0x333333, // Gris foncé
    [TerrainType.GRASS]: 0x44aa44, // Vert
    [TerrainType.SAND]: 0xeecc88, // Beige
    [TerrainType.MUD]: 0x886644, // Marron
    [TerrainType.GRAVEL]: 0x999999, // Gris clair
  };

  // ============================================================================
  // MÉTHODE PRINCIPALE DE CRÉATION
  // ============================================================================

  /**
   * Crée un terrain du type spécifié avec des options personnalisées.
   *
   * C'est la méthode principale à utiliser pour créer des terrains.
   * Elle délègue la création au factory method approprié.
   *
   * @param type - Type de terrain à créer
   * @param options - Options de personnalisation (optionnel)
   * @returns Instance de terrain complète avec données et position
   */
  public static create(
    type: TerrainType,
    options: TerrainCreationOptions = {}
  ): TerrainInstance {
    // Créer les données de base selon le type
    let baseData: TerrainData;

    switch (type) {
      case TerrainType.ASPHALT:
        baseData = this.createAsphalt();
        break;
      case TerrainType.GRASS:
        baseData = this.createGrass();
        break;
      case TerrainType.SAND:
        baseData = this.createSand();
        break;
      case TerrainType.MUD:
        baseData = this.createMud();
        break;
      case TerrainType.GRAVEL:
        baseData = this.createGravel();
        break;
      default:
        console.warn(`[TerrainFactory] Type inconnu: ${type}, utilisation de ASPHALT`);
        baseData = this.createAsphalt();
    }

    // Appliquer les options de personnalisation
    const customizedData = this.applyOptions(baseData, options);

    // Créer l'instance complète
    const instance: TerrainInstance = {
      data: customizedData,
      position: options.position ?? new Phaser.Math.Vector2(0, 0),
    };

    return instance;
  }

  // ============================================================================
  // FACTORY METHODS PRIVÉS (UN PAR TYPE DE TERRAIN)
  // ============================================================================

  /**
   * Crée un terrain ASPHALT.
   *
   * Propriétés :
   * - Très rapide (speedMultiplier = 1.0)
   * - Excellente adhérence (gripLevel = 1.0)
   * - Faible drain d'endurance (1.0)
   * - Faible drag (0.9)
   *
   * Idéal pour les sections rapides et techniques.
   */
  private static createAsphalt(): TerrainData {
    return {
      // Identification
      type: TerrainType.ASPHALT,
      name: 'Asphalte',
      description: 'Surface rapide et adhérente, idéale pour la vitesse',

      // Propriétés physiques
      speedMultiplier: 1.0, // Vitesse normale
      staminaDrainMultiplier: 1.0, // Drain normal
      gripLevel: 1.0, // Adhérence maximale
      dragMultiplier: 0.9, // Peu de résistance

      // Relief (valeurs par défaut, modifiables)
      slope: 0,
      camber: 0,

      // Propriétés visuelles
      tileIndex: this.TILE_INDICES[TerrainType.ASPHALT],
      color: this.COLORS[TerrainType.ASPHALT],
      tint: 0xffffff, // Pas de teinte
      alpha: 1.0,
    };
  }

  /**
   * Crée un terrain GRASS.
   *
   * Propriétés :
   * - Modérément rapide (speedMultiplier = 0.85)
   * - Bonne adhérence (gripLevel = 0.8)
   * - Drain d'endurance modéré (1.2)
   * - Drag moyen (1.1)
   *
   * Terrain polyvalent, légèrement plus difficile que l'asphalte.
   */
  private static createGrass(): TerrainData {
    return {
      type: TerrainType.GRASS,
      name: 'Herbe',
      description: 'Surface naturelle modérément rapide',

      speedMultiplier: 0.85,
      staminaDrainMultiplier: 1.2,
      gripLevel: 0.8,
      dragMultiplier: 1.1,

      slope: 0,
      camber: 0,

      tileIndex: this.TILE_INDICES[TerrainType.GRASS],
      color: this.COLORS[TerrainType.GRASS],
      tint: 0xffffff,
      alpha: 1.0,
    };
  }

  /**
   * Crée un terrain SAND.
   *
   * Propriétés :
   * - Lent (speedMultiplier = 0.6)
   * - Faible adhérence (gripLevel = 0.4)
   * - Drain d'endurance élevé (1.8)
   * - Drag élevé (1.5)
   *
   * Terrain difficile qui ralentit considérablement et épuise.
   */
  private static createSand(): TerrainData {
    return {
      type: TerrainType.SAND,
      name: 'Sable',
      description: 'Surface instable et épuisante',

      speedMultiplier: 0.6,
      staminaDrainMultiplier: 1.8,
      gripLevel: 0.4,
      dragMultiplier: 1.5,

      slope: 0,
      camber: 0,

      tileIndex: this.TILE_INDICES[TerrainType.SAND],
      color: this.COLORS[TerrainType.SAND],
      tint: 0xffffff,
      alpha: 1.0,
    };
  }

  /**
   * Crée un terrain MUD.
   *
   * Propriétés :
   * - Très lent (speedMultiplier = 0.5)
   * - Très faible adhérence (gripLevel = 0.3)
   * - Drain d'endurance très élevé (2.0)
   * - Drag très élevé (1.7)
   *
   * Terrain le plus difficile, glissant et épuisant.
   */
  private static createMud(): TerrainData {
    return {
      type: TerrainType.MUD,
      name: 'Boue',
      description: 'Surface glissante et très difficile',

      speedMultiplier: 0.5,
      staminaDrainMultiplier: 2.0,
      gripLevel: 0.3,
      dragMultiplier: 1.7,

      slope: 0,
      camber: 0,

      tileIndex: this.TILE_INDICES[TerrainType.MUD],
      color: this.COLORS[TerrainType.MUD],
      tint: 0xffffff,
      alpha: 1.0,
    };
  }

  /**
   * Crée un terrain GRAVEL.
   *
   * Propriétés :
   * - Modérément lent (speedMultiplier = 0.75)
   * - Adhérence moyenne (gripLevel = 0.6)
   * - Drain d'endurance modéré (1.4)
   * - Drag moyen (1.2)
   *
   * Terrain intermédiaire entre herbe et sable.
   */
  private static createGravel(): TerrainData {
    return {
      type: TerrainType.GRAVEL,
      name: 'Gravier',
      description: 'Surface instable de difficulté moyenne',

      speedMultiplier: 0.75,
      staminaDrainMultiplier: 1.4,
      gripLevel: 0.6,
      dragMultiplier: 1.2,

      slope: 0,
      camber: 0,

      tileIndex: this.TILE_INDICES[TerrainType.GRAVEL],
      color: this.COLORS[TerrainType.GRAVEL],
      tint: 0xffffff,
      alpha: 1.0,
    };
  }

  // ============================================================================
  // MÉTHODES UTILITAIRES
  // ============================================================================

  /**
   * Applique les options de personnalisation à un terrain de base.
   *
   * Permet de modifier slope, camber, tint, alpha sans recréer
   * tout l'objet TerrainData.
   *
   * @param baseData - Données de base du terrain
   * @param options - Options de personnalisation
   * @returns Nouvelles données avec options appliquées
   */
  private static applyOptions(
    baseData: TerrainData,
    options: TerrainCreationOptions
  ): TerrainData {
    const result: TerrainData = {
      ...baseData,
      slope: options.slope !== undefined ? options.slope : baseData.slope,
      camber: options.camber !== undefined ? options.camber : baseData.camber,
    };

    // Conditionally include tint and alpha if they are defined
    if (options.tint !== undefined) {
      return { ...result, tint: options.tint };
    }
    if (options.alpha !== undefined) {
      return { ...result, alpha: options.alpha };
    }

    return result;
  }

  /**
   * Crée plusieurs terrains en masse.
   *
   * Utile pour générer une map complète.
   *
   * @param types - Tableau des types à créer
   * @param options - Options communes (optionnel)
   * @returns Tableau d'instances de terrain
   *
   * @example
   * ```typescript
   * const terrains = TerrainFactory.createBatch([
   *   TerrainType.ASPHALT,
   *   TerrainType.GRASS,
   *   TerrainType.SAND,
   * ]);
   * ```
   */
  public static createBatch(
    types: TerrainType[],
    options: TerrainCreationOptions = {}
  ): TerrainInstance[] {
    return types.map(type => this.create(type, options));
  }

  /**
   * Retourne les valeurs par défaut d'un type de terrain.
   *
   * Utile pour debugging ou UI.
   *
   * @param type - Type de terrain
   * @returns Données par défaut du terrain
   */
  public static getDefaults(type: TerrainType): TerrainData {
    return this.create(type).data;
  }

  /**
   * Vérifie si un type de terrain est valide.
   *
   * @param type - Type à vérifier
   * @returns true si le type existe
   */
  public static isValidType(type: string): type is TerrainType {
    return Object.values(TerrainType).includes(type as TerrainType);
  }
}
