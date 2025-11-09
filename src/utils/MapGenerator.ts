/**
 * Générateur de maps de test pour le système de terrain.
 *
 * Crée des maps procédurales avec différents patterns de terrain
 * pour tester le système et avoir un parcours varié.
 */

import { TerrainType } from '@/types/enums';

/**
 * Générateur de maps de terrain programmatiques.
 */
export class MapGenerator {
  /**
   * Génère une map de test simple avec différentes zones de terrain.
   *
   * Layout :
   * - Centre : Piste d'asphalte en forme de circuit
   * - Côtés : Zones de terrain varié (herbe, sable, boue, gravier)
   * - Zones de transition entre les terrains
   *
   * @param width - Largeur en tiles
   * @param height - Hauteur en tiles
   * @returns Tableau 2D des types de terrain
   */
  public static generateTestMap(width: number, height: number): TerrainType[][] {
    // Initialiser avec de l'herbe partout
    const map: TerrainType[][] = [];
    for (let y = 0; y < height; y++) {
      map[y] = [];
      const row = map[y];
      if (row) {
        for (let x = 0; x < width; x++) {
          row[x] = TerrainType.GRASS;
        }
      }
    }

    // Créer une piste d'asphalte centrale (circuit ovale)
    this.createOvalTrack(map, width, height);

    // Ajouter des zones de terrain difficile
    this.addTerrainZones(map, width, height);

    return map;
  }

  /**
   * Crée une piste ovale d'asphalte au centre.
   *
   * @param map - Map à modifier
   * @param width - Largeur de la map
   * @param height - Hauteur de la map
   */
  private static createOvalTrack(
    map: TerrainType[][],
    width: number,
    height: number
  ): void {
    const centerX = Math.floor(width / 2);
    const centerY = Math.floor(height / 2);
    const radiusX = Math.floor(width * 0.35);
    const radiusY = Math.floor(height * 0.35);
    const trackWidth = 4; // Largeur de la piste en tiles

    for (let y = 0; y < height; y++) {
      const row = map[y];
      if (!row) continue;

      for (let x = 0; x < width; x++) {
        // Calculer la distance normalisée au centre
        const dx = (x - centerX) / radiusX;
        const dy = (y - centerY) / radiusY;
        const distance = Math.sqrt(dx * dx + dy * dy);

        // Si dans la bande de la piste
        if (distance >= 0.7 && distance <= 0.7 + trackWidth / Math.min(radiusX, radiusY)) {
          row[x] = TerrainType.ASPHALT;
        }
      }
    }
  }

  /**
   * Ajoute des zones de terrain varié.
   *
   * @param map - Map à modifier
   * @param width - Largeur de la map
   * @param height - Hauteur de la map
   */
  private static addTerrainZones(
    map: TerrainType[][],
    width: number,
    height: number
  ): void {
    // Zone de sable (coin supérieur droit)
    this.fillRectangle(
      map,
      Math.floor(width * 0.7),
      Math.floor(height * 0.1),
      Math.floor(width * 0.2),
      Math.floor(height * 0.3),
      TerrainType.SAND
    );

    // Zone de boue (coin inférieur gauche)
    this.fillRectangle(
      map,
      Math.floor(width * 0.1),
      Math.floor(height * 0.6),
      Math.floor(width * 0.2),
      Math.floor(height * 0.3),
      TerrainType.MUD
    );

    // Zone de gravier (coin supérieur gauche)
    this.fillRectangle(
      map,
      Math.floor(width * 0.1),
      Math.floor(height * 0.1),
      Math.floor(width * 0.15),
      Math.floor(height * 0.2),
      TerrainType.GRAVEL
    );
  }

  /**
   * Remplit une zone rectangulaire avec un type de terrain.
   *
   * @param map - Map à modifier
   * @param startX - X de départ
   * @param startY - Y de départ
   * @param w - Largeur de la zone
   * @param h - Hauteur de la zone
   * @param type - Type de terrain
   */
  private static fillRectangle(
    map: TerrainType[][],
    startX: number,
    startY: number,
    w: number,
    h: number,
    type: TerrainType
  ): void {
    const firstRow = map[0];
    if (!firstRow) return;

    for (let y = startY; y < Math.min(startY + h, map.length); y++) {
      const row = map[y];
      if (!row) continue;

      for (let x = startX; x < Math.min(startX + w, firstRow.length); x++) {
        // Ne pas écraser l'asphalte
        if (row[x] !== TerrainType.ASPHALT) {
          row[x] = type;
        }
      }
    }
  }

  /**
   * Génère une map en damier pour tester les transitions.
   *
   * @param width - Largeur en tiles
   * @param height - Hauteur en tiles
   * @param tileSize - Taille des carreaux du damier
   * @returns Tableau 2D des types de terrain
   */
  public static generateCheckerboardMap(
    width: number,
    height: number,
    tileSize: number = 5
  ): TerrainType[][] {
    const map: TerrainType[][] = [];
    const types = [
      TerrainType.ASPHALT,
      TerrainType.GRASS,
      TerrainType.SAND,
      TerrainType.MUD,
      TerrainType.GRAVEL,
    ];

    for (let y = 0; y < height; y++) {
      map[y] = [];
      for (let x = 0; x < width; x++) {
        const checkX = Math.floor(x / tileSize);
        const checkY = Math.floor(y / tileSize);
        const index = (checkX + checkY) % types.length;
        const terrainType = types[index];
        if (terrainType) {
          map[y]![x] = terrainType;
        }
      }
    }

    return map;
  }

  /**
   * Génère une map avec des bandes horizontales de terrain.
   *
   * Utile pour tester les effets de chaque terrain séparément.
   *
   * @param width - Largeur en tiles
   * @param height - Hauteur en tiles
   * @returns Tableau 2D des types de terrain
   */
  public static generateStripedMap(width: number, height: number): TerrainType[][] {
    const map: TerrainType[][] = [];
    const types = [
      TerrainType.ASPHALT,
      TerrainType.GRASS,
      TerrainType.SAND,
      TerrainType.MUD,
      TerrainType.GRAVEL,
    ];

    const stripHeight = Math.floor(height / types.length);

    for (let y = 0; y < height; y++) {
      map[y] = [];
      const typeIndex = Math.min(Math.floor(y / stripHeight), types.length - 1);
      const terrainType = types[typeIndex];

      if (terrainType) {
        for (let x = 0; x < width; x++) {
          map[y]![x] = terrainType;
        }
      }
    }

    return map;
  }

  /**
   * Génère une map aléatoire avec des clusters de terrain.
   *
   * @param width - Largeur en tiles
   * @param height - Hauteur en tiles
   * @param seed - Seed pour la génération aléatoire
   * @returns Tableau 2D des types de terrain
   */
  public static generateRandomMap(
    width: number,
    height: number,
    seed: number = Date.now()
  ): TerrainType[][] {
    // Simple random (pas de vrai seeding pour simplifier)
    const map: TerrainType[][] = [];
    const types = Object.values(TerrainType);

    for (let y = 0; y < height; y++) {
      map[y] = [];
      for (let x = 0; x < width; x++) {
        // Utiliser un bruit simplifié basé sur la position
        const noise = (Math.sin(x * 0.1 + seed) + Math.cos(y * 0.1 + seed)) / 2;
        const index = Math.floor((noise + 1) * (types.length / 2));
        const terrainType = types[Math.min(index, types.length - 1)];
        if (terrainType) {
          map[y]![x] = terrainType;
        }
      }
    }

    return map;
  }
}
