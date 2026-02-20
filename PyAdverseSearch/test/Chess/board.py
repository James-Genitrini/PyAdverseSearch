# FILE: PyAdverseSearch/test/Chess/board.py

from .piece import Piece 


coord=[
    'a8','b8','c8','d8','e8','f8','g8','h8',
    'a7','b7','c7','d7','e7','f7','g7','h7',
    'a6','b6','c6','d6','e6','f6','g6','h6',
    'a5','b5','c5','d5','e5','f5','g5','h5',
    'a4','b4','c4','d4','e4','f4','g4','h4',
    'a3','b3','c3','d3','e3','f3','g3','h3',
    'a2','b2','c2','d2','e2','f2','g2','h2',
    'a1','b1','c1','d1','e1','f1','g1','h1',
    ]


class Board:
    def __init__(self, cases=None):
        """
        Initializes the chess board.

        :param board: 8×8 list of lists representing the chess board (default starting position)
        """
        if cases is None:
            self.cases = [
                Piece('R','BLACK'), Piece('N','BLACK'), Piece('B','BLACK'), Piece('Q','BLACK'),
                Piece('K','BLACK'), Piece('B','BLACK'), Piece('N','BLACK'), Piece('R','BLACK'),

                Piece('P','BLACK'), Piece('P','BLACK'), Piece('P','BLACK'), Piece('P','BLACK'),
                Piece('P','BLACK'), Piece('P','BLACK'), Piece('P','BLACK'), Piece('P','BLACK'),

                Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'),
                Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'),

                Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'),
                Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'),

                Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'),
                Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'),

                Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'),
                Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'), Piece(' ','NONE'),

                Piece('P','WHITE'), Piece('P','WHITE'), Piece('P','WHITE'), Piece('P','WHITE'),
                Piece('P','WHITE'), Piece('P','WHITE'), Piece('P','WHITE'), Piece('P','WHITE'),

                Piece('R','WHITE'), Piece('N','WHITE'), Piece('B','WHITE'), Piece('Q','WHITE'),
                Piece('K','WHITE'), Piece('B','WHITE'), Piece('N','WHITE'), Piece('R','WHITE')
            ]
        else:
            self.cases = cases

        self.white_can_castle_56=True
        self.white_can_castle_63=True
        self.black_can_castle_0=True
        self.black_can_castle_7=True 

    def move_piece(self, from_pos, to_pos):
        """
        Moves a piece from from_pos to to_pos.

        :param from_pos: Tuple (row, col) of the piece to move.
        :param to_pos: Tuple (row, col) of the destination.
        """
        piece = self.cases[coord.index(from_pos)]
        
        
        if (self.can_move(piece, from_pos, to_pos)):
            self.cases[coord.index(to_pos)] = piece
            self.cases[coord.index(from_pos)] = Piece(' ','NONE')
            
            if (from_pos == 'e1'):
                self.white_can_castle_56=False
                self.white_can_castle_63=False
            elif (from_pos == 'h1'):
                self.white_can_castle_63=False
            elif (from_pos == 'a1'):
                self.white_can_castle_56=False
            elif (from_pos == 'e8'):
                self.black_can_castle_0=False
                self.black_can_castle_7=False
            elif (from_pos == 'h8'):
                self.black_can_castle_7=False
            elif (from_pos == 'a8'):
                self.black_can_castle_0=False
        elif (piece.name == 'K' and self.can_castle(piece, from_pos, to_pos)):
            match to_pos:
                case 'c1':
                    self.cases[coord.index('c1')] = piece
                    self.cases[coord.index('e1')] = Piece(' ','NONE')
                    self.cases[coord.index('a1')] = Piece(' ','NONE')
                    self.cases[coord.index('d1')] = Piece('R','WHITE')
                    self.white_can_castle_56=False
                    self.white_can_castle_63=False
                case'g1':
                    self.cases[coord.index('g1')] = piece
                    self.cases[coord.index('e1')] = Piece(' ','NONE')
                    self.cases[coord.index('h1')] = Piece(' ','NONE')
                    self.cases[coord.index('f1')] = Piece('R','WHITE')
                    self.white_can_castle_56=False
                    self.white_can_castle_63=False
                case 'c8':
                    self.cases[coord.index('c8')] = piece
                    self.cases[coord.index('e8')] = Piece(' ','NONE')
                    self.cases[coord.index('a8')] = Piece(' ','NONE')
                    self.cases[coord.index('d8')] = Piece('R','BLACK')
                    self.black_can_castle_0=False
                    self.black_can_castle_7=False
                case 'g8':
                    self.cases[coord.index('g8')] = piece
                    self.cases[coord.index('e8')] = Piece(' ','NONE')
                    self.cases[coord.index('h8')] = Piece(' ','NONE')
                    self.cases[coord.index('f8')] = Piece('R','BLACK')
                    self.black_can_castle_0=False
                    self.black_can_castle_7=False

    def can_move(self, piece, from_pos, to_pos):
        """
        Checks if a piece can move from from_pos to to_pos.

        :param from_pos: Tuple (row, col) of the piece to move.
        :param to_pos: Tuple (row, col) of the destination.
        :return: True if the move is valid, False otherwise.
        """

        piece = self.cases[coord.index(from_pos)]
        piece_name = piece.name
        from_pos_index = coord.index(from_pos)
        to_pos_index = coord.index(to_pos)
        possible_moves = []

        print(f"Checking if {piece_name} can move from {from_pos} to {to_pos}")
        match piece_name:
            case 'P':
                possible_moves = piece.pawn_possible_moves(from_pos_index, self)
                #pawn_can_move(piece, movement, target_piece)
            case 'R':
                possible_moves = piece.rook_possible_moves(from_pos_index, self)
                #return rook_can_move(self, piece, from_pos, to_pos)
            case 'N':
                possible_moves = piece.knight_possible_moves(from_pos_index, self)
            case 'B':
                possible_moves = piece.bishop_possible_moves(from_pos_index, self)
            case 'Q':
                possible_moves = piece.queen_possible_moves(from_pos_index, self)
            case 'K':
                possible_moves = piece.king_possible_moves(from_pos_index, self)

        if to_pos_index in possible_moves:
            return True
        else:
            return False
    
    def promote_pawn(self, from_pos, to_pos, promotion_piece):
        """
        Promotes a pawn to a queen when it reaches the opposite end of the board.

        :param from_pos: The position of the pawn to promote.
        :param to_pos: The position where the pawn is being promoted.
        :param promotion_piece: The piece to promote to (e.g., 'Q' for queen).
        """
        piece = self.cases[coord.index(from_pos)]
        if not promotion_piece in ['Q', 'R', 'B', 'N']:
            raise ValueError("Invalid promotion piece")
        if self.can_promote(piece, from_pos, to_pos) and piece.name == 'P' and ((piece.color == 'WHITE' and to_pos[1] == '8') or (piece.color == 'BLACK' and to_pos[1] == '1')):
            self.cases[coord.index(to_pos)] = Piece(promotion_piece, piece.color)
            self.cases[coord.index(from_pos)] = Piece(' ','NONE')

    def can_promote(self, piece, from_pos, to_pos):
        """
        Checks if a pawn can be promoted.

        :param piece: The pawn piece to check.
        :param to_pos: The position where the pawn is being promoted.
        :return: True if the pawn can be promoted, False otherwise.
        """
        from_pos_index = coord.index(from_pos)
        to_pos_index = coord.index(to_pos)
        possible_promotions = []

        possible_promotions = piece.pawn_possible_promotions(from_pos_index, self)
        if piece.name == 'P' and to_pos_index in possible_promotions:
            return True
        return False

    def can_castle(self, piece, from_pos, to_pos):
        """
        Checks if castling is possible between the king and rook.

        :param from_pos: Tuple (row, col) of the piece to move.
        :param to_pos: Tuple (row, col) of the destination.
        :return: True if castling is possible, False otherwise.
        """
        from_pos_index = coord.index(from_pos)
        to_pos_index = coord.index(to_pos)
        possible_castling_moves = []
        possible_castling_moves = piece.king_possible_castling_moves(from_pos_index, self)
        if piece.name == 'K' and to_pos_index in possible_castling_moves:
            return True
        return False

    def get_all_possible_moves(self, color):
        """
        Returns a list of all possible moves for a given color.

        :param color: The color of the pieces to get moves for ('WHITE' or 'BLACK').
        :return: A list of possible moves for the specified color.
        """
        all_possible_moves = []
        for index, piece in enumerate(self.cases):
            if piece.color == color:
                from_pos = coord[index]
                possible_moves = []
                possible_promotions = []
                possible_castling_moves = []
                
                match piece.name:
                    case 'P':
                        possible_moves = piece.pawn_possible_moves(index, self) 
                        possible_promotions = piece.pawn_possible_promotions(index, self)
                    case 'R':
                        possible_moves = piece.rook_possible_moves(index, self)
                    case 'N':
                        possible_moves = piece.knight_possible_moves(index, self)
                    case 'B':
                        possible_moves = piece.bishop_possible_moves(index, self)
                    case 'Q':
                        possible_moves = piece.queen_possible_moves(index, self)
                    case 'K':
                        possible_moves = piece.king_possible_moves(index, self)
                        possible_castling_moves = piece.king_possible_castling_moves(index, self)

                for move in possible_moves:
                    to_pos = coord[move]
                    all_possible_moves.append((from_pos, to_pos, ''))

                for promotion in possible_promotions:
                    to_pos = coord[promotion]
                    for promotion_piece in ['Q', 'R', 'B', 'N']:
                        all_possible_moves.append((from_pos, to_pos, promotion_piece))

                for castling_move in possible_castling_moves:
                    to_pos = coord[castling_move]
                    all_possible_moves.append((from_pos, to_pos, 'CASTLE'))

        return all_possible_moves

    def apply_castling_move(self,from_pos, to_pos):
        """
        Applies a castling move between the king and rook.

        :param from_pos: The position of the king to move.
        :param to_pos: The position where the king is being moved for castling.
        """
        from_pos_index = coord.index(from_pos)
        to_pos_index = coord.index(to_pos)
        
        if from_pos == 'e1' and to_pos == 'c1':
            self.cases[coord.index('c1')] = self.cases[coord.index('e1')]
            self.cases[coord.index('e1')] = Piece(' ','NONE')
            self.cases[coord.index('a1')] = Piece(' ','NONE')
            self.cases[coord.index('d1')] = Piece('R','WHITE')
            self.white_can_castle_56=False
            self.white_can_castle_63=False
        elif from_pos == 'e1' and to_pos == 'g1':
            self.cases[coord.index('g1')] = self.cases[coord.index('e1')]
            self.cases[coord.index('e1')] = Piece(' ','NONE')
            self.cases[coord.index('h1')] = Piece(' ','NONE')
            self.cases[coord.index('f1')] = Piece('R','WHITE')
            self.white_can_castle_56=False
            self.white_can_castle_63=False
        elif from_pos == 'e8' and to_pos == 'c8':
            self.cases[coord.index('c8')] = self.cases[coord.index('e8')]
            self.cases[coord.index('e8')] = Piece(' ','NONE')
            self.cases[coord.index('a8')] = Piece(' ','NONE')
            self.cases[coord.index('d8')] = Piece('R','BLACK')
            self.black_can_castle_0=False
            self.black_can_castle_7=False
        elif from_pos == 'e8' and to_pos == 'g8':
            self.cases[coord.index('g8')] = self.cases[coord.index('e8')]
            self.cases[coord.index('e8')] = Piece(' ','NONE')
            self.cases[coord.index('h8')] = Piece(' ','NONE')
            self.cases[coord.index('f8')] = Piece('R','BLACK')
            self.black_can_castle_0=False
            self.black_can_castle_7=False

    def apply_move(self, from_pos, to_pos):
        """
        Applies a move from from_pos to to_pos.

        :param from_pos: The position of the piece to move.
        :param to_pos: The position where the piece is being moved.
        """
        piece = self.cases[coord.index(from_pos)]
        self.cases[coord.index(to_pos)] = piece
        self.cases[coord.index(from_pos)] = Piece(' ','NONE')

    def apply_pawn_promotion(self, from_pos, to_pos, promotion_piece):
        """
        Applies a pawn promotion move.

        :param from_pos: The position of the pawn to promote.
        :param to_pos: The position where the pawn is being promoted.
        :param promotion_piece: The piece to promote to (e.g., 'Q' for queen).
        """
        piece = self.cases[coord.index(from_pos)]
        self.cases[coord.index(to_pos)] = Piece(promotion_piece, piece.color)
        self.cases[coord.index(from_pos)] = Piece(' ','NONE')
        

    def log_move(piece, from_pos, to_pos):
        """
        Logs a move made by a piece.

        :param piece: The piece that is moving.
        :param from_pos: The starting position of the piece.
        :param to_pos: The ending position of the piece.
        """
        # This function would log the move in a standard chess notation format.
        # For simplicity, we will just print the move here.
        print(f"{piece.color} {piece.name} moves from {from_pos} to {to_pos}")

        #TODO: Implement move logging in standard chess notation format