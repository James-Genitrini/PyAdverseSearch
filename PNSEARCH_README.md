# PN-Search (Proof-Number Search) - Documentation

## Vue d'ensemble

L'algorithme **PN-Search (Proof-Number Search)** est un algorithme de recherche avancé conçu pour résoudre les fins de partie dans les jeux à deux joueurs à somme nulle. Contrairement aux algorithmes classiques comme Minimax ou Alpha-Beta, PN-Search vise à **prouver mathématiquement** qu'une position est gagnante ou perdante.

## Principe de fonctionnement

### Concepts fondamentaux

PN-Search utilise deux valeurs pour chaque nœud de l'arbre de jeu :

1. **phi (φ)** : Le **nombre de preuve** - représente la difficulté de prouver que le nœud est gagnant
2. **delta (δ)** : Le **nombre de réfutation** - représente la difficulté de prouver que le nœud est perdant

### Règles de calcul

Pour un **nœud OR** (joueur MAX) :
- `phi = min(phi des enfants)` - Il suffit qu'UN enfant soit prouvé gagnant
- `delta = sum(delta des enfants)` - TOUS les enfants doivent être réfutés

Pour un **nœud AND** (joueur MIN) :
- `phi = sum(phi des enfants)` - TOUS les enfants doivent être prouvés
- `delta = min(delta des enfants)` - Il suffit qu'UN enfant soit réfuté

### États terminaux

- **Position prouvée gagnante** : `phi = 0`, `delta = ∞`
- **Position prouvée perdante** : `phi = ∞`, `delta = 0`
- **Position non résolue** : `phi > 0` et `delta > 0`

## Architecture de l'implémentation

### Classes principales

#### `PNNode`
Représente un nœud dans l'arbre de recherche PN-Search.

**Attributs :**
- `state` : État du jeu à ce nœud
- `parent` : Nœud parent
- `move` : Coup qui a mené à ce nœud
- `children` : Liste des nœuds enfants
- `phi` : Nombre de preuve
- `delta` : Nombre de réfutation
- `proof_status` : Statut (UNKNOWN, PROVEN, DISPROVEN)
- `is_or_node` : Type de nœud (OR pour MAX, AND pour MIN)

**Méthodes :**
- `is_proven()` : Retourne True si prouvé gagnant
- `is_disproven()` : Retourne True si prouvé perdant
- `is_solved()` : Retourne True si résolu

#### `PNSearch`
Classe principale implémentant l'algorithme PN-Search.

**Paramètres d'initialisation :**
- `game` : Instance de la classe Game (requis)
- `max_nodes` : Limite de nœuds à explorer (défaut : 100000)
- `use_transposition_table` : Active la table de transposition (défaut : True)

**Méthodes principales :**
- `choose_best_move(state)` : Point d'entrée - retourne le meilleur coup
- `pn_search(root)` : Algorithme principal PN-Search
- `evaluate(node)` : Évalue un nœud
- `select_most_proving_node(root)` : Sélectionne le nœud le plus prometteur
- `expand_node(node)` : Étend un nœud
- `update_proof_numbers(node)` : Met à jour phi et delta
- `update_ancestors(node)` : Propage les mises à jour vers la racine
- `get_statistics()` : Retourne les statistiques de recherche

## Optimisations implémentées

### 1. Table de transposition

La **table de transposition** stocke les nœuds déjà évalués pour éviter de recalculer les mêmes positions.

**Fonctionnement :**
- Chaque état est hashé (`_hash_state()`)
- Les nœuds sont stockés dans un dictionnaire avec le hash comme clé
- Lors de l'évaluation, on vérifie d'abord si l'état existe dans la table

**Bénéfices :**
- Réduit considérablement le nombre de nœuds explorés
- Particulièrement efficace pour les jeux avec transpositions (différents chemins vers le même état)

### 2. Détection de cycles

La **détection de cycles** empêche les boucles infinies dans les graphes de jeu.

**Fonctionnement :**
- Maintien d'un ensemble `current_path` contenant les états du chemin actuel
- Avant de descendre dans un enfant, vérification si l'état est déjà dans le chemin
- Si un cycle est détecté, la recherche s'arrête pour cette branche

