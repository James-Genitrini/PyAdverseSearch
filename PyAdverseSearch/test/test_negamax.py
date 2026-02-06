import time
from PyAdverseSearch.test.state_tictactoe import generate_tictactoe_game
from PyAdverseSearch.test.state_connect4 import generate_connect4_game

from PyAdverseSearch.classes.negamax import NegamaxSolver
from PyAdverseSearch.classes.node import Node

GAME_CONFIGS = {
    't': {
        'name': 'TIC TAC TOE',
        'generator': generate_tictactoe_game,
        'depth': 9,
        'max_moves': 9
    },
    'c': {
        'name': 'CONNECT 4',
        'generator': generate_connect4_game,
        'depth': 6,
        'max_moves': 42
    }
}



def get_human_move(state):
    successors = state._generate_successors()
    print("\nPossible moves:")
    for idx, move in enumerate(successors):
        print(f"Option {idx + 1}:")
        move.display()
        
    while True:
        try:
            choice = int(input(f"Choose move (1-{len(successors)}): "))
            if 1 <= choice <= len(successors):
                new_state = successors[choice - 1]
                new_state.display()
                return new_state
            print("Invalid choice.")
        except ValueError:
            print("Please enter a numeric value.")
  
  
            
def play_game(game_type):
    config = GAME_CONFIGS.get(game_type)
    if not config:
        print("Invalid selection")
        return

    print(f"\n--- TESTING NEGAMAX AGAINST HUMAN ({config['name']}) ---")
    human_starts = input("Would you like to start (y/n)? ").lower() == 'y'
    
    # Initialisation
    game = config['generator'](not human_starts)
    state = game.state
    solver = NegamaxSolver(depth_limit=config['depth'])
    
    ai_turn = not human_starts

    for move_num in range(1, config['max_moves'] + 1):
        player_label = "AI (MAX)" if ai_turn else "Your (MIN)"
        print(f"\n--- Move {move_num} | {player_label} turn ---")

        if ai_turn:
            start_time = time.time()
            
            root_node = Node(state=state, parent=None, depth=0)
            best_board = solver.get_best_move(root_node)
            
            successors = state._generate_successors()
            state = next((s for s in successors if s.board == best_board), None)
            
            print(f"AI played in {time.time() - start_time:.3f} seconds.")
            if state: state.display()
        else:
            state = get_human_move(state)

        if not state or state._is_terminal():
            break
            
        ai_turn = not ai_turn # Alterne le tour

    # Fin de partie
    print("\n--- GAME OVER ---")
    winner = game.winner_function(state)
    print(f"Result: {'It\'s a draw' if not winner else f'Winner is {winner}'}")


if __name__ == "__main__":
    choice = input("TicTacToe or Connect 4 ? (t or c) : ").lower()
    play_game(choice)