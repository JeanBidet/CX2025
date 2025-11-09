import Phaser from 'phaser';
import type { IComponent } from '../types/IComponent';
import { BalanceComponent } from '@components/BalanceComponent';
import {
  CYCLIST_WIDTH,
  CYCLIST_HEIGHT,
  CYCLIST_MAX_SPEED,
  CYCLIST_DRAG,
  CYCLIST_MASS,
  CYCLIST_BOUNCE,
} from '@config/constants';

/**
 * Classe représentant un cycliste dans le jeu.
 *
 * Hérite de Phaser.Physics.Arcade.Sprite pour bénéficier automatiquement :
 * - Du système de physique (velocity, acceleration, drag, mass)
 * - Des collisions Arcade Physics
 * - De l'intégration automatique dans le monde physique
 *
 * Architecture :
 * - Le body Phaser gère la physique bas niveau
 * - Les composants ajoutent la logique métier (mouvement, input, rotation)
 * - Séparation claire entre rendu (Phaser) et logique (Components)
 *
 * @example
 * ```typescript
 * // Dans RaceScene.create()
 * const cyclist = new Cyclist(this, 100, 300, true);
 * this.physics.add.existing(cyclist);
 *
 * // Ajouter des composants
 * cyclist.addComponent(new MovementComponent(cyclist));
 * cyclist.addComponent(new InputComponent(cyclist));
 * ```
 */
export class Cyclist extends Phaser.Physics.Arcade.Sprite {
  // ============================================================================
  // PROPRIÉTÉS
  // ============================================================================

  /** Liste des composants métier attachés à ce cycliste */
  private components: IComponent[] = [];

  /** Indique si c'est le cycliste du joueur (vs IA) */
  private isPlayer: boolean;

  /** Nom du cycliste */
  private cyclistName: string;

  /**
   * Facteur d'échelle du sprite.
   * Valeur documentée : 0.2 permet au cycliste d'être visible sans être trop gros.
   * Ajustable selon les besoins de gameplay.
   */
  private readonly SPRITE_SCALE = 0.2;

  /**
   * Offset d'angle pour corriger l'orientation native du sprite.
   *
   * Les sprites PNG sont orientés vers le HAUT dans l'image source (rotation native = 0).
   * Dans Phaser, l'angle 0 correspond à la DROITE pour le mouvement.
   *
   * Pour convertir la rotation du sprite en angle de mouvement Phaser :
   * - Sprite pointe vers le haut (rotation = 0) → doit se déplacer vers le haut (angle = -π/2)
   * - Sprite pointe vers la droite (rotation = π/2) → doit se déplacer vers la droite (angle = 0)
   *
   * Formule : angle_mouvement = rotation_sprite - SPRITE_ANGLE_OFFSET
   * Donc : SPRITE_ANGLE_OFFSET = π/2
   *
   * Valeur : Math.PI / 2 (90 degrés)
   */
  public static readonly SPRITE_ANGLE_OFFSET = Math.PI / 2;

  // ============================================================================
  // CONSTRUCTEUR
  // ============================================================================

  /**
   * Crée un nouveau cycliste.
   *
   * @param scene - La scène Phaser propriétaire
   * @param x - Position X initiale
   * @param y - Position Y initiale
   * @param isPlayer - true si c'est le joueur, false si IA
   * @param name - Nom du cycliste (optionnel)
   */
  constructor(
    scene: Phaser.Scene,
    x: number,
    y: number,
    isPlayer: boolean = false,
    name: string = 'Cyclist'
  ) {
    // Appeler le constructeur parent avec la première frame du sprite réel
    // Si le sprite n'existe pas, utilisera une texture vide
    super(scene, x, y, 'cyclist-frame-0');

    this.isPlayer = isPlayer;
    this.cyclistName = name;

    // Si le sprite réel n'existe pas, créer une texture procédurale en fallback
    if (!scene.textures.exists('cyclist-frame-0')) {
      console.warn('[Cyclist] Sprites réels non trouvés, utilisation de textures procédurales');
      this.createTemporaryTexture(scene);
    }

    // Configurer le sprite (scale, origin, depth)
    this.setupSprite();

    // Note : setupPhysics() sera appelé depuis RaceScene après physics.add.existing()
    // Le body n'existe pas encore à ce stade du constructeur

    // Lancer l'animation de pédalage si disponible
    this.playRideAnimation();

    console.log(`[Cyclist] ${name} créé à (${x}, ${y}) - Joueur: ${isPlayer}`);
  }

