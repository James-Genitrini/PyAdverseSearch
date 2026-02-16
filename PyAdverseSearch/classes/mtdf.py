# FILE: PyAdverseSearch/classes/mtdf.py

import time
from PyAdverseSearch.classes.algorithm import SearchAlgorithm


class MTDf(SearchAlgorithm):
    """
    MTD(f) - Memory-enhanced Test Driver with node n.
    
    MTD(f) est un algorithme de recherche qui utilise des recherches successives
    avec fenêtre nulle (null-window) pour converger vers la valeur minimax exacte.
    Il est plus efficace qu'Alpha-Beta classique car il explore moins de nœuds,
    mais nécessite une table de transposition pour être performant.
    
    MTD(f) appelle plusieurs fois une recherche alpha-beta avec fenêtre nulle
    (où beta = alpha + 1) pour affiner progressivement la valeur du nœud racine.
    
    Référence: Aske Plaat et al. "MTD(f), a new chess algorithm" (1996)
    """

    def __init__(self, game=None, max_depth=9, max_time_seconds=None, initial_guess=0):
        """
        Initialise l'algorithme MTD(f).
        
        :param game: Instance du jeu
        :param max_depth: Profondeur maximale de recherche
        :param max_time_seconds: Temps maximum de recherche en secondes
        :param initial_guess: Estimation initiale de la valeur (f)
        """
        # Verifying parameters
        if max_depth is not None and (max_depth <= 0 or not isinstance(max_depth, int)):
            print("Error: max_depth must be a positive integer")
            return
        if max_time_seconds is not None and (max_time_seconds <= 0 or not isinstance(max_time_seconds, (int, float))):
            print("Error: max_time_seconds must be a positive number")
            return

        self.game = game
        self.max_depth = max_depth
        self.max_time = max_time_seconds
        self.initial_guess = initial_guess
        self.start_time = None
        
        # MTD(f) nécessite une table de transposition pour être efficace
        self.transposition_table = {}
        
        # Statistiques
        self.nodes_explored = 0
        self.cutoffs = 0
        self.iterations = 0

    def choose_best_move(self, state):
        """
        Sélectionne le meilleur coup en utilisant MTD(f).
        
        :param state: État actuel du jeu
        :return: Le meilleur état enfant trouvé
        """
        self.start_time = time.time()
        self.nodes_explored = 0
        self.cutoffs = 0
        self.iterations = 0
        self.transposition_table.clear()

        is_max = (state.player == "MAX")
        best_move = None
        best_score = self.initial_guess

        # Évaluer chaque coup possible
        moves_scores = []
        for action in state._possible_actions():
            child = state._apply_action(action)
            
            if self.time_limit_reached():
                break

            # Utiliser MTD(f) pour évaluer ce coup
            score = self.mtdf(child, self.max_depth - 1, best_score, not is_max)
            moves_scores.append((child, score))

        # Choisir le meilleur coup
        if not moves_scores:
            return None
            
        if is_max:
            best_move = max(moves_scores, key=lambda x: x[1])[0]
        else:
            best_move = min(moves_scores, key=lambda x: x[1])[0]

        return best_move

    def mtdf(self, state, depth, f, is_max_node):
        """
        Algorithme MTD(f) principal - effectue des recherches successives avec fenêtre nulle.
        
        :param state: État à évaluer
        :param depth: Profondeur de recherche
        :param f: Estimation initiale de la valeur
        :param is_max_node: True si c'est un nœud MAX, False sinon
        :return: Valeur exacte de l'état
        """
        g = f
        upper_bound = float('inf')
        lower_bound = -float('inf')

        while lower_bound < upper_bound:
            self.iterations += 1
            
            if self.time_limit_reached():
                return g

            # Recherche avec fenêtre nulle
            beta = max(g, lower_bound + 1)
            g = self.alpha_beta_with_memory(state, depth, beta - 1, beta, is_max_node)

            if g < beta:
                upper_bound = g
            else:
                lower_bound = g

        return g

    def alpha_beta_with_memory(self, state, depth, alpha, beta, is_max_node):
        """
        Alpha-Beta avec table de transposition (memory).
        
        :param state: État actuel
        :param depth: Profondeur restante
        :param alpha: Borne inférieure
        :param beta: Borne supérieure
        :param is_max_node: True si MAX, False si MIN
        :return: Valeur de l'état
        """
        self.nodes_explored += 1

        # Vérifier la table de transposition
        state_key = self._get_state_key(state)
        if state_key in self.transposition_table:
            cached = self.transposition_table[state_key]
            if cached['depth'] >= depth:
                # Utiliser la valeur en cache si les bornes sont satisfaites
                if cached['lowerbound'] >= beta:
                    return cached['lowerbound']
                if cached['upperbound'] <= alpha:
                    return cached['upperbound']
                alpha = max(alpha, cached['lowerbound'])
                beta = min(beta, cached['upperbound'])

        # État terminal
        if self.game.game_is_terminal(state):
            value = self.game.game_utility(state)
            self._store_transposition(state_key, value, value, depth)
            return value

        # Limite de profondeur
        if depth == 0 or self.time_limit_reached():
            value = self.game.game_heuristic(state)
            self._store_transposition(state_key, value, value, depth)
            return value

        # Recherche alpha-beta
        if is_max_node:
            g = -float('inf')
            a = alpha  # Sauvegarde de la valeur originale d'alpha

            for action in state._possible_actions():
                child = state._apply_action(action)
                g = max(g, self.alpha_beta_with_memory(child, depth - 1, a, beta, False))
                a = max(a, g)
                
                if g >= beta:
                    self.cutoffs += 1
                    break

            # Stocker dans la table de transposition
            if g <= alpha:
                self._store_transposition(state_key, -float('inf'), g, depth)
            elif g >= beta:
                self._store_transposition(state_key, g, float('inf'), depth)
            else:
                self._store_transposition(state_key, g, g, depth)

            return g

        else:  # MIN node
            g = float('inf')
            b = beta  # Sauvegarde de la valeur originale de beta

            for action in state._possible_actions():
                child = state._apply_action(action)
                g = min(g, self.alpha_beta_with_memory(child, depth - 1, alpha, b, True))
                b = min(b, g)
                
                if g <= alpha:
                    self.cutoffs += 1
                    break

            # Stocker dans la table de transposition
            if g <= alpha:
                self._store_transposition(state_key, -float('inf'), g, depth)
            elif g >= beta:
                self._store_transposition(state_key, g, float('inf'), depth)
            else:
                self._store_transposition(state_key, g, g, depth)

            return g

    def _store_transposition(self, key, lowerbound, upperbound, depth):
        """
        Stocke une entrée dans la table de transposition.
        
        :param key: Clé de l'état
        :param lowerbound: Borne inférieure de la valeur
        :param upperbound: Borne supérieure de la valeur
        :param depth: Profondeur à laquelle cette valeur a été calculée
        """
        if key not in self.transposition_table or self.transposition_table[key]['depth'] <= depth:
            self.transposition_table[key] = {
                'lowerbound': lowerbound,
                'upperbound': upperbound,
                'depth': depth
            }

    def _get_state_key(self, state):
        """
        Génère une clé unique pour un état (pour la table de transposition).
        
        :param state: État du jeu
        :return: Clé hashable représentant l'état
        """
        if hasattr(state.board, 'tobytes'):
            # Pour les numpy arrays
            return state.board.tobytes()
        elif isinstance(state.board, (list, tuple)):
            # Pour les listes/tuples, convertir en tuple de tuples si nécessaire
            def make_hashable(obj):
                if isinstance(obj, list):
                    return tuple(make_hashable(item) for item in obj)
                elif isinstance(obj, tuple):
                    return tuple(make_hashable(item) for item in obj)
                else:
                    return obj
            return make_hashable(state.board)
        else:
            # Fallback
            return str(state.board)

    def time_limit_reached(self):
        """Vérifie si la limite de temps est atteinte."""
        if self.max_time is None:
            return False
        return (time.time() - self.start_time) >= self.max_time

    def get_statistics(self):
        """
        Retourne les statistiques de la dernière recherche.
        
        :return: Dictionnaire avec les statistiques
        """
        return {
            'nodes_explored': self.nodes_explored,
            'cutoffs': self.cutoffs,
            'iterations': self.iterations,
            'transposition_table_size': len(self.transposition_table)
        }

    def clear_transposition_table(self):
        """Vide la table de transposition."""
        self.transposition_table.clear()

