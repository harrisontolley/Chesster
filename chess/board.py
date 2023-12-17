""" board.py:
This module contains the Board class, which represents the chess board.
"""
from pieces import Piece, convert_piece_to_string

class Board:
    Square = [0] * 64

    def __init__(self):
        self.Square[0] = Piece.WHITE | Piece.BISHOP
        self.Square[63] = Piece.BLACK | Piece.QUEEN


def LoadPositionFromFen(fen):
    board = Board()
    rank, file = 7, 0  # Start from the top-left corner of the board

    for char in fen:
        if char == ' ':
            break  # Ignore the rest of the FEN string after the position part

        if char == '/':
            rank -= 1
            file = 0
        elif char.isdigit():
            file += int(char)
        else:
            color = Piece.WHITE if char.isupper() else Piece.BLACK
            piece_type = 0

            char_lower = char.lower()
            if char_lower == 'k':
                piece_type = Piece.KING
            elif char_lower == 'p':
                piece_type = Piece.PAWN
            elif char_lower == 'n':
                piece_type = Piece.KNIGHT
            elif char_lower == 'b':
                piece_type = Piece.BISHOP
            elif char_lower == 'r':
                piece_type = Piece.ROOK
            elif char_lower == 'q':
                piece_type = Piece.QUEEN

            board.Square[rank * 8 + file] = Piece.create_piece(piece_type, color)
            file += 1

    return board





# Example usage:
starting_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
loaded_board = LoadPositionFromFen(starting_position)

# Print the loaded board
for rank in range(7, -1, -1):
    for file in range(8):
        piece = loaded_board.Square[rank * 8 + file]
        print(convert_piece_to_string(piece), end=" ")
    print()