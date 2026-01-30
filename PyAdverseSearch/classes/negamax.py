class NegamaxSolver:
    def __init__(self, depth_limit=5):
        self.depth_limit = depth_limit
        self.transposition_table = {}
        self.nodes_visited = 0

    def solve(self, game, state, color):
        self.transposition_table = {}
        self.nodes_visited = 0
        return self._negamax(game, state, self.depth_limit, -float('inf'), float('inf'), color)

    def _negamax(self, game, state, depth, alpha, beta, color):
        self.nodes_visited += 1
        
        state_key = state.get_hash()
        if state_key in self.transposition_table:
            entry = self.transposition_table[state_key]
            if entry['depth'] >= depth:
                return entry['value']

        # 2. Cas terminaux
        if game.game_is_terminal(state):
            return color * game.game_utility(state)

        if depth == 0:
            return self._quiescence(game, state, alpha, beta, color)

        value = -float('inf')
        
        # 3. Exploration
        for action in game.game_possible_actions(state):
            next_state = state.apply_action(action)
            score = -self._negamax(game, next_state, depth - 1, -beta, -alpha, -color)
            
            value = max(value, score)
            alpha = max(alpha, value)
            
            if alpha >= beta:
                break

        # 4. Sauvegarde
        self.transposition_table[state_key] = {
            'value': value,
            'depth': depth
        }
        return value

    def _quiescence(self, game, state, alpha, beta, color):
        """Recherche calme pour éviter l'effet d'horizon."""
        stand_pat = color * game.game_heuristic(state)

        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        # Filtre optionnel : ne tester que les actions "bruyantes" (captures)
        actions = game.game_possible_actions(state)
        captures = [a for a in actions if getattr(a, 'is_capture', False)]

        for action in captures:
            next_state = state.apply_action(action)
            score = -self._quiescence(game, next_state, -beta, -alpha, -color)
            
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        
        return alpha