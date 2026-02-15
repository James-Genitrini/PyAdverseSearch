# FILE: PyAdverseSearch/test/test_integration_pnsearch.py

"""
Test d'intégration de PN-Search avec le système d'algorithmes existant.
Vérifie la compatibilité avec l'API unifiée.
"""

import unittest
from PyAdverseSearch.classes.algorithm import choose_best_move
from PyAdverseSearch.classes.game import Game
from PyAdverseSearch.test.state_tictactoe import TicTacToeState, generate_tictactoe_game


class TestPNSearchIntegration(unittest.TestCase):
    """Tests d'intégration de PN-Search avec le système existant"""

    def test_integration_via_choose_best_move(self):
        """Test de l'utilisation via choose_best_move (API unifiée)"""
        # Configuration d'une position gagnante
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

        # Utilisation via l'API unifiée
        best_move = choose_best_move(
            'pnsearch',
            game,
            state,
            max_nodes=10000,
            use_transposition_table=True
        )

        # Vérifications
        self.assertIsNotNone(best_move)
        self.assertIsInstance(best_move, TicTacToeState)

    def test_integration_with_factory(self):
        """Test avec la factory generate_tictactoe_game"""
        game = generate_tictactoe_game(isMaxStartingParameter=True)

        # Jouer quelques coups
        game.state = game.state._apply_action((1, 1))  # X au centre
        game.state = game.state._apply_action((0, 0))  # O en haut gauche
        game.state = game.state._apply_action((0, 1))  # X en haut milieu

        # Utiliser PN-Search
        best_move = choose_best_move(
            'pnsearch',
            game,
            game.state,
            max_nodes=5000
        )

        self.assertIsNotNone(best_move)

    def test_comparison_algorithms(self):
        """Compare PN-Search avec Minimax sur la même position"""
        board = [
            ['X', ' ', 'O'],
            [' ', 'X', ' '],
            ['O', ' ', ' ']
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

        # PN-Search
        pn_move = choose_best_move('pnsearch', game, state, max_nodes=10000)

        # Minimax
        minimax_move = choose_best_move('minimax', game, state, max_depth=5)

        # Les deux devraient trouver un coup
        self.assertIsNotNone(pn_move)
        self.assertIsNotNone(minimax_move)

    def test_pnsearch_parameters(self):
        """Test différents paramètres de PN-Search"""
        game = generate_tictactoe_game()

        # Petit nombre de nœuds
        move1 = choose_best_move('pnsearch', game, game.state, max_nodes=50)
        self.assertIsNotNone(move1)

        # Grand nombre de nœuds
        move2 = choose_best_move('pnsearch', game, game.state, max_nodes=50000)
        self.assertIsNotNone(move2)

        # Sans table de transposition
        move3 = choose_best_move(
            'pnsearch',
            game,
            game.state,
            max_nodes=1000,
            use_transposition_table=False
        )
        self.assertIsNotNone(move3)


if __name__ == '__main__':
    unittest.main()

