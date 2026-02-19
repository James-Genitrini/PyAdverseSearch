
import unittest
import time
from PyAdverseSearch.classes.game import Game
from PyAdverseSearch.classes.montecarlo import MonteCarlo
from PyAdverseSearch.classes.minimax import Minimax
from PyAdverseSearch.classes.node import Node
from PyAdverseSearch.test.state_tictactoe import TicTacToeState, generate_tictactoe_game

class TestCriticalComponents(unittest.TestCase):
    
    def setUp(self):
        """Setup a standard TicTacToe game for tests."""
        self.game = generate_tictactoe_game(isMaxStartingParameter=True)
        self.initial_state = self.game.state

    # --- CRITICAL POINT 1: STATE INHERITANCE & INTEGRITY ---
    def test_state_integrity(self):
        """
        Verify that states are correctly linked and independent properly.
        Critical because shared references (shallow copies) ruin tree search.
        """
        print("\n[CRITICAL] Testing State Integrity and Independence...")
        actions = self.initial_state._possible_actions()
        first_child = self.initial_state._apply_action(actions[0])
        
        self.assertIsNotNone(first_child.parent, "Child state must have a reference to parent.")
        self.assertEqual(first_child.parent, self.initial_state, "Child parent must be the creating state.")
        
        self.assertNotEqual(first_child.board, self.initial_state.board, "Child board must be different (moved).")
        self.assertEqual(self.initial_state.board[actions[0][0]][actions[0][1]], ' ', "Parent board should remain empty at move position.")
        
        self.assertIsNotNone(first_child.game, "Child state must keep reference to Game object.")
        self.assertEqual(first_child.game, self.game, "Game reference must be consistent.")

    # --- CRITICAL POINT 2: NODE EXPANSION & GRAPH ---
    def test_node_expansion(self):
        """
        Verify that Node expansion correctly builds the tree layer.
        Critical: If nodes are missing or linked wrong, search fails.
        """
        print("\n[CRITICAL] Testing Tree Node Expansion...")
        root = Node(self.initial_state, depth=0)
        root._expand()
        
        possible_moves = len(self.initial_state._possible_actions())
        self.assertEqual(len(root.children), possible_moves, f"Root should have {possible_moves} children.")
        
        for child in root.children:
            self.assertEqual(child.parent, root, "Child node parent must be root.")
            self.assertEqual(child.depth, 1, "Child depth should be 1.")

    # --- CRITICAL POINT 3: ALGORITHM EXECUTION (MCTS) ---
    def test_mcts_execution(self):
        """
        Verify MCTS runs without crashing and returns a valid valid successor.
        Critical: Ensures the main loop, selection, expansion, and backprop integration works.
        """
        print("\n[CRITICAL] Testing MCTS Execution Cycle...")
        mcts = MonteCarlo(game=self.game, max_iterations=200)
        
        start_time = time.time()
        best_state = mcts.choose_best_move(self.initial_state)
        duration = time.time() - start_time
        
        print(f"MCTS run completed in {duration:.4f}s")
        self.assertIsNotNone(best_state, "MCTS must return a state.")
        self.assertNotEqual(best_state, self.initial_state, "MCTS must make a move (return a child), not the root itself.")
        
        # Verify result is a legal move
        legal_successors = [str(c.board) for c in self.initial_state._generate_successors()]
        self.assertIn(str(best_state.board), legal_successors, "Returned state must be a valid immediate successor.")

    # --- CRITICAL POINT 4: ALGORITHM EXECUTION (MINIMAX) ---
    def test_minimax_execution(self):
        """
        Verify Minimax runs and respects depth limits.
        """
        print("\n[CRITICAL] Testing Minimax Execution...")
        minimax = Minimax(game=self.game, max_depth=2)
        
        best_state = minimax.choose_best_move(self.initial_state)
        self.assertIsNotNone(best_state, "Minimax must return a move.")

    # --- CRITICAL POINT 5: TERMINATION ---
    def test_terminal_detection(self):
        """
        Verify correct detection of terminal states.
        Critical: Loops infinite if terminal states aren't caught.
        """
        print("\n[CRITICAL] Testing Terminal State Logic...")
        board = [
            ['X', 'X', 'X'],
            ['O', 'O', ' '],
            [' ', ' ', ' ']
        ]
        win_state = TicTacToeState(board=board, player='MIN', game=self.game)
        
        self.assertTrue(win_state._is_terminal(), "State should be terminal (MAX Win).")
        self.assertEqual(win_state._utility(), 1000, "Utility should be positive for MAX win.")
    
        self.assertFalse(self.initial_state._is_terminal(), "Initial state is not terminal.")

if __name__ == "__main__":
    unittest.main()
