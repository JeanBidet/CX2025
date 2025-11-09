/**
 * CyclistAnimationGenerator - Creates cyclist animation frames programmatically
 *
 * Generates visual frames for each cyclist state:
 * - RIDING: Normal cycling pose (multiple frames)
 * - CARRYING: Walking with bike pose (multiple frames)
 * - REMOUNTING: Getting on bike transition (multiple frames)
 * - CRASHED: Fallen over pose (single frame)
 *
 * Since we don't have sprite sheets, we generate distinct visual representations
 * for each state to make state changes clearly visible.
 */

import { CYCLIST_WIDTH, CYCLIST_HEIGHT } from '@config/constants';

export class CyclistAnimationGenerator {
  /**
   * Generate all cyclist animation textures
   * Should be called in preload() or create() before creating cyclists
   */
  public static generateAll(scene: Phaser.Scene, isPlayer: boolean = true): void {
    this.generateRidingFrames(scene, isPlayer);
    this.generateCarryingFrames(scene, isPlayer);
    this.generateRemountingFrames(scene, isPlayer);
    this.generateCrashedFrame(scene, isPlayer);
  }

  /**
   * Generate RIDING animation frames (normal cycling)
   * Creates 4 frames showing cycling motion
   */
  private static generateRidingFrames(scene: Phaser.Scene, isPlayer: boolean): void {
    const prefix = isPlayer ? 'player' : 'ai';
    const baseColor = isPlayer ? 0x4ecdc4 : 0xff6b6b; // Cyan for player, Red for AI

    for (let frame = 0; frame < 4; frame++) {
      const key = `${prefix}_ride_${frame}`;

      if (!scene.textures.exists(key)) {
        const graphics = scene.add.graphics({ x: 0, y: 0 });

        // Base cyclist body
        graphics.fillStyle(baseColor, 1);
        graphics.fillRect(0, 0, CYCLIST_WIDTH, CYCLIST_HEIGHT);

        // White outline
        graphics.lineStyle(2, 0xffffff, 1);
        graphics.strokeRect(0, 0, CYCLIST_WIDTH, CYCLIST_HEIGHT);

        // Direction indicator (triangle) - animated position
        graphics.fillStyle(0xffffff, 1);
        const offset = Math.sin((frame * Math.PI) / 2) * 3; // Subtle bobbing
        graphics.fillTriangle(
          CYCLIST_WIDTH / 2,
          5 + offset,
          CYCLIST_WIDTH / 2 - 8,
          15 + offset,
          CYCLIST_WIDTH / 2 + 8,
          15 + offset
        );

        // Wheel indicators (animated)
        graphics.fillStyle(0x333333, 1);
        graphics.fillCircle(12, CYCLIST_HEIGHT - 5 + offset, 4);
        graphics.fillCircle(CYCLIST_WIDTH - 12, CYCLIST_HEIGHT - 5 - offset, 4);

        graphics.generateTexture(key, CYCLIST_WIDTH, CYCLIST_HEIGHT);
        graphics.destroy();
      }
    }
  }

  /**
   * Generate CARRYING animation frames (walking with bike)
   * Creates 4 frames showing walking motion
   */
  private static generateCarryingFrames(scene: Phaser.Scene, isPlayer: boolean): void {
    const prefix = isPlayer ? 'player' : 'ai';
    const baseColor = isPlayer ? 0x4ecdc4 : 0xff6b6b;

    for (let frame = 0; frame < 4; frame++) {
      const key = `${prefix}_carry_${frame}`;

      if (!scene.textures.exists(key)) {
        const graphics = scene.add.graphics({ x: 0, y: 0 });

        // Body slightly smaller (walking stance)
        graphics.fillStyle(baseColor, 0.9);
        graphics.fillRect(2, 4, CYCLIST_WIDTH - 4, CYCLIST_HEIGHT - 4);

        // Blue tint to indicate carrying state
        graphics.fillStyle(0x8888ff, 0.3);
        graphics.fillRect(2, 4, CYCLIST_WIDTH - 4, CYCLIST_HEIGHT - 4);

        // Outline
        graphics.lineStyle(2, 0xffffff, 1);
        graphics.strokeRect(2, 4, CYCLIST_WIDTH - 4, CYCLIST_HEIGHT - 4);

        // Walking motion indicator - alternating sides
        const side = frame % 2 === 0 ? -1 : 1;
        graphics.fillStyle(0xffffff, 1);
        graphics.fillCircle(CYCLIST_WIDTH / 2 + side * 8, CYCLIST_HEIGHT / 2, 3);

        // Bike wheels beside (being pushed)
        graphics.fillStyle(0x333333, 0.7);
        graphics.fillCircle(CYCLIST_WIDTH + 5, 8, 5);
        graphics.fillCircle(CYCLIST_WIDTH + 5, CYCLIST_HEIGHT - 8, 5);

        graphics.generateTexture(key, CYCLIST_WIDTH + 10, CYCLIST_HEIGHT);
        graphics.destroy();
      }
    }
  }

