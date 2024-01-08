""" board.py:
This module contains the Board class, which represents the chess board.
"""
from pieces import Piece, convert_piece_to_string

class Board:

    def __init__(self):
        self.current_turn = Piece.WHITE
        self.selected_piece = None
        self.selected_square = None
        self.original_square = None
        self.destination_square = None

        self.en_passant_square = '-'
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.castling_availability = 'KQkq'

        self.square_to_index = {
            "a1": 0, "b1": 1, "c1": 2, "d1": 3, "e1": 4, "f1": 5, "g1": 6, "h1": 7,
            "a2": 8, "b2": 9, "c2": 10, "d2": 11, "e2": 12, "f2": 13, "g2": 14, "h2": 15,
            "a3": 16, "b3": 17, "c3": 18, "d3": 19, "e3": 20, "f3": 21, "g3": 22, "h3": 23,
            "a4": 24, "b4": 25, "c4": 26, "d4": 27, "e4": 28, "f4": 29, "g4": 30, "h4": 31,
            "a5": 32, "b5": 33, "c5": 34, "d5": 35, "e5": 36, "f5": 37, "g5": 38, "h5": 39,
            "a6": 40, "b6": 41, "c6": 42, "d6": 43, "e6": 44, "f6": 45, "g6": 46, "h6": 47,
            "a7": 48, "b7": 49, "c7": 50, "d7": 51, "e7": 52, "f7": 53, "g7": 54, "h7": 55,
            "a8": 56, "b8": 57, "c8": 58, "d8": 59, "e8": 60, "f8": 61, "g8": 62, "h8": 63,
        }

        self.index_to_square = {
            0: "a1", 1: "b1", 2: "c1", 3: "d1", 4: "e1", 5: "f1", 6: "g1", 7: "h1",
            8: "a2", 9: "b2", 10: "c2", 11: "d2", 12: "e2", 13: "f2", 14: "g2", 15: "h2",
            16: "a3", 17: "b3", 18: "c3", 19: "d3", 20: "e3", 21: "f3", 22: "g3", 23: "h3",
            24: "a4", 25: "b4", 26: "c4", 27: "d4", 28: "e4", 29: "f4", 30: "g4", 31: "h4",
            32: "a5", 33: "b5", 34: "c5", 35: "d5", 36: "e5", 37: "f5", 38: "g5", 39: "h5",
            40: "a6", 41: "b6", 42: "c6", 43: "d6", 44: "e6", 45: "f6", 46: "g6", 47: "h6",
            48: "a7", 49: "b7", 50: "c7", 51: "d7", 52: "e7", 53: "f7", 54: "g7", 55: "h7",
            56: "a8", 57: "b8", 58: "c8", 59: "d8", 60: "e8", 61: "f8", 62: "g8", 63: "h8",
        }

        self.Square = [0] * 64

    def __str__(self):
        board_str = ""
        for rank in range(7, -1, -1):  # Start from the bottom rank
            for file in range(8):
                piece = self.Square[rank * 8 + file]
                board_str += convert_piece_to_string(piece)
            board_str += "\n"
        return board_str
    
    def convert_file_rank_to_index(self, file, rank):        
        return (rank * 8) + file

    def move_piece(self, piece, current_square, destination_square):
        # Calculate the index for the current and destination squares

        # print("--------------MOVE PIECE FUNCTION--------------")
        # print("CURRENT SQUARE: ", current_square)
        # print("SQUARE[CURRENT SQUARE]: ", convert_piece_to_string(self.Square[destination_square]))
        # print("DESTINATIOON SQUARE: ", destination_square)
        # print("SQUARE[DESTINATION SQUARE]: ", convert_piece_to_string(self.Square[destination_square]))

        # Move the piece
        self.Square[current_square] = Piece.NONE

        self.Square[destination_square] = piece

        # Switch the turn
        self.current_turn = Piece.BLACK if self.current_turn == Piece.WHITE else Piece.WHITE
        # print(self)

    def get_pieces_for_color(self, color):
        '''Returns a list of pieces for a given color.'''
        pieces = []
        for i, piece in enumerate(self.Square):
            print(i, convert_piece_to_string(piece))
            if Piece.get_color(piece) == color:
                pieces.append((i, piece))
        return pieces

    def get_valid_moves(self, color_to_move):
        # Want to get all valid moves for a color to move
        moves = []
        for piece in self.get_pieces_for_color(color_to_move):

            rank, file = 7 - piece[0] // 8, piece[0] % 8

            moves = self.get_piece_moves(piece[1], rank, file)
            moves_squares = [self.index_to_square[self.convert_file_rank_to_index(move[1], move[0])] for move in moves]
            print(f"Moves for {convert_piece_to_string(piece[1])} at {self.index_to_square[self.convert_file_rank_to_index(file, rank)]} {(file, rank)}: {moves_squares}")

    def get_piece_moves(self, piece, rank, file):
        piece_type = Piece.get_piece_type(piece)
        color = Piece.get_color(piece)
        if piece_type == Piece.PAWN:
            return self.get_pawn_moves(piece, rank, file)
        elif piece_type == Piece.KNIGHT:
            return self.get_knight_moves(piece, rank, file)
        elif piece_type == Piece.BISHOP:
            return self.get_bishop_moves(piece, rank, file)
        elif piece_type == Piece.ROOK:
            return self.get_rook_moves(piece, rank, file)
        elif piece_type == Piece.QUEEN:
            return self.get_queen_moves(piece, rank, file)
        elif piece_type == Piece.KING:
            return self.get_king_moves(piece, rank, file)
        return []
    
    def get_pawn_moves(self, piece, rank, file):
        moves = []
        color = Piece.get_color(piece)

        # Direction pawns can move (1 for white, -1 for black)
        direction = -1 if color == Piece.WHITE else 1

        # Forward move
        if 0 <= rank + direction < 8:

            if self.Square[self.convert_file_rank_to_index(file, rank + direction)] == Piece.NONE:
                moves.append((rank + direction, file))

                # Double move from starting position
                starting_rank = 1 if color == Piece.BLACK else 6
                if rank == starting_rank and self.Square[self.convert_file_rank_to_index(file, rank + 2 * direction)] == Piece.NONE:
                    moves.append((rank + 2 * direction, file))

        # Captures
        for offset in [-1, 1]:
            capture_file = file + offset
            if 0 <= capture_file < 8 and 0 <= rank + direction < 8:
                capture_index = self.convert_file_rank_to_index(capture_file, rank + direction)
                if self.Square[capture_index] != Piece.NONE and Piece.get_color(self.Square[capture_index]) == color:
                    moves.append((rank + direction, capture_file))

        # En passant
        if self.en_passant_square != '-':
            en_passant_rank, en_passant_file = 7 - self.square_to_index[self.en_passant_square] // 8, self.square_to_index[self.en_passant_square] % 8
            if rank == en_passant_rank and abs(file - en_passant_file) == 1:
                moves.append((en_passant_rank + direction, en_passant_file))

        return moves


    def get_knight_moves(self, piece, rank, file):
        moves = []
        color = Piece.get_color(piece)
        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i) + abs(j) == 3:
                    if rank + i in range(8) and file + j in range(8):
                        if self.Square[(rank + i) * 8 + file + j] == Piece.NONE or Piece.get_color(self.Square[(rank + i) * 8 + file + j]) == color:
                            moves.append((rank + i, file + j))
        return moves
    
    def get_bishop_moves(self, piece, rank, file):
        moves = []
        color = Piece.get_color(piece)
        for i in range(1, 8):
            if rank + i in range(8) and file + i in range(8):
                if self.Square[(rank + i) * 8 + file + i] == Piece.NONE:
                    moves.append((rank + i, file + i))
                elif Piece.get_color(self.Square[(rank + i) * 8 + file + i]) == color:
                    moves.append((rank + i, file + i))
                    break
                else:
                    break
        for i in range(1, 8):
            if rank - i in range(8) and file + i in range(8):
                if self.Square[(rank - i) * 8 + file + i] == Piece.NONE:
                    moves.append((rank - i, file + i))
                elif Piece.get_color(self.Square[(rank - i) * 8 + file + i]) == color:
                    moves.append((rank - i, file + i))
                    break
                else:
                    break
        for i in range(1, 8):
            if rank + i in range(8) and file - i in range(8):
                if self.Square[(rank + i) * 8 + file - i] == Piece.NONE:
                    moves.append((rank + i, file - i))
                elif Piece.get_color(self.Square[(rank + i) * 8 + file - i]) == color:
                    moves.append((rank + i, file - i))
                    break
                else:
                    break
        for i in range(1, 8):
            if rank - i in range(8) and file - i in range(8):
                if self.Square[(rank - i) * 8 + file - i] == Piece.NONE:
                    moves.append((rank - i, file - i))
                elif Piece.get_color(self.Square[(rank - i) * 8 + file - i]) == color:
                    moves.append((rank - i, file - i))
                    break
                else:
                    break
        return moves
    
    def get_rook_moves(self, piece, rank, file):
        moves = []
        color = Piece.get_color(piece)

        for i in range(1, 8):
            if rank + i in range(8):
                if self.Square[(rank + i) * 8 + file] == Piece.NONE:
                    moves.append((rank + i, file))
                elif Piece.get_color(self.Square[(rank + i) * 8 + file]) == color:
                    moves.append((rank + i, file))
                    break
                else:
                    break
        for i in range(1, 8):
            if rank - i in range(8):
                if self.Square[(rank - i) * 8 + file] == Piece.NONE:
                    moves.append((rank - i, file))
                elif Piece.get_color(self.Square[(rank - i) * 8 + file]) == color:
                    moves.append((rank - i, file))
                    break
                else:
                    break
        for i in range(1, 8):
            if file + i in range(8):
                if self.Square[rank * 8 + file + i] == Piece.NONE:
                    moves.append((rank, file + i))
                elif Piece.get_color(self.Square[rank * 8 + file + i]) == color:
                    moves.append((rank, file + i))
                    break
                else:
                    break
        for i in range(1, 8):
            if file - i in range(8):
                if self.Square[rank * 8 + file - i] == Piece.NONE:
                    moves.append((rank, file - i))
                elif Piece.get_color(self.Square[rank * 8 + file - i]) == color:
                    moves.append((rank, file - i))
                    break
                else:
                    break
        return moves
    
    def get_queen_moves(self, piece, rank, file):
        moves = []
        moves += self.get_bishop_moves(piece, rank, file)
        moves += self.get_rook_moves(piece, rank, file)
        return moves
    
    def get_king_moves(self, piece, rank, file):
        moves = []
        color = Piece.get_color(piece)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if rank + i in range(8) and file + j in range(8):
                    if self.Square[(rank + i) * 8 + file + j] == Piece.NONE or Piece.get_color(self.Square[(rank + i) * 8 + file + j]) == color:
                        moves.append((rank + i, file + j))
        return moves

    def clear_en_passant_square(self):
        self.en_passant_square = '-'
    
    def set_en_passant_square(self, square):
        self.en_passant_square = square
    
    def get_fen(self):
        fen = ""
        for rank in range(8):
            empty_count = 0
            for file in range(8):
                piece = self.Square[rank * 8 + file]
                if piece == Piece.NONE:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    fen += convert_piece_to_string(piece)
            if empty_count > 0:
                fen += str(empty_count)
            if rank < 7:
                fen += "/"
        
        active_color = 'w' if self.current_turn == Piece.WHITE else 'b'
        fen += " " + active_color
        return fen
    
    def load_position_from_fen(fen: str):
        board = Board()
        parts = fen.split()
        piece_placement = parts[0]
        active_color = parts[1]
        castling_availability = parts[2]
        en_passant_square = parts[3]
        halfmove_clock = parts[4]
        fullmove_number = parts[5]

        rank, file = 7, 0  # Start from the top-left corner of the board
        for char in piece_placement:
            if char == '/':
                rank -= 1
                file = 0
            elif char.isdigit():
                file += int(char)
            else:
                color = Piece.WHITE if char.isupper() else Piece.BLACK
                piece_type = {
                    'P': Piece.PAWN, 'N': Piece.KNIGHT, 'B': Piece.BISHOP,
                    'R': Piece.ROOK, 'Q': Piece.QUEEN, 'K': Piece.KING
                }.get(char.upper(), 0)
                board.Square[rank * 8 + file] = Piece.create_piece(piece_type, color)
                file += 1

        board.current_turn = Piece.WHITE if active_color == 'w' else Piece.BLACK
        return board
