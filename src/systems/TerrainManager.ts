/**
 * Gestionnaire du système de terrain avec Phaser Tilemaps.
 *
 * Le TerrainManager est responsable de :
 * - Créer et gérer le tilemap Phaser
 * - Mapper les tile indices aux TerrainData
 * - Convertir les coordonnées monde → tile → TerrainData
 * - Optimiser les requêtes fréquentes via cache
 * - Permettre les modifications dynamiques de terrain
 */

import { TerrainType } from '@/types/enums';
import type { TerrainData, TerrainMapConfig } from '@/types/terrain';
import { TerrainFactory } from '@/patterns/factories/TerrainFactory';

/**
 * Gestionnaire centralisé pour tout le système de terrain.
 *
 * Architecture en couches :
 * - Phaser Tilemap (rendu visuel)
 * - TerrainManager (logique de mapping)
 * - TerrainData (données physiques)
 * - Components (utilisation gameplay)
 */
export class TerrainManager {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Référence à la scène Phaser */
  private scene: Phaser.Scene;

  /** Tilemap Phaser */
  private tilemap!: Phaser.Tilemaps.Tilemap;

  /** Layer principale du terrain */
  private terrainLayer!: Phaser.Tilemaps.TilemapLayer;

  /** Map : tile index → TerrainData */
  private terrainDataMap: Map<number, TerrainData>;

  /** Cache des requêtes récentes (coordonnées → TerrainData) */
  private queryCache: Map<string, TerrainData>;

  /** Taille maximale du cache */
  private readonly MAX_CACHE_SIZE = 100;

  /** Configuration du tilemap */
  private config: TerrainMapConfig;

  // ============================================================================
  // CONSTRUCTEUR
  // ============================================================================

  /**
   * Crée un nouveau TerrainManager.
   *
   * @param scene - Scène Phaser propriétaire
   * @param config - Configuration du tilemap
   */
  constructor(scene: Phaser.Scene, config: TerrainMapConfig) {
    this.scene = scene;
    this.config = config;
    this.terrainDataMap = new Map();
    this.queryCache = new Map();

    console.log('[TerrainManager] Initialisation...');
  }

  // ============================================================================
  // INITIALISATION
  // ============================================================================

  /**
   * Initialise le tilemap avec des données.
   *
   * @param mapData - Tableau 2D des types de terrain
   */
  public initializeMap(mapData: TerrainType[][]): void {
    // Créer le tilemap programmatiquement
    this.createTilemap(mapData);

    // Mapper les indices aux TerrainData
    this.initializeTerrainMapping();

    console.log('[TerrainManager] Tilemap initialisé');
  }

  /**
   * Crée le tilemap Phaser à partir des données.
   *
   * @param mapData - Tableau 2D des types de terrain
   */
  private createTilemap(mapData: TerrainType[][]): void {
    const { width, height, tileWidth, tileHeight, tilesetKey, tilesetImageKey } = this.config;

    // Créer un tilemap vide
    this.tilemap = this.scene.make.tilemap({
      width,
      height,
      tileWidth,
      tileHeight,
    });

    // Ajouter le tileset
    const tileset = this.tilemap.addTilesetImage(tilesetKey, tilesetImageKey);

    if (!tileset) {
      throw new Error('[TerrainManager] Impossible de créer le tileset');
    }

    // Créer la layer
    this.terrainLayer = this.tilemap.createBlankLayer('Terrain', tileset, 0, 0)!;

    if (!this.terrainLayer) {
      throw new Error('[TerrainManager] Impossible de créer la layer');
    }

    // Remplir la map avec les données
    this.populateMap(mapData);
  }

  /**
   * Remplit le tilemap avec les données de terrain.
   *
   * @param mapData - Tableau 2D des types de terrain
   */
  private populateMap(mapData: TerrainType[][]): void {
    for (let y = 0; y < mapData.length; y++) {
      const row = mapData[y];
      if (!row) continue;

      for (let x = 0; x < row.length; x++) {
        const terrainType = row[x];
        if (!terrainType) continue;

        const tileIndex = this.getTileIndexForType(terrainType);

        // Placer la tile
        this.terrainLayer.putTileAt(tileIndex, x, y);
      }
    }
  }

  /**
   * Initialise le mapping tile index → TerrainData.
   */
  private initializeTerrainMapping(): void {
    // Créer les TerrainData pour chaque type
    Object.values(TerrainType).forEach(type => {
      const terrainInstance = TerrainFactory.create(type);
      const tileIndex = terrainInstance.data.tileIndex;

      this.terrainDataMap.set(tileIndex, terrainInstance.data);
    });

    console.log(
      `[TerrainManager] ${this.terrainDataMap.size} types de terrain mappés`
    );
  }

  // ============================================================================
  // REQUÊTES DE TERRAIN
  // ============================================================================

  /**
   * Récupère les données de terrain à une position tile.
   *
   * @param tileX - Coordonnée X en tiles
   * @param tileY - Coordonnée Y en tiles
   * @returns Données du terrain ou undefined
   */
  public getTerrainAt(tileX: number, tileY: number): TerrainData | undefined {
    // Vérifier le cache
    const cacheKey = `${tileX},${tileY}`;
    if (this.queryCache.has(cacheKey)) {
      return this.queryCache.get(cacheKey);
    }

    // Récupérer la tile
    const tile = this.terrainLayer.getTileAt(tileX, tileY);

    if (!tile) {
      return undefined;
    }

    // Récupérer les données associées
    const terrainData = this.terrainDataMap.get(tile.index);

    // Mettre en cache
    if (terrainData) {
      this.addToCache(cacheKey, terrainData);
    }

    return terrainData;
  }

