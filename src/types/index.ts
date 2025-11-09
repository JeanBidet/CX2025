/**
 * Point d'entrée pour tous les types TypeScript du jeu.
 * Centralise les exports pour faciliter les imports.
 */

// Interfaces de patterns
export type { IComponent } from './IComponent';
export type { ICommand } from './ICommand';
export type { IGameCommand } from './IGameCommand';
export type { IState } from './IState';
export type { IStrategy } from './IStrategy';

// Enums
export {
  TerrainType,
  CyclistState,
  ObstacleType,
  AIDifficulty,
  CommandType,
} from './enums';

// Types de données métier
export type {
  CyclistStats,
  ObstacleData,
  AIConfig,
  RaceResult,
  RaceConfig,
} from './gameData';

// Types de terrain (nouveau système détaillé)
export type {
  TerrainData,
  TerrainCreationOptions,
  TerrainInstance,
  TerrainMapConfig,
} from './terrain';
