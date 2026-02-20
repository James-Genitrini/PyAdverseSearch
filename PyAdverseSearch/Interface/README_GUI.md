# Interface Graphique Puissance 4 - Guide d'Utilisation

## Lancement de l'Interface

Pour lancer l'interface graphique amelioree:

```bash
python -m PyAdverseSearch.Interface.connect4_gui_enhanced
```

## Caracteristiques

### Mode de Selection d'Algorithme

L'interface propose maintenant **7 options d'algorithme**:

#### 1. Auto (Selection Intelligente) - RECOMMANDE

Le mode **Auto** selectionne automatiquement le meilleur algorithme en fonction de la situation du jeu:

- **Debut de partie** (< 30% rempli): **MTD(f)**
  - Le plus efficace pour explorer l'arbre complet
  - Utilise des fenetres nulles iteratives
  - Converge rapidement vers la solution optimale

- **Milieu de partie** (30-70% rempli):
  - Si peu d'actions possibles (≤ 4): **Alpha-Beta + Table de Transposition**
  - Sinon: **MTD(f)** pour efficacite maximale

- **Fin de partie** (> 70% rempli ou < 10 cases vides):
  - Si ≤ 8 cases vides: **PN-Search**
    - Prouve mathematiquement la victoire/defaite
    - Exploration selective
  - Sinon: **Alpha-Beta + Table de Transposition**

L'algorithme change dynamiquement a chaque coup pour optimiser la performance.

#### 2. Minimax (Classique)

Algorithme de base sans optimisation:
- Explore tous les noeuds de l'arbre
- Garantit la solution optimale
- Plus lent que les autres
- Utile pour comprendre les bases

**Utilisation**: Difficulte Facile ou pour comparaison pedagogique

#### 3. Alpha-Beta (Elagage)

Amelioration de Minimax avec elagage:
- Elimine les branches inutiles
- 10x a 30x plus rapide que Minimax
- Meme resultat garanti
- Avec table de transposition

**Utilisation**: Bon compromis performance/simplicite

#### 4. MTD(f) (Plus Efficace)

Algorithme le plus efficace pour recherche complete:
- Utilise des recherches avec fenetre nulle
- Converge vers la valeur minimax exacte
- Table de transposition obligatoire
- 30x a 50x plus rapide que Minimax

**Utilisation**: Pour maximiser la profondeur de recherche

#### 5. Negamax (Simplifie)

Variante simplifiee de Minimax:
- Meme logique pour les deux joueurs
- Code plus concis
- Performance similaire a Alpha-Beta
- Avec elagage et table de transposition

**Utilisation**: Alternative a Alpha-Beta

#### 6. Monte Carlo (Simulations)

Approche par simulations aleatoires:
- Ne garantit pas l'optimal
- Bon pour des arbres tres larges
- Performance depend du nombre de simulations
- Peut trouver des coups surprenants

**Utilisation**: Difficulte Facile/Moyen, ou pour variete de jeu

#### 7. PN-Search (Preuve)

Algorithme de preuve mathematique:
- Prouve qu'une position est gagnante/perdante
- Exploration selective (phi/delta)
- Ideal pour fins de partie
- Peut etre lent sur positions complexes

**Utilisation**: Fin de partie ou analyse de positions critiques

---

## Niveaux de Difficulte

### Facile (Profondeur 3)
- L'IA regarde 3 coups a l'avance
- Temps de reflexion: < 1 seconde
- Fait des erreurs tactiques
- Bon pour debutants

### Moyen (Profondeur 5)
- L'IA regarde 5 coups a l'avance
- Temps de reflexion: 1-3 secondes
- Jeu tactique solide
- Niveau intermediaire

### Difficile (Profondeur 7)
- L'IA regarde 7 coups a l'avance
- Temps de reflexion: 3-10 secondes
- Jeu strategique avance
- Difficile a battre

### Expert (Profondeur 9)
- L'IA regarde 9 coups a l'avance
- Temps de reflexion: 10-30 secondes
- Jeu quasi-parfait
- Extremement difficile

---

## Informations Affichees

### Pendant le Jeu

1. **Label principal**: Indique le joueur actif
2. **Algo**: Affiche l'algorithme en cours d'utilisation
3. **Temps IA**: Temps de calcul du dernier coup
4. **Barre de progression**: Progression du calcul IA
5. **Statistiques**: Details selon l'algorithme
   - **Minimax/Alpha-Beta/MTD(f)**: Noeuds explores, coupures
   - **Monte Carlo**: Nombre de simulations
   - **PN-Search**: Noeuds explores, taille table de transposition
   - **Negamax**: Noeuds visites, coupures
6. **Historique**: Derniers coups joues

### Statistiques par Algorithme

