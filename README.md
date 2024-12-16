# Candy Game 

## Description

Le **Candy Game ** est un jeu  où des enfants agents interagissent dans un environnement simulé. Chaque enfant suit une stratégie unique pour collecter des bonbons tout en évitant la maîtresse. Deux versions sont disponibles :

1. **Version sans potion magique** : située dans la branche `Malik.2.0`.
2. **Version avec potion magique(environnement Dynamique )** : située dans la branche `Hadil`.

## Fonctionnalités principales

- **Stratégies des enfants** : Chaque enfant dispose d'une stratégie différente pour collecter les bonbons :
  - Aller directement (DirectToCandy).
  - Attendre et aller (WaitAndGo).
  - Détourner la maîtresse (DistractorKid).
  - Suivre le chemin le plus long (LongestPath).
  -Parcours en largeur (BFS) : L'enfant utilise un algorithme de parcours en largeur pour trouver le chemin optimal jusqu'à un bonbon.

- **Stratégie de la maîtresse** :
  - La maîtresse cible les enfants qui sont hors de la **zone de coloriage**.
  - Elle identifie et poursuit l'enfant le plus proche en fonction de la distance manhattan.
  - Si elle intercepte un enfant :
    - Si l'enfant porte un bonbon, elle le confisque et remet le bonbon dans la zone des bonbons.
    - L'enfant intercepté est renvoyé à sa position initiale.
    - Si un enfant est intercepté trop souvent, il est **puni**.

- **Potion magique** :
  - Les enfants peuvent utiliser une **potion magique** qui les rend invisibles à la maîtresse pour une durée limitée.
  - Pendant cet état d'invisibilité, les enfants peuvent se déplacer librement sans risque d'interception.
  - La durée d'invisibilité est définie dans `kid.py` :
    ```python
    INVISIBILITY_DURATION = 10000  # Durée de l'invisibilité en millisecondes
    ```
  - Une fois l'effet terminé, l'enfant redevient visible et peut être intercepté.

--

## Instructions d'exécution

### Version `Malik.2.0` (sans potion magique)

1. **Configuration** :
   - Lancer le script principal `main.py`.
   - À l'exécution, vous serez invité à entrer le **nombre de bonbons** via la console.

2. **Exécution** :
   - Naviguez dans la branche `Malik.2.0` :
     ```bash
     git checkout Malik.2.0
     ```
   - Exécutez le fichier principal :
     ```bash
     python main.py
     ```

---

### Version `Hadil` (avec potion magique)

1. **Configuration** :
   - Dans le fichier `game.py`, ajustez les variables suivantes selon vos besoins :
     - **Nombre de bonbons** :
       ```python
       CANDY_COUNT = 10  # Modifier ce nombre
       ```
     - **Durée du jeu** :
       ```python
       GAME_DURATION = 60  # Temps limite en secondes
       ```

   - Dans le fichier `kid.py`, personnalisez les constantes suivantes pour modifier le comportement des enfants :
     - Délai entre les actions :
       ```python
       DEFAULT_TICK_DELAY = 10
       ```
     - Durée de punition :
       ```python
       PUNISHMENT_DURATION = 5000  # En millisecondes
       ```
     - Durée d'invisibilité (si applicable) :
       ```python
       INVISIBILITY_DURATION = 10000
       ```

2. **Exécution** :
   - Naviguez dans la branche `Hadil` :
     ```bash
     git checkout Hadil
     ```
   - Exécutez le fichier principal :
     ```bash
     python main.py
     ```

---

## Structure du projet

```
.
├── src/
│   ├── agents/
│   │   ├── strategies/
│   │   │   ├── direct_to_candy.py  # Stratégie DirectToCandy
│   │   │   ├── waitAndGo.py        # Stratégie WaitAndGo
│   │   │   ├── DistractorKid.py    # Stratégie DistractorKid
│   │   │   ├── longestPath.py      # Stratégie LongestPath
│   │   └── teacher.py              # Classe Maîtresse
│   ├── environment.py              # Définition de l'environnement
│   ├── game.py                     # Logique principale du jeu
│   └── kid.py                      # Base des enfants
├── main.py                         # Script principal
└── assets/                         # Ressources graphiques
```

---


- **Comportement des enfants et maîtresse** :
  - Délai de mouvement et stratégies spécifiques dans `kid.py` et `teacher.py`.
