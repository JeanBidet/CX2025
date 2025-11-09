/**
 * Générateur de tiles de terrain programmatique.
 *
 * Crée des textures de tiles visuellement distinctives pour chaque
 * type de terrain en utilisant Phaser.GameObjects.Graphics.
 *
 * Utilisé quand on n'a pas d'assets graphiques prêts.
 */

import { TerrainType } from '@/types/enums';

/**
 * Génère des textures de tiles pour tous les types de terrain.
 *
 * Chaque tile est générée programmatiquement avec :
 * - Une couleur de base distinctive
 * - Des patterns visuels (points, lignes, textures)
 * - Une bordure pour mieux voir les limites
 */
export class TerrainTileGenerator {
  /** Taille par défaut d'une tile */
  private static readonly TILE_SIZE = 32;

  /**
   * Génère toutes les textures de terrain dans une scène.
   *
   * @param scene - Scène Phaser où créer les textures
   * @param tileSize - Taille des tiles (défaut: 32px)
   */
  public static generateAll(scene: Phaser.Scene, tileSize: number = this.TILE_SIZE): void {
    // Générer les textures individuelles
    this.generateAsphaltTile(scene, tileSize);
    this.generateGrassTile(scene, tileSize);
    this.generateSandTile(scene, tileSize);
    this.generateMudTile(scene, tileSize);
    this.generateGravelTile(scene, tileSize);

    // Générer le tileset combiné
    this.generateCombinedTileset(scene, tileSize);

    console.log('[TerrainTileGenerator] Toutes les textures de terrain générées');
  }

  /**
   * Génère un tileset combiné avec toutes les tiles en une seule image.
   * Layout: tiles arrangées horizontalement (1 row x 5 columns)
   *
   * @param scene - Scène Phaser
   * @param tileSize - Taille d'une tile
   */
  private static generateCombinedTileset(scene: Phaser.Scene, tileSize: number): void {
    const numTiles = 5;
    const tilesetWidth = tileSize * numTiles;
    const tilesetHeight = tileSize;

    const graphics = scene.make.graphics({ x: 0, y: 0 });

    // Dessiner chaque tile à sa position dans le tileset
    // Tile 0: Asphalt
    this.drawAsphaltTile(graphics, 0 * tileSize, 0, tileSize);

    // Tile 1: Grass
    this.drawGrassTile(graphics, 1 * tileSize, 0, tileSize);

    // Tile 2: Sand
    this.drawSandTile(graphics, 2 * tileSize, 0, tileSize);

    // Tile 3: Mud
    this.drawMudTile(graphics, 3 * tileSize, 0, tileSize);

    // Tile 4: Gravel
    this.drawGravelTile(graphics, 4 * tileSize, 0, tileSize);

    // Générer la texture du tileset
    graphics.generateTexture('terrain_tileset', tilesetWidth, tilesetHeight);
    graphics.destroy();

    console.log(`[TerrainTileGenerator] Tileset combiné généré: ${tilesetWidth}x${tilesetHeight}`);
  }

  /**
   * Dessine une tile d'asphalte à une position spécifique.
   */
  private static drawAsphaltTile(graphics: Phaser.GameObjects.Graphics, x: number, y: number, size: number): void {
    graphics.fillStyle(0x333333, 1);
    graphics.fillRect(x, y, size, size);

    graphics.lineStyle(1, 0x555555, 0.3);
    for (let i = 0; i < 5; i++) {
      const px = x + Math.random() * size;
      const py = y + Math.random() * size;
      graphics.lineBetween(px, py, px + 3, py + 1);
    }

    graphics.lineStyle(1, 0x222222, 0.5);
    graphics.strokeRect(x, y, size, size);
  }

  /**
   * Dessine une tile d'herbe à une position spécifique.
   */
  private static drawGrassTile(graphics: Phaser.GameObjects.Graphics, x: number, y: number, size: number): void {
    graphics.fillStyle(0x44aa44, 1);
    graphics.fillRect(x, y, size, size);

    graphics.lineStyle(1, 0x228822, 0.6);
    for (let i = 0; i < 15; i++) {
      const px = x + Math.random() * size;
      const py = y + Math.random() * size;
      graphics.lineBetween(px, py, px, py + 3);
    }

    graphics.lineStyle(1, 0x66cc66, 0.4);
    for (let i = 0; i < 10; i++) {
      const px = x + Math.random() * size;
      const py = y + Math.random() * size;
      graphics.lineBetween(px, py, px, py + 2);
    }

    graphics.lineStyle(1, 0x338833, 0.5);
    graphics.strokeRect(x, y, size, size);
  }

