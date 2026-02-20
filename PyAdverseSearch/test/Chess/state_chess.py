# FILE: PyAdverseSearch/test/Chess/state_chess.py

from ...classes.state import State
from ...classes.game import Game
from .board import Board

class ChessState(State):
    def __init__(self, board=None, parent=None, game=None):
        """
        Initializes a Chess game state.

        :param board: 8×8 list of lists representing the chess board (default starting position)
        :param player: 'MAX' or 'MIN' meeting the convention that MAX is WHITE and MIN is BLACK
        :param parent: parent state (previous move)
        :param game: reference to the Game instance (attached after init)
        """
        if board is None:
            board = Board()

        # Call to the base State initializer
        super().__init__(board, parent)
        # Ensure essential attributes are set
        self.board = board
        #self.player = player
        self.parent = parent
        self.game = game 

    def _apply_action(self, action):
        """
        Applies the given action ((from_row, from_col), (to_row, to_col)) and returns a new ChessState.
        """
        action_from, action_to, type = action
        if type=='CASTLE':
            new_board = self.board.apply_castling_move(action_from, action_to)
        elif type in ['Q', 'R', 'B', 'N']:
            new_board = self.board.apply_pawn_promotion(action_from, action_to, type)
        else:
            new_board = self.board.apply_move(action_from, action_to)
        #next_player = 'MIN' if self.player == 'MAX' else 'MAX'

        return ChessState(board=new_board, parent=self, game=self.game)

    def display(self):
        GRAY = "\033[90m"
        RESET = "\033[0m"

        print("  +" + "---+" * 8)
        for i in range(8):
            col = 8 - i
            row_pieces = self.board.cases[i*8 : (i+1)*8]
            
            display_row = []
            for piece in row_pieces:
                if piece.color == "BLACK":
                    char = f"{GRAY}{piece.name}{RESET}"
                else:
                    char = piece.name
                
                display_row.append(char)
            
            print(str(col) + " | " + " | ".join(display_row) + " |")
            print("  +" + "---+" * 8)
            
        print("    a   b   c   d   e   f   g   h")

def possible_actions(state):
    """
    Returns a list of available (from_pos, to_pos) moves on the board.
    """
    return state.board.get_all_possible_moves(state.player)


def is_terminal(state):
    """
    Checks if the game has ended (win or full board).
    """
    b = state.board
    

def utility(state):
    """
    Returns 1 if MAX wins, -1 if MIN wins, 0 otherwise.
    """
    b = state.board
    
    return 0


def heuristic(state):
    """
    Returns a heuristic evaluation of the state.
    """
    b = state.board

    WhiteScore=0
    BlackScore=0
        
    # Parsing the board squares from 0 to 63
    for pos1,piece in enumerate(b.cases):

        # Material score
        if(piece.color=='WHITE'):
            WhiteScore+=piece.value
        else:
            # NB : here is for black piece or empty square
            BlackScore+=piece.value

    if(state.player=='MAX'):
        return WhiteScore-BlackScore
    else:
        return BlackScore-WhiteScore


def winner_function(state):
    """
    Returns 'MAX' or 'MIN' if there is a winner, else None.
    """
    b = state.board

    return None                      

def generate_chess_game(isMaxStartingParameter=True):

    """
    Factory: builds a Game configured for Chess.
    """
    initial_state = ChessState()
    game = Game(
        initial_state=initial_state,
        possible_actions=possible_actions,
        is_terminal=is_terminal,
        winner_function=winner_function,
        utility=utility,
        heuristic=heuristic,
        isMaxStarting=isMaxStartingParameter
    )
    initial_state.game = game
    return game
