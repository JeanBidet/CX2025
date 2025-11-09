import Phaser from 'phaser';

/**
 * Classe utilitaire pour les opérations mathématiques courantes.
 * Complète les fonctions de Phaser.Math avec des méthodes spécifiques au jeu.
 */
export class MathUtils {
  /**
   * Effectue une interpolation linéaire entre deux valeurs.
   * Alternative à Phaser.Math.Linear si besoin de logique custom.
   *
   * @param start - Valeur de départ
   * @param end - Valeur de fin
   * @param t - Facteur d'interpolation (0-1)
   * @returns Valeur interpolée
   */
  static lerp(start: number, end: number, t: number): number {
    return start + (end - start) * Phaser.Math.Clamp(t, 0, 1);
  }

  /**
   * Clamp une valeur entre un minimum et un maximum.
   * Wrapper de Phaser.Math.Clamp pour cohérence.
   *
   * @param value - Valeur à clamp
   * @param min - Valeur minimale
   * @param max - Valeur maximale
   * @returns Valeur clampée
   */
  static clamp(value: number, min: number, max: number): number {
    return Phaser.Math.Clamp(value, min, max);
  }

  /**
   * Calcule la distance entre deux points.
   *
   * @param x1 - Position X du premier point
   * @param y1 - Position Y du premier point
   * @param x2 - Position X du second point
   * @param y2 - Position Y du second point
   * @returns Distance euclidienne
   */
  static distance(x1: number, y1: number, x2: number, y2: number): number {
    return Phaser.Math.Distance.Between(x1, y1, x2, y2);
  }

  /**
   * Calcule la distance entre deux vecteurs.
   *
   * @param v1 - Premier vecteur
   * @param v2 - Second vecteur
   * @returns Distance euclidienne
   */
  static distanceVec(v1: Phaser.Math.Vector2, v2: Phaser.Math.Vector2): number {
    return v1.distance(v2);
  }

  /**
   * Normalise une valeur dans une plage vers une autre plage.
   *
   * @param value - Valeur à normaliser
   * @param inMin - Minimum de la plage d'entrée
   * @param inMax - Maximum de la plage d'entrée
   * @param outMin - Minimum de la plage de sortie
   * @param outMax - Maximum de la plage de sortie
   * @returns Valeur normalisée
   */
  static mapRange(
    value: number,
    inMin: number,
    inMax: number,
    outMin: number,
    outMax: number
  ): number {
    return ((value - inMin) * (outMax - outMin)) / (inMax - inMin) + outMin;
  }

  /**
   * Génère un nombre aléatoire entre min et max.
   *
   * @param min - Valeur minimale (incluse)
   * @param max - Valeur maximale (incluse)
   * @returns Nombre aléatoire
   */
  static randomRange(min: number, max: number): number {
    return Phaser.Math.Between(min, max);
  }

  /**
   * Génère un nombre aléatoire flottant entre min et max.
   *
   * @param min - Valeur minimale
   * @param max - Valeur maximale
   * @returns Nombre flottant aléatoire
   */
  static randomFloat(min: number, max: number): number {
    return Phaser.Math.FloatBetween(min, max);
  }

  /**
   * Vérifie si une valeur est dans une plage (avec tolérance).
   *
   * @param value - Valeur à tester
   * @param target - Valeur cible
   * @param tolerance - Tolérance (epsilon)
   * @returns True si la valeur est proche de la cible
   */
  static approximately(value: number, target: number, tolerance: number = 0.01): boolean {
    return Math.abs(value - target) <= tolerance;
  }

  /**
   * Calcule le pourcentage d'une valeur dans une plage.
   *
   * @param value - Valeur actuelle
   * @param min - Minimum de la plage
   * @param max - Maximum de la plage
   * @returns Pourcentage (0-100)
   */
  static percentInRange(value: number, min: number, max: number): number {
    return ((value - min) / (max - min)) * 100;
  }

  /**
   * Applique un smooth damping (pour caméra, mouvements fluides, etc.).
   * Alternative à lerp avec effet de ralentissement plus naturel.
   *
   * @param current - Valeur actuelle
   * @param target - Valeur cible
   * @param velocity - Vitesse actuelle (modifiée par référence)
   * @param smoothTime - Temps de lissage approximatif
   * @param delta - Delta time (secondes)
   * @returns Nouvelle valeur
   */
  static smoothDamp(
    current: number,
    target: number,
    velocity: { value: number },
    smoothTime: number,
    delta: number
  ): number {
    smoothTime = Math.max(0.0001, smoothTime);
    const omega = 2 / smoothTime;
    const x = omega * delta;
    const exp = 1 / (1 + x + 0.48 * x * x + 0.235 * x * x * x);
    let change = current - target;
    const originalTo = target;
    const maxChange = Infinity;
    change = Phaser.Math.Clamp(change, -maxChange, maxChange);
    const temp = (velocity.value + omega * change) * delta;
    velocity.value = (velocity.value - omega * temp) * exp;
    let output = current - change + (change + temp) * exp;

    if ((originalTo - current > 0) === (output > originalTo)) {
      output = originalTo;
      velocity.value = (output - originalTo) / delta;
    }

    return output;
  }

  /**
   * Convertit des degrés en radians.
   * Wrapper de Phaser.Math.DegToRad.
   *
   * @param degrees - Angle en degrés
   * @returns Angle en radians
   */
  static degToRad(degrees: number): number {
    return Phaser.Math.DegToRad(degrees);
  }

  /**
   * Convertit des radians en degrés.
   * Wrapper de Phaser.Math.RadToDeg.
   *
   * @param radians - Angle en radians
   * @returns Angle en degrés
   */
  static radToDeg(radians: number): number {
    return Phaser.Math.RadToDeg(radians);
  }
}