  /**
   * Dessine une tile de sable à une position spécifique.
   */
  private static drawSandTile(graphics: Phaser.GameObjects.Graphics, x: number, y: number, size: number): void {
    graphics.fillStyle(0xeecc88, 1);
    graphics.fillRect(x, y, size, size);

    graphics.fillStyle(0xddbb77, 0.5);
    for (let i = 0; i < 30; i++) {
      const px = x + Math.random() * size;
      const py = y + Math.random() * size;
      graphics.fillCircle(px, py, 1);
    }

    graphics.fillStyle(0xccaa66, 0.3);
    for (let i = 0; i < 20; i++) {
      const px = x + Math.random() * size;
      const py = y + Math.random() * size;
      graphics.fillCircle(px, py, 0.5);
    }

    graphics.lineStyle(1, 0xddaa66, 0.5);
    graphics.strokeRect(x, y, size, size);
  }

  /**
   * Dessine une tile de boue à une position spécifique.
   */
  private static drawMudTile(graphics: Phaser.GameObjects.Graphics, x: number, y: number, size: number): void {
    graphics.fillStyle(0x886644, 1);
    graphics.fillRect(x, y, size, size);

    graphics.fillStyle(0x664422, 0.6);
    for (let i = 0; i < 8; i++) {
      const px = x + Math.random() * size;
      const py = y + Math.random() * size;
      const radius = 2 + Math.random() * 3;
      graphics.fillCircle(px, py, radius);
    }

    graphics.fillStyle(0xaa8866, 0.3);
    for (let i = 0; i < 5; i++) {
      const px = x + Math.random() * size;
      const py = y + Math.random() * size;
      graphics.fillCircle(px, py, 2);
    }

    graphics.lineStyle(1, 0x664422, 0.5);
    graphics.strokeRect(x, y, size, size);
  }

  /**
   * Dessine une tile de gravier à une position spécifique.
   */
  private static drawGravelTile(graphics: Phaser.GameObjects.Graphics, x: number, y: number, size: number): void {
    graphics.fillStyle(0x999999, 1);
    graphics.fillRect(x, y, size, size);

    for (let i = 0; i < 20; i++) {
      const px = x + Math.random() * size;
      const py = y + Math.random() * size;
      const radius = 1 + Math.random() * 2;

      const brightness = 0x666666 + Math.floor(Math.random() * 0x555555);
      graphics.fillStyle(brightness, 0.8);

      graphics.fillCircle(px, py, radius);
    }

    for (let i = 0; i < 5; i++) {
      const px = x + Math.random() * size;
      const py = y + Math.random() * size;
      graphics.fillStyle(0x777777, 0.7);
      graphics.fillCircle(px, py, 2.5);
    }

    graphics.lineStyle(1, 0x888888, 0.5);
    graphics.strokeRect(x, y, size, size);
  }

  /**
   * Génère la texture pour l'asphalte.
   * Couleur : gris foncé avec légères variations
   */
  private static generateAsphaltTile(scene: Phaser.Scene, size: number): void {
    const graphics = scene.make.graphics({ x: 0, y: 0 });

    // Fond gris foncé
    graphics.fillStyle(0x333333, 1);
    graphics.fillRect(0, 0, size, size);

    // Ajouter des variations de texture (petites lignes)
    graphics.lineStyle(1, 0x555555, 0.3);
    for (let i = 0; i < 5; i++) {
      const x = Math.random() * size;
      const y = Math.random() * size;
      graphics.lineBetween(x, y, x + 3, y + 1);
    }

    // Bordure subtile
    graphics.lineStyle(1, 0x222222, 0.5);
    graphics.strokeRect(0, 0, size, size);

    graphics.generateTexture('terrain_asphalt', size, size);
    graphics.destroy();
  }

  /**
   * Génère la texture pour l'herbe.
   * Couleur : vert avec brins d'herbe
   */
  private static generateGrassTile(scene: Phaser.Scene, size: number): void {
    const graphics = scene.make.graphics({ x: 0, y: 0 });

    // Fond vert
    graphics.fillStyle(0x44aa44, 1);
    graphics.fillRect(0, 0, size, size);

    // Brins d'herbe (petites lignes verticales vertes foncées)
    graphics.lineStyle(1, 0x228822, 0.6);
    for (let i = 0; i < 15; i++) {
      const x = Math.random() * size;
      const y = Math.random() * size;
      graphics.lineBetween(x, y, x, y + 3);
    }

    // Quelques brins plus clairs
    graphics.lineStyle(1, 0x66cc66, 0.4);
    for (let i = 0; i < 10; i++) {
      const x = Math.random() * size;
      const y = Math.random() * size;
      graphics.lineBetween(x, y, x, y + 2);
    }

    // Bordure
    graphics.lineStyle(1, 0x338833, 0.5);
    graphics.strokeRect(0, 0, size, size);

    graphics.generateTexture('terrain_grass', size, size);
    graphics.destroy();
  }

