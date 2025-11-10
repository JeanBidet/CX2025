# Guide d'Installation - CycloCross 2025

Ce document explique comment installer et configurer l'environnement de développement pour le jeu CycloCross 2025.

## Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation sur Windows

### Option 1 : Installation via wheel pré-compilée (Recommandé)

1. **Téléchargez la wheel pygame pour votre version de Python**

   Visitez : https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame

   Ou utilisez pip avec l'option `--only-binary` :
   ```bash
   pip install pygame --only-binary :all:
   ```

2. **Installez les dépendances**
   ```bash
   cd CycloCross2025
   pip install -r requirements.txt
   ```

### Option 2 : Installation depuis PyPI (version stable)

Si la compilation échoue, essayez une version stable :

```bash
pip install pygame-ce
# ou
pip install pygame==2.5.2
```

### Option 3 : Utilisation d'un environnement virtuel (Recommandé)

1. **Créez un environnement virtuel**
   ```bash
   python -m venv venv
   ```

2. **Activez l'environnement**
   - Windows CMD:
     ```bash
     venv\Scripts\activate.bat
     ```
   - Windows PowerShell:
     ```bash
     venv\Scripts\Activate.ps1
     ```

3. **Installez pygame et les dépendances**
   ```bash
   pip install pygame
   pip install -r requirements.txt
   ```

## Installation sur Linux/macOS

```bash
# Créer et activer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## Vérification de l'installation

Pour vérifier que pygame est correctement installé :

```bash
python -c "import pygame; print(pygame.ver)"
```

Si cela affiche la version de pygame, l'installation est réussie !

## Lancement du jeu

```bash
python main.py
```

## Contrôles du jeu

### Navigation entre scènes (touches de fonction)
- **F1** : Scène de test Terrain
- **F2** : Scène de test State Pattern
- **F3** : Toggle debug info
- **F4** : Scène de test Stamina/Balance (Prompt 6)
- **F11** : Toggle fullscreen
- **P** : Pause
- **ESC** : Quitter

### Contrôles du cycliste (dans la scène Stamina/Balance)
- **Flèches directionnelles** : Déplacement
- **C** : Porter/Remonter sur le vélo
- **T** : Changer de type de terrain
- **S** : Augmenter la pente (+10°)
- **D** : Diminuer la pente (-10°)
- **B** : Appliquer un déséquilibre (test)
- **F** : Drainer l'endurance (test)
- **R** : Reset endurance et équilibre

## Résolution des problèmes

### Erreur "ModuleNotFoundError: No module named 'pygame'"

- Assurez-vous que pygame est installé : `pip list | grep pygame`
- Réinstallez pygame : `pip install --force-reinstall pygame`

### Erreur de compilation pygame sur Windows

- Utilisez une wheel pré-compilée (voir Option 1)
- Ou installez pygame-ce : `pip install pygame-ce`

### Le jeu ne se lance pas

- Vérifiez que vous êtes dans le bon répertoire
- Vérifiez que l'environnement virtuel est activé (si vous en utilisez un)
- Consultez les logs d'erreur dans la console

## Structure du projet

```
CycloCross2025/
├── main.py                 # Point d'entrée du jeu
├── config/                 # Configuration et constantes
├── entities/              # Entités du jeu (Cyclist, etc.)
├── components/            # Composants ECS
│   ├── stamina_component.py      # Nouveau : Gestion de l'endurance
│   └── balance_component.py      # Nouveau : Gestion de l'équilibre
├── systems/               # Systèmes et managers
├── scenes/                # Scènes du jeu
│   └── stamina_balance_test_scene.py  # Nouveau : Test stamina/balance
├── ui/                    # Nouveau : Interface utilisateur
│   ├── gauge_widget.py           # Widgets de jauges
│   └── stamina_balance_ui.py     # UI stamina/balance
├── patterns/              # Design patterns
├── utils/                 # Utilitaires
└── requirements.txt       # Dépendances Python
```

## Développement

### Type checking avec mypy

```bash
pip install mypy
mypy --strict main.py
```

### Formatage du code

```bash
pip install black
black .
```

## Contact et Support

Pour toute question ou problème, consultez la documentation du projet ou créez une issue.

---

**Version**: Prompt 6 - Système d'Endurance et d'Équilibre
**Date**: 2025-11-10
