from PyAdverseSearch.classes.node import Node
import random

class NegamaxSolver:
    """
    Solveur basé sur l'algorithme Negamax avec élagage Alpha-Beta, 
    recherche de quiescence et table de transposition.
    
    Cette variante simplifiée du Minimax repose sur l'égalité : max(a, b) == -min(-a, -b).
    Elle permet de traiter les deux joueurs avec la même logique de maximisation.
    """
    
    def __init__(self, depth_limit=5):
        """
        Initialise le solveur avec une limite de profondeur de recherche.
        
        :param depth_limit: Profondeur maximale de l'arbre de recherche (nombre de demi-coups).
        """
        
        self.depth_limit = depth_limit
        self.transposition_table = {}

        self.nodes_visited = 0
        self.cutoffs = 0

    def get_best_move(self, root_node):
        """
        Analyse la racine du jeu et retourne l'état (board) résultant du meilleur coup possible.
        
        Cette fonction amorce la récursion en explorant les enfants directs de la racine 
        et en sélectionnant celui qui offre le score Negamax le plus élevé.
        
        :param root_node: Instance de Node représentant l'état actuel du jeu.
        :return: Le plateau (board) correspondant au meilleur coup trouvé.
        """
        
        best_value = -float('inf')
        best_action = None
        
        if not root_node.children:
            root_node._expand()
            
        for child in root_node.children:
            # On cherche pour l'adversaire (color = -1)
            # On suppose ici que la racine est toujours pour MAX (color 1)
            value = -self._negamax(child, self.depth_limit - 1, -float('inf'), float('inf'), -1)

            if value > best_value:
                best_value = value
                best_action = child.state.board 
        
        return best_action
    
    
    
    def solve(self, game, state, color):
        """
        Point d'entrée alternatif pour évaluer la valeur d'un état spécifique.
        Réinitialise la table de transposition pour garantir une recherche fraîche.
        
        :param game: Instance de la classe Game.
        :param state: L'état à évaluer.
        :param color: 1 pour le joueur MAX, -1 pour le joueur MIN.
        :return: Valeur numérique de l'état.
        """
        self.transposition_table = {}
        
        if state.game is None:
            state.game = game
            
        root_node = Node(state=state, parent=None, depth=0)
        
        return self._negamax(root_node, self.depth_limit, -float('inf'), float('inf'), color)



    def _get_move_score(self, node, color):
        """
        :param node: Instance de Node à évaluer.
        :param color: Multiplicateur (1 ou -1) selon le joueur actif.
        :return: int/float représentant la priorité du coup.
        """
        
        score = 0

        if node.is_terminal():
            if node.utility * color > 0: return 1000000
            if node.utility == 0: return 0  # Nul
            return -1000000  # Perdant

        score += node.state._evaluate() * color

        return score



    def _negamax(self, node, depth, alpha, beta, color):
        """
        Fonction récursive principale implémentant Negamax avec élagage Alpha-Beta.
        
        :param node: Le nœud (Node) actuellement exploré.
        :param depth: Profondeur restante à explorer.
        :param alpha: Borne inférieure du score sécurisé par le joueur actuel.
        :param beta: Borne supérieure du score que l'adversaire laissera au joueur actuel.
        :param color: Multiplicateur de score (1 ou -1) pour normaliser l'évaluation.
        :return: Le score évalué pour ce nœud du point de vue du joueur actuel.
        """
        
        self.nodes_visited += 1

        state_hash = hash(str(node.state.board)) 
        if state_hash in self.transposition_table:
            entry = self.transposition_table[state_hash]
            if entry['depth'] >= depth:
                return entry['value']

        if node.is_terminal():
            if node.utility > 0:
                adjusted_utility = node.utility + depth
            elif node.utility < 0:
                adjusted_utility = node.utility - depth
            else:
                adjusted_utility = 0

            return color * adjusted_utility

        if depth == 0 or node.is_terminal():
            return self._quiescence(node, alpha, beta, color)

        if not node.children:
            node._expand()

        # random.shuffle(node.children)
        node.children.sort(key=lambda n: self._get_move_score(n, color), reverse=True)

        value = -float('inf')
        for child in node.children:
            score = -self._negamax(child, depth - 1, -beta, -alpha, -color)
            value = max(value, score)
            alpha = max(alpha, value)
            if alpha >= beta:
                self.cutoffs += 1
                break

        self.transposition_table[state_hash] = {'value': value, 'depth': depth}
        return value
    
    
    
    def _quiescence(self, node, alpha, beta, color):
        """
        Recherche de 'calme' pour limiter l'effet d'horizon. 
        Continue d'explorer uniquement les captures pour éviter les erreurs d'évaluation 
        grossières sur le dernier coup.
        
        :param node: Le nœud à évaluer.
        :param alpha/beta: Bornes d'élagage.
        :param color: Direction de l'évaluation.
        :return: Une évaluation stabilisée de la position.
        """
        
        if hasattr(node.state, '_evaluate'):
            stand_pat = color * node.state._evaluate()
        else:
            stand_pat = color * getattr(node.state, 'utility', 0)

        if stand_pat >= beta: 
            return beta
        
        if alpha < stand_pat: 
            alpha = stand_pat

        delta_margin = 10
        if stand_pat < alpha - delta_margin:
            return alpha

        actions = node.state._possible_actions()
        # random.shuffle(actions)
        captures = [a for a in actions if getattr(a, 'is_capture', False)]
        
        for action in captures:
            new_state = node.state._apply_action(action)
            child_node = Node(state=new_state, parent=node, depth=node.depth + 1)
            
            score = -self._quiescence(child_node, -beta, -alpha, -color)
            
            if score >= beta:
                return beta 
            if score > alpha:
                alpha = score
                
        return alpha