  /**
   * Génère la texture pour le sable.
   * Couleur : beige avec points (grains de sable)
   */
  private static generateSandTile(scene: Phaser.Scene, size: number): void {
    const graphics = scene.make.graphics({ x: 0, y: 0 });

    // Fond beige
    graphics.fillStyle(0xeecc88, 1);
    graphics.fillRect(0, 0, size, size);

    // Grains de sable (petits points)
    graphics.fillStyle(0xddbb77, 0.5);
    for (let i = 0; i < 30; i++) {
      const x = Math.random() * size;
      const y = Math.random() * size;
      graphics.fillCircle(x, y, 1);
    }

    // Quelques grains plus foncés
    graphics.fillStyle(0xccaa66, 0.3);
    for (let i = 0; i < 20; i++) {
      const x = Math.random() * size;
      const y = Math.random() * size;
      graphics.fillCircle(x, y, 0.5);
    }

    // Bordure
    graphics.lineStyle(1, 0xddaa66, 0.5);
    graphics.strokeRect(0, 0, size, size);

    graphics.generateTexture('terrain_sand', size, size);
    graphics.destroy();
  }

  /**
   * Génère la texture pour la boue.
   * Couleur : marron foncé avec texture liquide
   */
  private static generateMudTile(scene: Phaser.Scene, size: number): void {
    const graphics = scene.make.graphics({ x: 0, y: 0 });

    // Fond marron foncé
    graphics.fillStyle(0x886644, 1);
    graphics.fillRect(0, 0, size, size);

    // Taches plus foncées (boue humide)
    graphics.fillStyle(0x664422, 0.6);
    for (let i = 0; i < 8; i++) {
      const x = Math.random() * size;
      const y = Math.random() * size;
      const radius = 2 + Math.random() * 3;
      graphics.fillCircle(x, y, radius);
    }

    // Reflets liquides (zones plus claires)
    graphics.fillStyle(0xaa8866, 0.3);
    for (let i = 0; i < 5; i++) {
      const x = Math.random() * size;
      const y = Math.random() * size;
      graphics.fillCircle(x, y, 2);
    }

    // Bordure
    graphics.lineStyle(1, 0x664422, 0.5);
    graphics.strokeRect(0, 0, size, size);

    graphics.generateTexture('terrain_mud', size, size);
    graphics.destroy();
  }

  /**
   * Génère la texture pour le gravier.
   * Couleur : gris clair avec cailloux
   */
  private static generateGravelTile(scene: Phaser.Scene, size: number): void {
    const graphics = scene.make.graphics({ x: 0, y: 0 });

    // Fond gris clair
    graphics.fillStyle(0x999999, 1);
    graphics.fillRect(0, 0, size, size);

    // Cailloux (petits polygones irréguliers)
    for (let i = 0; i < 20; i++) {
      const x = Math.random() * size;
      const y = Math.random() * size;
      const radius = 1 + Math.random() * 2;

      // Couleur variable du caillou
      const brightness = 0x666666 + Math.floor(Math.random() * 0x555555);
      graphics.fillStyle(brightness, 0.8);

      // Forme irrégulière
      graphics.fillCircle(x, y, radius);
    }

    // Quelques cailloux plus gros
    for (let i = 0; i < 5; i++) {
      const x = Math.random() * size;
      const y = Math.random() * size;
      graphics.fillStyle(0x777777, 0.7);
      graphics.fillCircle(x, y, 2.5);
    }

    // Bordure
    graphics.lineStyle(1, 0x888888, 0.5);
    graphics.strokeRect(0, 0, size, size);

    graphics.generateTexture('terrain_gravel', size, size);
    graphics.destroy();
  }

  /**
   * Retourne la clé de texture pour un type de terrain.
   *
   * @param type - Type de terrain
   * @returns Clé de la texture générée
   */
  public static getTextureKey(type: TerrainType): string {
    switch (type) {
      case TerrainType.ASPHALT:
        return 'terrain_asphalt';
      case TerrainType.GRASS:
        return 'terrain_grass';
      case TerrainType.SAND:
        return 'terrain_sand';
      case TerrainType.MUD:
        return 'terrain_mud';
      case TerrainType.GRAVEL:
        return 'terrain_gravel';
      default:
        console.warn(`[TerrainTileGenerator] Type inconnu: ${type}`);
        return 'terrain_asphalt';
    }
  }
}
