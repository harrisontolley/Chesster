""" pieces.py:
This file contains the Piece class, which is used to represent chess pieces.
"""


class Piece:
    # Piece types
    NONE = 0
    KING = 1
    PAWN = 2
    KNIGHT = 3
    BISHOP = 4
    ROOK = 5
    QUEEN = 6

    # Colors
    WHITE = 8
    BLACK = 16

    @staticmethod
    def create_piece(piece_type, color):
        return piece_type | color

    @staticmethod
    def get_piece_type(piece):
        return piece & 7

    @staticmethod
    def get_color(piece):
        return piece & 24

    def __str__(self):
        piece_type = Piece.get_piece_type(self)
        color = Piece.get_color(self)

        if color == Piece.BLACK:
            return piece_translation[piece_type].lower()
        elif color == Piece.WHITE:
            return piece_translation[piece_type].upper()
        else:
            return piece_translation[piece_type]


def convert_piece_to_string(piece):
    piece_type = Piece.get_piece_type(piece)
    color = Piece.get_color(piece)

    if color == Piece.BLACK:
        return piece_translation[piece_type].lower()
    elif color == Piece.WHITE:
        return piece_translation[piece_type].upper()
    else:
        return piece_translation[piece_type]


piece_translation = {
    Piece.KING: "k",
    Piece.PAWN: "p",
    Piece.KNIGHT: "n",
    Piece.BISHOP: "b",
    Piece.ROOK: "r",
    Piece.QUEEN: "q",
    Piece.NONE: "-",
}