  /**
   * Récupère les données de terrain à une position monde.
   *
   * C'est la méthode la plus utilisée par les composants.
   *
   * @param worldX - Coordonnée X dans le monde
   * @param worldY - Coordonnée Y dans le monde
   * @returns Données du terrain ou undefined
   */
  public getTerrainAtWorldXY(worldX: number, worldY: number): TerrainData | undefined {
    // Convertir coordonnées monde → tile
    const tileX = this.terrainLayer.worldToTileX(worldX);
    const tileY = this.terrainLayer.worldToTileY(worldY);

    if (tileX === null || tileY === null) {
      return undefined;
    }

    return this.getTerrainAt(tileX, tileY);
  }

  /**
   * Récupère les données de terrain sous un GameObject.
   *
   * @param gameObject - GameObject Phaser
   * @returns Données du terrain ou undefined
   */
  public getTerrainUnder(gameObject: Phaser.GameObjects.GameObject): TerrainData | undefined {
    const sprite = gameObject as Phaser.GameObjects.Sprite;
    return this.getTerrainAtWorldXY(sprite.x, sprite.y);
  }

  // ============================================================================
  // MODIFICATION DYNAMIQUE
  // ============================================================================

  /**
   * Change dynamiquement le type de terrain à une position.
   *
   * Utile pour effets spéciaux (créer de la boue après pluie, etc.)
   *
   * @param tileX - Coordonnée X en tiles
   * @param tileY - Coordonnée Y en tiles
   * @param newType - Nouveau type de terrain
   */
  public setTerrainAt(tileX: number, tileY: number, newType: TerrainType): void {
    const tileIndex = this.getTileIndexForType(newType);
    this.terrainLayer.putTileAt(tileIndex, tileX, tileY);

    // Invalider le cache pour cette position
    const cacheKey = `${tileX},${tileY}`;
    this.queryCache.delete(cacheKey);
  }

  /**
   * Change dynamiquement le terrain à une position monde.
   *
   * @param worldX - Coordonnée X dans le monde
   * @param worldY - Coordonnée Y dans le monde
   * @param newType - Nouveau type de terrain
   */
  public setTerrainAtWorldXY(worldX: number, worldY: number, newType: TerrainType): void {
    const tileX = this.terrainLayer.worldToTileX(worldX);
    const tileY = this.terrainLayer.worldToTileY(worldY);

    if (tileX !== null && tileY !== null) {
      this.setTerrainAt(tileX, tileY, newType);
    }
  }

  // ============================================================================
  // UTILITAIRES
  // ============================================================================

  /**
   * Retourne l'index de tile pour un type de terrain.
   *
   * @param type - Type de terrain
   * @returns Index de la tile
   */
  private getTileIndexForType(type: TerrainType): number {
    // Les indices correspondent à l'ordre de génération des textures
    switch (type) {
      case TerrainType.ASPHALT:
        return 0;
      case TerrainType.GRASS:
        return 1;
      case TerrainType.SAND:
        return 2;
      case TerrainType.MUD:
        return 3;
      case TerrainType.GRAVEL:
        return 4;
      default:
        return 0;
    }
  }

  /**
   * Ajoute une entrée au cache avec gestion de la taille maximale.
   *
   * @param key - Clé du cache
   * @param data - Données à cacher
   */
  private addToCache(key: string, data: TerrainData): void {
    // Si le cache est plein, supprimer l'entrée la plus ancienne
    if (this.queryCache.size >= this.MAX_CACHE_SIZE) {
      const firstKey = this.queryCache.keys().next().value as string | undefined;
      if (firstKey) {
        this.queryCache.delete(firstKey);
      }
    }

    this.queryCache.set(key, data);
  }

  /**
   * Vide le cache de requêtes.
   */
  public clearCache(): void {
    this.queryCache.clear();
  }

  /**
   * Retourne le tilemap Phaser.
   *
   * @returns Tilemap Phaser
   */
  public getTilemap(): Phaser.Tilemaps.Tilemap | undefined {
    return this.tilemap;
  }

  /**
   * Retourne la layer de terrain.
   *
   * @returns Layer de terrain
   */
  public getTerrainLayer(): Phaser.Tilemaps.TilemapLayer | undefined {
    return this.terrainLayer;
  }

  /**
   * Retourne les dimensions du tilemap en tiles.
   *
   * @returns Dimensions { width, height }
   */
  public getMapSize(): { width: number; height: number } {
    return {
      width: this.tilemap.width,
      height: this.tilemap.height,
    };
  }

  /**
   * Retourne les dimensions du tilemap en pixels.
   *
   * @returns Dimensions { width, height }
   */
  public getMapSizeInPixels(): { width: number; height: number } {
    return {
      width: this.tilemap.widthInPixels,
      height: this.tilemap.heightInPixels,
    };
  }

  /**
   * Affiche des infos de debug sur le terrain.
   */
  public debugInfo(): void {
    console.log('[TerrainManager] Debug Info:');
    console.log(`  Map size: ${this.tilemap.width}x${this.tilemap.height} tiles`);
    console.log(
      `  Map size: ${this.tilemap.widthInPixels}x${this.tilemap.heightInPixels}px`
    );
    console.log(`  Terrain types: ${this.terrainDataMap.size}`);
    console.log(`  Cache entries: ${this.queryCache.size}`);
  }

  // ============================================================================
  // DESTRUCTION
  // ============================================================================

  /**
   * Nettoie les ressources.
   */
  public destroy(): void {
    this.queryCache.clear();
    this.terrainDataMap.clear();

    if (this.terrainLayer) {
      this.terrainLayer.destroy();
    }

    if (this.tilemap) {
      this.tilemap.destroy();
    }

    console.log('[TerrainManager] Destroyed');
  }
}