  // ============================================================================
  // CONFIGURATION
  // ============================================================================

  /**
   * Configure les propriétés visuelles du sprite.
   *
   * Configuration appliquée :
   * - setScale: Agrandit le sprite pour qu'il soit visible
   * - setOrigin: Centre le sprite pour rotation centrée (0.5, 0.5)
   * - setDepth: Assure que le cycliste est au-dessus du terrain (10)
   * - setRotation: Rotation initiale pour orienter le sprite vers la droite au démarrage
   *
   * Note sur la rotation initiale :
   * Le sprite PNG natif pointe vers le HAUT (rotation = 0).
   * Pour qu'il pointe vers la DROITE au démarrage (direction par défaut),
   * on applique SPRITE_ANGLE_OFFSET comme rotation initiale.
   *
   * Formule : rotation_sprite = angle_mouvement_désiré + SPRITE_ANGLE_OFFSET
   * Pour démarrer vers la droite : rotation = 0 + π/2 = π/2
   */
  private setupSprite(): void {
    // Agrandir le sprite pour meilleure visibilité
    this.setScale(this.SPRITE_SCALE);

    // Centrer l'origine pour que la rotation se fasse au centre du sprite
    this.setOrigin(0.5, 0.5);

    // Définir la profondeur pour s'assurer que le cycliste est visible au-dessus du terrain
    // Valeurs typiques : terrain = 0, cycliste = 10, UI = 100+
    this.setDepth(10);

    // Définir la rotation initiale pour orienter le cycliste vers la droite
    // Utilise SPRITE_ANGLE_OFFSET pour compenser l'orientation native du sprite
    this.setRotation(Cyclist.SPRITE_ANGLE_OFFSET);

    console.log('[Cyclist] Sprite configuré (scale: 0.2, origin: center, depth: 10, rotation initiale: 90°)');
  }

  /**
   * Crée une texture procédurale temporaire.
   * Utilisée comme fallback si les sprites réels ne sont pas chargés.
   */
  private createTemporaryTexture(scene: Phaser.Scene): void {
    const key = this.isPlayer ? 'cyclist-player' : 'cyclist-ai';

    // Vérifier si la texture existe déjà
    if (!scene.textures.exists(key)) {
      const graphics = scene.add.graphics({ x: 0, y: 0});

      // Couleur différente pour joueur vs IA
      const color = this.isPlayer ? 0x4ECDC4 : 0xFF6B6B; // Cyan pour joueur, Rouge pour IA

      // Dessiner un rectangle représentant le cycliste
      graphics.fillStyle(color, 1);
      graphics.fillRect(0, 0, CYCLIST_WIDTH, CYCLIST_HEIGHT);

      // Contour blanc
      graphics.lineStyle(3, 0xFFFFFF, 1);
      graphics.strokeRect(0, 0, CYCLIST_WIDTH, CYCLIST_HEIGHT);

      // Indicateur de direction (triangle vers le haut)
      graphics.fillStyle(0xFFFFFF, 1);
      graphics.fillTriangle(
        CYCLIST_WIDTH / 2, 5,           // Sommet
        CYCLIST_WIDTH / 2 - 8, 15,      // Bas gauche
        CYCLIST_WIDTH / 2 + 8, 15       // Bas droite
      );

      // Générer la texture
      graphics.generateTexture(key, CYCLIST_WIDTH, CYCLIST_HEIGHT);
      graphics.destroy();
    }

    // Appliquer la texture
    this.setTexture(key);
    this.setOrigin(0.5);
  }

