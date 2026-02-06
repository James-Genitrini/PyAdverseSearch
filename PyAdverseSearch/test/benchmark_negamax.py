import time
import statistics
import random

from PyAdverseSearch.test.state_tictactoe import generate_tictactoe_game
from PyAdverseSearch.test.state_connect4 import generate_connect4_game
from PyAdverseSearch.classes.negamax import NegamaxSolver
from PyAdverseSearch.classes.minimax import Minimax
from PyAdverseSearch.classes.node import Node



def play_ai_vs_ai(game, solver):
    state = game.state

    solver.nodes_visited = 0
    solver.cutoffs = 0

    while not state._is_terminal():
        root = Node(state=state, parent=None, depth=0)
        best_board = solver.get_best_move(root)

        successors = state._generate_successors()
        state = next(s for s in successors if s.board == best_board)

    return game.winner_function(state)



def play_negamax_vs_minimax(game, negamax, minimax):
    state = game.state

    negamax.nodes_visited = 0
    negamax.cutoffs = 0

    while not state._is_terminal():
        if state.player == "MAX":
            # Negamax joue
            root = Node(state=state, parent=None, depth=0)
            best_board = negamax.get_best_move(root)

            successors = state._generate_successors()
            state = next(s for s in successors if s.board == best_board)

        else:
            # Minimax joue
            minimax.game = game
            state = minimax.choose_best_move(state)
    # state.display()
    return game.winner_function(state)



def benchmark_negamax_vs_minimax(game_generator, depth, games=20):
    negamax_wins = 0
    minimax_wins = 0
    draws = 0

    times = []
    nodes = []
    cutoffs = []

    for _ in range(games):
        game = game_generator(random.choice([True, False]))

        negamax = NegamaxSolver(depth_limit=depth)
        minimax = Minimax(game=game, max_depth=depth)

        start = time.perf_counter()
        result = play_negamax_vs_minimax(game, negamax, minimax)
        elapsed = time.perf_counter() - start

        times.append(elapsed)
        nodes.append(negamax.nodes_visited)
        cutoffs.append(negamax.cutoffs)

        if result == "MAX":
            negamax_wins += 1
        elif result == "MIN":
            minimax_wins += 1
        else:
            draws += 1


    print("\n=== NEGAMAX vs MINIMAX ===")
    print(f"Games played     : {games}")
    print(f"Negamax wins     : {negamax_wins}")
    print(f"Minimax wins     : {minimax_wins}")
    print(f"Draws            : {draws}")
    print(f"Avg time/game    : {statistics.mean(times):.3f}s")
    print(f"Avg nodes visited: {int(statistics.mean(nodes))}")
    print(f"Avg cutoffs      : {int(statistics.mean(cutoffs))}")



if __name__ == "__main__":
    benchmark_negamax_vs_minimax(
        generate_connect4_game,
        depth=5,
        games=1
    )