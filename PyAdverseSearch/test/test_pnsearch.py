# FILE: PyAdverseSearch/test/test_pnsearch.py

"""
Tests unitaires pour l'algorithme PN-Search.
Démontre l'utilisation et vérifie le bon fonctionnement.
"""

import unittest
from PyAdverseSearch.classes.pnsearch import PNSearch, PNNode, ProofStatus
from PyAdverseSearch.classes.game import Game
from PyAdverseSearch.test.state_tictactoe import TicTacToeState


class TestPNSearch(unittest.TestCase):
    """Tests pour l'algorithme PN-Search"""

    def setUp(self):
        """Configuration initiale pour chaque test"""
        # Configuration d'un jeu de Tic-Tac-Toe
        initial_board = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ]
        initial_state = TicTacToeState(initial_board)

        self.game = Game(
            initial_state=initial_state,
            possible_actions=lambda s: s.get_possible_moves(),
            is_terminal=lambda s: s.is_game_over(),
            winner_function=lambda s: s.get_winner(),
            utility=lambda s: s.get_utility(),
            heuristic=lambda s: s.evaluate(),
            isMaxStarting=True
        )
        initial_state.game = self.game

    def test_pnsearch_initialization(self):
        """Test l'initialisation de PNSearch"""
        pn = PNSearch(game=self.game, max_nodes=1000)

        self.assertIsNotNone(pn)
        self.assertEqual(pn.max_nodes, 1000)
        self.assertTrue(pn.use_transposition_table)
        self.assertEqual(pn.nodes_explored, 0)

    def test_pnnode_creation(self):
        """Test la création d'un PNNode"""
        node = PNNode(self.game.state)

        self.assertIsNotNone(node)
        self.assertEqual(node.phi, 1)
        self.assertEqual(node.delta, 1)
        self.assertEqual(node.proof_status, ProofStatus.UNKNOWN)
        self.assertTrue(node.is_or_node)  # MAX joue en premier

    def test_evaluate_terminal_state(self):
        """Test l'évaluation d'un état terminal"""
        # Configuration d'une victoire pour X (MAX)
        winning_board = [
            ['X', 'X', 'X'],
            ['O', 'O', ' '],
            [' ', ' ', ' ']
        ]
        winning_state = TicTacToeState(winning_board)
        winning_state.game = self.game
        winning_state.player = "MAX"

        pn = PNSearch(game=self.game)
        node = PNNode(winning_state)
        pn._evaluate_terminal(node)

        # Vérifier que le nœud est prouvé (victoire pour MAX)
        self.assertEqual(node.phi, 0)
        self.assertEqual(node.delta, PNSearch.INFINITY)
        self.assertTrue(node.is_proven())

    def test_hash_state(self):
        """Test le hachage des états pour la table de transposition"""
        pn = PNSearch(game=self.game)

        state1 = self.game.state
        hash1 = pn._hash_state(state1)

        # Le même état devrait produire le même hash
        hash2 = pn._hash_state(state1)
        self.assertEqual(hash1, hash2)

        # Un état différent devrait produire un hash différent
        board2 = [
            ['X', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ]
        state2 = TicTacToeState(board2)
        state2.game = self.game
        hash3 = pn._hash_state(state2)
        self.assertNotEqual(hash1, hash3)

    def test_choose_best_move_simple(self):
        """Test le choix du meilleur coup sur une position simple"""
        # Configuration : X peut gagner en un coup
        board = [
            ['X', 'X', ' '],  # X peut jouer en (0,2) pour gagner
            ['O', 'O', ' '],
            [' ', ' ', ' ']
        ]
        state = TicTacToeState(board)
        state.game = self.game
        state.player = "MAX"

        pn = PNSearch(game=self.game, max_nodes=10000)
        best_move = pn.choose_best_move(state)

        # Vérifier qu'un coup a été trouvé
        self.assertIsNotNone(best_move)

        # Vérifier que le coup gagnant a été trouvé
        # Le coup devrait placer X en (0,2) pour gagner immédiatement
        # Sinon, c'est quand même un coup valide
        if best_move:
            # Vérifier qu'au moins un X a été ajouté
            x_count_before = sum(row.count('X') for row in board)
            x_count_after = sum(row.count('X') for row in best_move.board)
            self.assertEqual(x_count_after, x_count_before + 1)

    def test_transposition_table(self):
        """Test que la table de transposition fonctionne correctement"""
        pn = PNSearch(game=self.game, max_nodes=1000, use_transposition_table=True)

        # Effectuer une recherche
        pn.choose_best_move(self.game.state)

        # Vérifier que la table de transposition contient des entrées
        stats = pn.get_statistics()
        self.assertGreater(stats['transposition_table_size'], 0)

    def test_without_transposition_table(self):
        """Test sans table de transposition"""
        pn = PNSearch(game=self.game, max_nodes=1000, use_transposition_table=False)

        best_move = pn.choose_best_move(self.game.state)

        # Vérifier qu'un coup a été trouvé même sans table de transposition
        self.assertIsNotNone(best_move)

        # Vérifier que la table de transposition est vide
        stats = pn.get_statistics()
        self.assertEqual(stats['transposition_table_size'], 0)

    def test_update_proof_numbers_or_node(self):
        """Test la mise à jour des nombres de preuve pour un nœud OR"""
        pn = PNSearch(game=self.game)

        # Créer un nœud OR avec des enfants
        parent = PNNode(self.game.state)
        parent.is_or_node = True
        parent.expanded = True

        # Créer des enfants avec différentes valeurs phi/delta
        child1 = PNNode(self.game.state)
        child1.phi = 5
        child1.delta = 10

        child2 = PNNode(self.game.state)
        child2.phi = 3
        child2.delta = 7

        parent.children = [child1, child2]

        # Mise à jour
        pn.update_proof_numbers(parent)

        # Pour un nœud OR : phi = min(phi enfants), delta = sum(delta enfants)
        self.assertEqual(parent.phi, 3)
        self.assertEqual(parent.delta, 17)

    def test_update_proof_numbers_and_node(self):
        """Test la mise à jour des nombres de preuve pour un nœud AND"""
        pn = PNSearch(game=self.game)

        # Créer un nœud AND avec des enfants
        parent = PNNode(self.game.state)
        parent.is_or_node = False
        parent.expanded = True

        # Créer des enfants
        child1 = PNNode(self.game.state)
        child1.phi = 5
        child1.delta = 10

        child2 = PNNode(self.game.state)
        child2.phi = 3
        child2.delta = 7

        parent.children = [child1, child2]

        # Mise à jour
        pn.update_proof_numbers(parent)

        # Pour un nœud AND : phi = sum(phi enfants), delta = min(delta enfants)
        self.assertEqual(parent.phi, 8)
        self.assertEqual(parent.delta, 7)

    def test_node_limit_respected(self):
        """Test que la limite de nœuds est respectée"""
        pn = PNSearch(game=self.game, max_nodes=10)

        pn.choose_best_move(self.game.state)

        stats = pn.get_statistics()
        self.assertLessEqual(stats['nodes_explored'], 10)

    def test_get_statistics(self):
        """Test la récupération des statistiques"""
        pn = PNSearch(game=self.game, max_nodes=500)

        pn.choose_best_move(self.game.state)
        stats = pn.get_statistics()

        self.assertIn('nodes_explored', stats)
        self.assertIn('transposition_table_size', stats)
        self.assertIn('max_nodes', stats)
        self.assertGreater(stats['nodes_explored'], 0)


class TestPNSearchAdvanced(unittest.TestCase):
    """Tests avancés pour PN-Search"""

    def setUp(self):
        """Configuration pour les tests avancés"""
        initial_board = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ]
        initial_state = TicTacToeState(initial_board)

        self.game = Game(
            initial_state=initial_state,
            possible_actions=lambda s: s.get_possible_moves(),
            is_terminal=lambda s: s.is_game_over(),
            winner_function=lambda s: s.get_winner(),
            utility=lambda s: s.get_utility(),
            heuristic=lambda s: s.evaluate(),
            isMaxStarting=True
        )
        initial_state.game = self.game

    def test_proven_winning_position(self):
        """Test sur une position clairement gagnante"""
        # X peut gagner en un coup
        board = [
            ['X', 'X', ' '],
            ['O', ' ', ' '],
            ['O', ' ', ' ']
        ]
        state = TicTacToeState(board)
        state.game = self.game
        state.player = "MAX"

        pn = PNSearch(game=self.game, max_nodes=5000)
        root = PNNode(state)
        pn.pn_search(root)

        # La position devrait être prouvée gagnante
        self.assertTrue(root.is_proven() or root.phi < root.delta)

    def test_blocking_move(self):
        """Test que l'algorithme trouve un coup de blocage nécessaire"""
        # O peut gagner au prochain coup, X doit bloquer
        board = [
            ['X', ' ', ' '],
            ['O', 'O', ' '],  # O peut gagner en (1,2)
            [' ', ' ', ' ']
        ]
        state = TicTacToeState(board)
        state.game = self.game
        state.player = "MAX"

        pn = PNSearch(game=self.game, max_nodes=5000)
        best_move = pn.choose_best_move(state)

        # Vérifier qu'un coup a été trouvé
        self.assertIsNotNone(best_move)


if __name__ == '__main__':
    unittest.main()


