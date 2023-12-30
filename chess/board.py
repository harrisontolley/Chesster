""" board.py:
This module contains the Board class, which represents the chess board.
"""
from pieces import Piece, convert_piece_to_string

class Board:
    Square = [0] * 64

    def __init__(self):
        self.current_turn = Piece.WHITE
        self.selected_piece = None
        self.selected_square = None
        self.original_square = None
        self.destination_square = None

    def __str__(self):
        board_str = ""
        for rank in range(7, -1, -1):  # Start from the bottom rank
            for file in range(8):
                piece = self.Square[rank * 8 + file]
                board_str += convert_piece_to_string(piece)
            board_str += "\n"
        return board_str
    
    def select_piece(self, index):
        if self.Square[index] == Piece.NONE:  # If the square is empty, do nothing
            return
        # If it's not the turn of the piece's color, do nothing
        if Piece.get_color(self.Square[index]) != self.current_turn:
            return
        self.selected_piece = (index, self.Square[index])
        self.selected_square = (7 - index // 8, index % 8)  # Set selected_square here
        self.original_square = self.selected_square  # Store the original square

    def deselect_piece(self):
        self.selected_piece = None
        self.selected_square = None
        self.original_square = None  # Clear the original square
        self.destination_square = None  # Clear the destination square

    def move_piece(self, index):
        # Calculate the rank and file of the destination square
        file = index % 8
        rank = 7 - index // 8

        # Move the piece to the new square
        self.Square[self.selected_piece[0]] = Piece.NONE
        self.Square[index] = self.selected_piece[1]
        self.selected_piece = None
        self.destination_square = (rank, file)  # Store the destination square
        self.selected_square = None
        # Switch the turn
        self.current_turn = Piece.BLACK if self.current_turn == Piece.WHITE else Piece.WHITE

    def get_fen(self):
        fen = ""
        empty_count = 0
        for rank in range(8):
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
                empty_count = 0
            if rank < 7:
                fen += "/"
        return fen


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