  /**
   * Configure le body physique Arcade.
   *
   * IMPORTANT : Cette méthode doit être appelée APRÈS physics.add.existing()
   * car le body n'existe pas avant.
   *
   * Paramètres importants :
   * - setSize : taille du corps physique (hitbox)
   * - setOffset : décalage de la hitbox par rapport au sprite
   * - setMaxVelocity : vitesse maximale autorisée
   * - setDrag : résistance naturelle (friction de l'air)
   * - setMass : masse (affecte l'inertie)
   * - setBounce : élasticité lors des collisions
   *
   * Configuration de la hitbox :
   * - La hitbox est plus petite que le sprite visuel (0.6x) pour compenser le scale
   * - Cela évite les collisions trop larges et améliore le gameplay
   * - L'offset centre la hitbox sur le sprite après scaling
   * - Justification : Un cycliste ne doit pas collider avec tout son sprite visuel,
   *   seulement la partie "solide" (corps + vélo)
   */
  public initializePhysics(): void {
    // S'assurer que le body existe (devrait être créé automatiquement)
    if (!this.body) {
      console.warn('[Cyclist] Body physique non trouvé');
      return;
    }

    const body = this.body as Phaser.Physics.Arcade.Body;

    // Taille du corps physique (hitbox) - plus petite que le sprite visuel
    // 0.6 * dimensions originales pour une hitbox réaliste
    const hitboxWidth = CYCLIST_WIDTH * 0.6;
    const hitboxHeight = CYCLIST_HEIGHT * 0.6;
    body.setSize(hitboxWidth, hitboxHeight);

    // Centrer la hitbox sur le sprite
    // L'offset doit compenser la différence entre la taille du sprite et la hitbox
    const offsetX = (CYCLIST_WIDTH - hitboxWidth) / 2;
    const offsetY = (CYCLIST_HEIGHT - hitboxHeight) / 2;
    body.setOffset(offsetX, offsetY);

    // Vitesse maximale (sera modifiée par le MovementComponent selon le contexte)
    body.setMaxVelocity(CYCLIST_MAX_SPEED, CYCLIST_MAX_SPEED);

    // Drag : résistance qui réduit progressivement la vitesse
    // Plus c'est élevé, plus le cycliste ralentit rapidement
    body.setDrag(CYCLIST_DRAG * 10000); // Multiplié pour avoir un effet perceptible

    // Masse : affecte l'inertie et les collisions
    body.setMass(CYCLIST_MASS);

    // Bounce : élasticité lors des collisions
    body.setBounce(CYCLIST_BOUNCE);

    // Collisions avec les bords du monde (désactivé pour l'instant)
    body.setCollideWorldBounds(false);

    // Activer le body
    body.enable = true;

    console.log(
      `[Cyclist] Physique configurée - Hitbox: ${hitboxWidth}x${hitboxHeight}, ` +
      `Offset: (${offsetX}, ${offsetY})`
    );
  }

  // ============================================================================
  // GESTION DES COMPOSANTS
  // ============================================================================

  /**
   * Ajoute un composant au cycliste.
   *
   * @param component - Le composant à ajouter
   * @returns this pour chaînage
   */
  public addComponent(component: IComponent): this {
    this.components.push(component);
    component.init();
    return this;
  }

  /**
   * Retire un composant du cycliste.
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
   * Récupère un composant d'un type spécifique.
   *
   * @template T - Type du composant recherché
   * @param componentClass - Classe du composant
   * @returns Le composant trouvé ou undefined
   */
  public getComponent<T extends IComponent>(
    componentClass: new (...args: any[]) => T
  ): T | undefined {
    return this.components.find(c => c instanceof componentClass) as T | undefined;
  }

  // ============================================================================
  // CYCLE DE VIE PHASER
  // ============================================================================

  /**
   * PreUpdate est appelé automatiquement par Phaser avant update().
   * C'est ici que Phaser met à jour la physique.
   *
   * On l'override pour appeler les preUpdate des composants.
   *
   * Note : La rotation est gérée par les commandes TurnLeft/TurnRight,
   * pas par la vélocité. Cela permet de tourner indépendamment du mouvement.
   *
   * L'oscillation visuelle de l'équilibre est appliquée ici en addition
   * à la rotation contrôlée par le joueur.
   *
   * @param time - Temps total écoulé (ms)
   * @param delta - Temps depuis dernière frame (ms)
   */
  preUpdate(time: number, delta: number): void {
    // Appeler le preUpdate parent (important pour Phaser)
    super.preUpdate(time, delta);

    // Appeler le preUpdate de chaque composant
    this.components.forEach(component => {
      component.preUpdate(time, delta);
    });

    // Appliquer l'oscillation visuelle de l'équilibre
    this.applyBalanceOscillation(time);
  }

  /**
   * Applique l'oscillation visuelle selon le déséquilibre.
   * Plus le cycliste est déséquilibré, plus il oscille.
   *
   * @param time - Temps actuel (ms)
   */
  private applyBalanceOscillation(time: number): void {
    // Récupérer le composant d'équilibre
    const balanceComponent = this.getComponent(BalanceComponent);

    if (!balanceComponent) {
      return;
    }

    // Calculer l'angle d'oscillation
    const oscillationAngle = balanceComponent.getOscillationAngle(time);

    // L'oscillation s'ajoute à la rotation de base (contrôlée par les commandes)
    // On ne modifie PAS this.rotation directement pour ne pas interférer avec les commandes
    // On stocke l'angle de base et on ajoute l'oscillation
    const baseRotation = this.rotation;

    // Appliquer l'oscillation (en radians)
    this.setRotation(baseRotation + oscillationAngle);
  }

