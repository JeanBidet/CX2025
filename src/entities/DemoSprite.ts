import Phaser from 'phaser';
import { RotationComponent } from '@/components/RotationComponent';
import type { IComponent } from '@/types/IComponent';

/**
 * Sprite de démonstration illustrant l'architecture Entity-Component.
 *
 * Démontre :
 * - Comment créer une entité héritant de Phaser.GameObjects.Sprite
 * - Comment attacher des composants métier à un GameObject
 * - Comment gérer le cycle de vie des composants
 * - La séparation entre rendu (Phaser) et logique métier (Components)
 *
 * @example
 * ```typescript
 * // Dans RaceScene.create()
 * const demoSprite = new DemoSprite(this, 400, 300);
 * this.add.existing(demoSprite);
 * ```
 */
export class DemoSprite extends Phaser.GameObjects.Sprite {
  /**
   * Liste des composants métier attachés à ce sprite.
   */
  private components: IComponent[] = [];

  /**
   * Crée un nouveau sprite de démonstration.
   *
   * @param scene - La scène Phaser qui possède ce sprite
   * @param x - Position X
   * @param y - Position Y
   */
  constructor(scene: Phaser.Scene, x: number, y: number) {
    // Créer un sprite rectangulaire via les Graphics de Phaser
    // (en attendant de charger de vrais sprites dans les prompts suivants)
    super(scene, x, y, '');

    // Créer une texture procédurale simple
    this.createTexture(scene);

    // Ajouter un composant de rotation comme démonstration
    this.addComponent(new RotationComponent(this, 90)); // 90°/seconde

    // Initialiser tous les composants
    this.initializeComponents();

    console.log('[DemoSprite] Créé à la position', x, y);
  }

  /**
   * Crée une texture procédurale simple pour la démonstration.
   * Dans les prompts suivants, on utilisera de vraies images.
   */
  private createTexture(scene: Phaser.Scene): void {
    const key = 'demo-sprite';

    // Vérifier si la texture existe déjà
    if (!scene.textures.exists(key)) {
      // Créer un Graphics temporaire
      const graphics = scene.add.graphics({ x: 0, y: 0 });

      // Dessiner un rectangle avec un contour
      graphics.fillStyle(0xff6b6b, 1); // Rouge clair
      graphics.fillRect(0, 0, 60, 60);
      graphics.lineStyle(4, 0xffffff, 1); // Contour blanc
      graphics.strokeRect(0, 0, 60, 60);

      // Dessiner une croix pour voir la rotation
      graphics.lineStyle(2, 0xffffff, 1);
      graphics.lineBetween(0, 0, 60, 60);
      graphics.lineBetween(60, 0, 0, 60);

      // Générer la texture depuis le Graphics
      graphics.generateTexture(key, 60, 60);
      graphics.destroy();
    }

    // Appliquer la texture
    this.setTexture(key);
    this.setOrigin(0.5);
  }

  /**
   * Ajoute un composant à ce sprite.
   *
   * @param component - Le composant à ajouter
   */
  public addComponent(component: IComponent): void {
    this.components.push(component);
  }

  /**
   * Retire un composant de ce sprite.
   *
   * @param component - Le composant à retirer
   */
  public removeComponent(component: IComponent): void {
    const index = this.components.indexOf(component);
    if (index !== -1) {
      this.components.splice(index, 1);
      component.destroy();
    }
  }

  /**
   * Initialise tous les composants attachés.
   */
  private initializeComponents(): void {
    this.components.forEach(component => component.init());
  }

  /**
   * Met à jour tous les composants attachés.
   * Cette méthode doit être appelée depuis le update() de la scène.
   *
   * @param time - Temps total écoulé depuis le début du jeu (ms)
   * @param delta - Temps écoulé depuis la dernière frame (ms)
   */
  public updateComponents(time: number, delta: number): void {
    this.components.forEach(component => {
      component.preUpdate(time, delta);
      component.update(time, delta);
    });
  }

  /**
   * Détruit le sprite et tous ses composants.
   * Surcharge la méthode destroy de Phaser.
   *
   * @param fromScene - Indique si la destruction vient de la scène
   */
  public destroy(fromScene?: boolean): void {
    // Détruire tous les composants
    this.components.forEach(component => component.destroy());
    this.components = [];

    // Appeler la méthode destroy de Phaser
    super.destroy(fromScene);

    console.log('[DemoSprite] Détruit');
  }

  /**
   * Récupère un composant d'un type spécifique.
   *
   * @template T - Type du composant recherché
   * @param componentClass - Classe du composant recherché
   * @returns Le composant trouvé ou undefined
   */
  public getComponent<T extends IComponent>(componentClass: new (...args: any[]) => T): T | undefined {
    return this.components.find(c => c instanceof componentClass) as T | undefined;
  }
}