  /**
   * Generate REMOUNTING animation frames (getting on bike)
   * Creates 3 frames showing mounting transition
   */
  private static generateRemountingFrames(scene: Phaser.Scene, isPlayer: boolean): void {
    const prefix = isPlayer ? 'player' : 'ai';
    const baseColor = isPlayer ? 0x4ecdc4 : 0xff6b6b;

    for (let frame = 0; frame < 3; frame++) {
      const key = `${prefix}_remount_${frame}`;

      if (!scene.textures.exists(key)) {
        const graphics = scene.add.graphics({ x: 0, y: 0 });

        // Progressive mounting - body gets higher
        const heightOffset = frame * 3;
        graphics.fillStyle(baseColor, 1);
        graphics.fillRect(0, heightOffset, CYCLIST_WIDTH, CYCLIST_HEIGHT - heightOffset);

        // Yellow tint during remount
        graphics.fillStyle(0xffff88, 0.4);
        graphics.fillRect(0, heightOffset, CYCLIST_WIDTH, CYCLIST_HEIGHT - heightOffset);

        // Outline
        graphics.lineStyle(2, 0xffffff, 1);
        graphics.strokeRect(0, heightOffset, CYCLIST_WIDTH, CYCLIST_HEIGHT - heightOffset);

        // Mounting indicator
        graphics.fillStyle(0xffffff, 1);
        graphics.fillCircle(CYCLIST_WIDTH / 2, CYCLIST_HEIGHT / 2, 4 - frame);

        graphics.generateTexture(key, CYCLIST_WIDTH, CYCLIST_HEIGHT);
        graphics.destroy();
      }
    }
  }

  /**
   * Generate CRASHED frame (fallen over)
   * Single frame showing crashed state
   */
  private static generateCrashedFrame(scene: Phaser.Scene, isPlayer: boolean): void {
    const prefix = isPlayer ? 'player' : 'ai';
    const key = `${prefix}_crash_0`;
    const baseColor = isPlayer ? 0x4ecdc4 : 0xff6b6b;

    if (!scene.textures.exists(key)) {
      const graphics = scene.add.graphics({ x: 0, y: 0 });

      // Flattened body (fallen over) - rotated rectangle shape
      graphics.fillStyle(baseColor, 0.8);
      graphics.fillRect(0, CYCLIST_HEIGHT / 2 - 8, CYCLIST_WIDTH + 10, 16);

      // Red tint for crash
      graphics.fillStyle(0xff0000, 0.3);
      graphics.fillRect(0, CYCLIST_HEIGHT / 2 - 8, CYCLIST_WIDTH + 10, 16);

      // Outline
      graphics.lineStyle(2, 0xff0000, 0.8);
      graphics.strokeRect(0, CYCLIST_HEIGHT / 2 - 8, CYCLIST_WIDTH + 10, 16);

      // Crash indicator (X mark)
      graphics.lineStyle(3, 0xffffff, 0.9);
      graphics.beginPath();
      graphics.moveTo(5, CYCLIST_HEIGHT / 2 - 5);
      graphics.lineTo(15, CYCLIST_HEIGHT / 2 + 5);
      graphics.moveTo(15, CYCLIST_HEIGHT / 2 - 5);
      graphics.lineTo(5, CYCLIST_HEIGHT / 2 + 5);
      graphics.strokePath();

      graphics.generateTexture(key, CYCLIST_WIDTH + 10, CYCLIST_HEIGHT);
      graphics.destroy();
    }
  }

  /**
   * Create Phaser animations from generated frames
   * Should be called in create() after generating textures
   */
  public static createAnimations(scene: Phaser.Scene, isPlayer: boolean = true): void {
    const prefix = isPlayer ? 'player' : 'ai';

    // RIDING animation - 4 frames looping
    if (!scene.anims.exists(`${prefix}_ride`)) {
      scene.anims.create({
        key: `${prefix}_ride`,
        frames: [
          { key: `${prefix}_ride_0` },
          { key: `${prefix}_ride_1` },
          { key: `${prefix}_ride_2` },
          { key: `${prefix}_ride_3` },
        ],
        frameRate: 8,
        repeat: -1, // Loop forever
      });
    }

    // CARRYING animation - 4 frames looping
    if (!scene.anims.exists(`${prefix}_carry`)) {
      scene.anims.create({
        key: `${prefix}_carry`,
        frames: [
          { key: `${prefix}_carry_0` },
          { key: `${prefix}_carry_1` },
          { key: `${prefix}_carry_2` },
          { key: `${prefix}_carry_3` },
        ],
        frameRate: 5,
        repeat: -1,
      });
    }

    // REMOUNTING animation - 3 frames, plays once
    if (!scene.anims.exists(`${prefix}_remount`)) {
      scene.anims.create({
        key: `${prefix}_remount`,
        frames: [
          { key: `${prefix}_remount_0` },
          { key: `${prefix}_remount_1` },
          { key: `${prefix}_remount_2` },
        ],
        frameRate: 3,
        repeat: 0, // Play once
      });
    }

    // CRASHED animation - single frame
    if (!scene.anims.exists(`${prefix}_crash`)) {
      scene.anims.create({
        key: `${prefix}_crash`,
        frames: [{ key: `${prefix}_crash_0` }],
        frameRate: 1,
        repeat: 0,
      });
    }

    console.log(`[CyclistAnimationGenerator] Animations created for ${prefix}`);
  }

  /**
   * Get the animation key for a specific state
   * Helper method to ensure consistency
   */
  public static getAnimationKey(state: string, isPlayer: boolean): string {
    const prefix = isPlayer ? 'player' : 'ai';
    return `${prefix}_${state.toLowerCase()}`;
  }
}