  /**
   * Update personnalisé pour la logique métier.
   * Appelé manuellement depuis la scène.
   *
   * @param time - Temps total écoulé (ms)
   * @param delta - Temps depuis dernière frame (ms)
   */
  public updateComponents(time: number, delta: number): void {
    this.components.forEach(component => {
      component.update(time, delta);
    });
  }

  /**
   * Détruit le cycliste et tous ses composants.
   *
   * @param fromScene - Indique si la destruction vient de la scène
   */
  public destroy(fromScene?: boolean): void {
    // Détruire tous les composants
    this.components.forEach(component => component.destroy());
    this.components = [];

    // Appeler la méthode destroy de Phaser
    super.destroy(fromScene);

    console.log(`[Cyclist] ${this.cyclistName} détruit`);
  }

  // ============================================================================
  // MÉTHODES D'ANIMATION (Interface publique pour State Pattern)
  // ============================================================================

  /**
   * Lance l'animation de pédalage (riding).
   *
   * Cette méthode est publique et sera appelée par le RidingState
   * lors de la transition vers l'état RIDING.
   *
   * Optimisation : Vérifie que l'animation n'est pas déjà en cours
   * pour éviter de la relancer inutilement.
   */
  public playRideAnimation(): void {
    // Vérifier que l'animation existe dans la scène
    if (!this.scene.anims.exists('ride')) {
      console.warn('[Cyclist] Animation "ride" non trouvée, animation ignorée');
      return;
    }

    // Optimisation : Ne relancer l'animation que si elle n'est pas déjà en cours
    if (this.anims.currentAnim?.key !== 'ride' || !this.anims.isPlaying) {
      this.play('ride');
      console.log('[Cyclist] Animation "ride" lancée');
    }
  }

  /**
   * Lance l'animation de portage (carrying).
   *
   * Cette méthode sera appelée par le CarryingState.
   * Pour l'instant, utilise l'animation procédurale générée.
   */
  public playCarryAnimation(): void {
    const animKey = this.isPlayer ? 'player_carry' : 'ai_carry';

    if (this.scene.anims.exists(animKey)) {
      if (this.anims.currentAnim?.key !== animKey || !this.anims.isPlaying) {
        this.play(animKey);
        console.log(`[Cyclist] Animation "${animKey}" lancée`);
      }
    }
  }

  /**
   * Lance l'animation de remontée sur le vélo (remounting).
   *
   * Cette méthode sera appelée par le RemountingState.
   * Pour l'instant, utilise l'animation procédurale générée.
   */
  public playRemountAnimation(): void {
    const animKey = this.isPlayer ? 'player_remount' : 'ai_remount';

    if (this.scene.anims.exists(animKey)) {
      if (this.anims.currentAnim?.key !== animKey || !this.anims.isPlaying) {
        this.play(animKey);
        console.log(`[Cyclist] Animation "${animKey}" lancée`);
      }
    }
  }

  /**
   * Lance l'animation de crash.
   *
   * Cette méthode sera appelée par le CrashedState.
   * Pour l'instant, utilise l'animation procédurale générée.
   */
  public playCrashAnimation(): void {
    const animKey = this.isPlayer ? 'player_crash' : 'ai_crash';

    if (this.scene.anims.exists(animKey)) {
      if (this.anims.currentAnim?.key !== animKey || !this.anims.isPlaying) {
        this.play(animKey);
        console.log(`[Cyclist] Animation "${animKey}" lancée`);
      }
    }
  }

  /**
   * Arrête l'animation actuelle et efface les teintes.
   *
   * Cette méthode est utile lors des transitions d'état.
   */
  public stopAnimation(): void {
    this.stop();
    this.clearTint();
  }

  // ============================================================================
  // GETTERS / SETTERS
  // ============================================================================

  /**
   * Vérifie si c'est le joueur.
   */
  public getIsPlayer(): boolean {
    return this.isPlayer;
  }

  /**
   * Récupère le nom du cycliste.
   */
  public getName(): string {
    return this.cyclistName;
  }

  /**
   * Récupère le body Arcade casté.
   */
  public getBody(): Phaser.Physics.Arcade.Body {
    return this.body as Phaser.Physics.Arcade.Body;
  }
}