**Bénéfices :**
- Évite la récursion infinie
- Gère correctement les jeux où des positions peuvent se répéter

### 3. Gestion de la mémoire

**Limite de nœuds :**
- Paramètre `max_nodes` pour contrôler la consommation mémoire
- Arrêt automatique de la recherche si la limite est atteinte

**Gestion de l'overflow :**
- Protection contre les débordements lors des sommes de phi/delta
- Utilisation de `sys.maxsize` comme valeur infinie

## Utilisation

### Exemple basique

```python
from PyAdverseSearch.classes.pnsearch import PNSearch
from PyAdverseSearch.classes.game import Game
from PyAdverseSearch.test.state_tictactoe import TicTacToeState

# Configuration du jeu
board = [
    ['X', 'X', ' '],
    ['O', 'O', ' '],
    [' ', ' ', ' ']
]
state = TicTacToeState(board)

game = Game(
    initial_state=state,
    possible_actions=lambda s: s.get_possible_moves(),
    is_terminal=lambda s: s.is_game_over(),
    winner_function=lambda s: s.get_winner(),
    utility=lambda s: s.get_utility(),
    heuristic=lambda s: s.evaluate(),
    isMaxStarting=True
)
state.game = game
state.player = "MAX"

# Création et utilisation de PN-Search
pn = PNSearch(game=game, max_nodes=10000)
best_move = pn.choose_best_move(state)

# Affichage des statistiques
stats = pn.get_statistics()
print(f"Nœuds explorés : {stats['nodes_explored']}")
```

### Utilisation avec le système d'algorithmes

```python
from PyAdverseSearch.classes.algorithm import choose_best_move

# Utilisation via le système unifié
best_move = choose_best_move(
    'pnsearch', 
    game, 
    state,
    max_nodes=50000,
    use_transposition_table=True
)
```

## Comparaison avec d'autres algorithmes

| Caractéristique | PN-Search | Minimax | Alpha-Beta | Monte Carlo |
|-----------------|-----------|---------|------------|-------------|
| Type de preuve | Mathématique | Heuristique | Heuristique | Statistique |
| Complétude | Oui (si mémoire suffisante) | Oui | Oui | Non |
| Optimalité | Oui | Oui | Oui | Approximative |
| Gestion mémoire | Table de transposition | N/A | N/A | Arbre UCT |
| Meilleur usage | Fins de partie | Jeux généraux | Jeux généraux | Grands espaces |

## Cas d'usage recommandés

### Idéal pour :
- ✅ Résolution de fins de partie
- ✅ Puzzles et problèmes de décision
- ✅ Vérification de positions tactiques
- ✅ Jeux avec beaucoup de transpositions

### Moins adapté pour :
- ❌ Positions d'ouverture (trop de possibilités)
- ❌ Jeux avec des plateaux très larges
- ❌ Recherche en temps limité stricte

## Complexité

- **Temps** : O(b^d) dans le pire cas, mais souvent bien meilleur grâce aux optimisations
- **Espace** : O(n) où n est le nombre de nœuds stockés (limité par `max_nodes`)

Avec la table de transposition, la complexité pratique est souvent réduite de manière significative.

## Améliorations futures possibles

1. **PN² (Proof-Number Search with Threshold)** : Variante avec seuils dynamiques
2. **df-pn (Depth-First PN-Search)** : Version utilisant moins de mémoire
3. **Heuristiques pour phi/delta** : Initialisation plus intelligente
4. **Parallélisation** : Exploration parallèle de différentes branches
5. **Apprentissage** : Utilisation de l'historique pour améliorer la sélection

## Références

- Allis, L. V. (1994). *Searching for Solutions in Games and Artificial Intelligence*. PhD thesis, Rijksuniversiteit Limburg.
- Kishimoto, A., & Müller, M. (2005). *Search versus knowledge for solving life and death problems in Go*. AAAI.
- Pawlewicz, J., & Hayward, R. B. (2013). *Scalable parallel DFPN search*. Computers and Games.

## License

Ce code est fourni à des fins éducatives dans le cadre du projet PyAdverseSearch.

