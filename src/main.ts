import Phaser from 'phaser';
import { gameConfig } from '@config/gameConfig';
import { RaceScene } from '@scenes/RaceScene';

/**
 * Point d'entrée principal de l'application CycloCross 2025.
 *
 * Ce fichier :
 * 1. Importe la configuration Phaser
 * 2. Enregistre toutes les scènes du jeu
 * 3. Crée et initialise l'instance du jeu Phaser
 * 4. Démarre la première scène
 *
 * L'instance du jeu est exportée pour permettre l'accès global si nécessaire
 * (debugging, tests, etc.)
 */

/**
 * Initialise et démarre le jeu.
 */
function startGame(): Phaser.Game {
  console.log('═══════════════════════════════════════════════════════════');
  console.log('  CycloCross 2025 - Initialisation');
  console.log('  Phaser 3 + TypeScript + Vite');
  console.log('═══════════════════════════════════════════════════════════');

  // Cloner la configuration pour éviter les modifications non désirées
  const config: Phaser.Types.Core.GameConfig = {
    ...gameConfig,
    // Ajouter les scènes du jeu
    scene: [
      RaceScene,
      // Les autres scènes seront ajoutées dans les prompts suivants :
      // MenuScene,
      // ResultsScene,
      // etc.
    ],
  };

  // Créer l'instance du jeu Phaser
  const game = new Phaser.Game(config);

  console.log('[Main] Jeu créé avec succès');
  console.log('[Main] Dimensions:', config.width, 'x', config.height);
  console.log('[Main] Type de rendu:', config.type === Phaser.AUTO ? 'AUTO' : config.type);

  // Événements globaux du jeu
  game.events.on('ready', () => {
    console.log('[Main] Jeu prêt - Démarrage de RaceScene');
  });

  game.events.on('hidden', () => {
    console.log('[Main] Jeu caché (onglet inactif) - Pause automatique');
  });

  game.events.on('visible', () => {
    console.log('[Main] Jeu visible (onglet actif) - Reprise');
  });

  // Gestion des erreurs Phaser
  game.events.on('boot', () => {
    console.log('[Main] Boot du jeu terminé');
  });

  return game;
}

/**
 * Instance globale du jeu.
 * Accessible via window.game dans la console du navigateur pour le débogage.
 */
const game = startGame();

// Exposer l'instance du jeu globalement pour le débogage
if (typeof window !== 'undefined') {
  (window as any).game = game;
  console.log('[Main] Instance du jeu exposée globalement (window.game)');
}

// Export pour usage éventuel dans d'autres modules
export default game;