#### Alpha-Beta / MTD(f)
```
[MTD(f)] 12,450 noeuds explores, 8,234 coupures en 2.34s
```
- Noeuds explores: Positions evaluees
- Coupures: Branches elaguees (plus il y en a, mieux c'est)

#### Monte Carlo
```
[Monte Carlo] 10,000 simulations en 1.52s (6,578/s)
```
- Simulations: Parties aleatoires jouees
- /s: Taux de simulation

#### PN-Search
```
[PN-Search] 3,421 noeuds explores, TT: 2,156 entrees en 0.89s
```
- TT: Table de transposition (cache)

#### Negamax
```
[Negamax] 15,678 noeuds visites, 9,012 coupures en 1.98s
```

---

## Conseils d'Utilisation

### Pour Apprendre
- Commencer en mode **Facile** avec **Minimax**
- Observer les statistiques de chaque algorithme
- Comparer **Minimax** vs **Alpha-Beta** pour voir l'elagage
- Comparer **Alpha-Beta** vs **MTD(f)** pour voir l'efficacite

### Pour Jouer Serieusement
- Utiliser le mode **Auto**
- Difficulte **Moyen** ou **Difficile**
- Observer comment l'algorithme change pendant la partie

### Pour Tester les Algorithmes
- Utiliser **Moyen** ou **Difficile**
- Tester chaque algorithme sur la meme position
- Comparer temps et qualite des coups

### Pour la Performance Maximale
- Mode **Auto** ou **MTD(f)**
- Difficulte **Expert**
- Patience requise (calculs longs)

---

## Comparaison de Performance

Sur une position typique de milieu de partie (profondeur 7):

| Algorithme | Temps | Noeuds | Efficacite |
|------------|-------|--------|------------|
| Minimax | ~25s | 850,000 | Baseline |
| Alpha-Beta | ~3s | 95,000 | 8x |
| MTD(f) | ~1.5s | 48,000 | 17x |
| Negamax | ~3.2s | 102,000 | 8x |
| Monte Carlo* | ~2s | 20,000 sim | Variable |
| PN-Search** | Variable | Variable | Selectif |

*Monte Carlo: 10,000 iterations
**PN-Search: Optimise pour fin de partie

---

## Mode Auto - Logique Detaillee

Le mode Auto analyse:

1. **Taux de remplissage du plateau**
   - Compte les cases vides
   - Calcule le pourcentage rempli

2. **Nombre d'actions possibles**
   - Colonnes encore jouables
   - Complexite de l'arbre

3. **Selection de l'algorithme**
   ```
   Si < 30% rempli:
       -> MTD(f) (efficace sur grand arbre)
   
   Si > 70% rempli OU < 10 cases vides:
       Si <= 8 cases vides:
           -> PN-Search (prouver la victoire)
       Sinon:
           -> Alpha-Beta+TT (solide)
   
   Sinon (milieu de partie):
       Si <= 4 actions possibles:
           -> Alpha-Beta+TT (arbre etroit)
       Sinon:
           -> MTD(f) (arbre large)
   ```

Cette logique optimise le temps de calcul tout en maintenant la qualite de jeu.

---

## Touches et Interactions

- **Clic sur une colonne**: Jouer un pion (si votre tour)
- **Survol souris**: Colonne surbrillonnee en vert
- **Bouton "Nouvelle Partie"**: Recommencer
- **Bouton "Quitter"**: Fermer l'application

---

## Troubleshooting

### L'IA est trop lente
- Reduire la difficulte
- Utiliser **Alpha-Beta** ou **MTD(f)** au lieu de **Minimax**
- Eviter **PN-Search** en milieu de partie

### L'IA fait des erreurs
- Augmenter la difficulte
- Utiliser mode **Auto** ou **MTD(f)**
- Eviter **Monte Carlo** en difficulte Facile

### Erreur "L'IA n'a pas trouve de coup valide"
- Relancer la partie
- Changer d'algorithme
- Verifier que le jeu n'est pas bloque

### Interface ne repond pas
- L'IA calcule (attendre)
- Si > 1 minute: fermer et relancer
- Reduire la profondeur

---

## Developpement et Extension

### Fichiers Concernes
- `connect4_gui_enhanced.py`: Interface graphique
- `state_connect4.py`: Logique du jeu
- `classes/*.py`: Algorithmes

### Ajouter un Nouvel Algorithme

1. Implementer la classe avec methode `choose_best_move(state)`
2. Ajouter l'import dans l'interface
3. Ajouter l'option dans `create_config_screen()`
4. Ajouter le cas dans `start_game()`
5. Gerer les statistiques dans `finish_ai_move()`

### Modifier la Selection Auto

Editer la methode `select_best_algorithm()` dans `connect4_gui_enhanced.py`

---

## Credits

PyAdverseSearch - Bibliotheque d'algorithmes de recherche adversariale
Benjamin Bouquet - Promotion 2026

Algorithmes implementes:
- Minimax: Algorithme classique
- Alpha-Beta: Knuth & Moore (1975)
- MTD(f): Plaat et al. (1996)
- Negamax: Variante de Minimax
- Monte Carlo: Approach stochastique
- PN-Search: Allis (1994)

