"""move.py:
This file contains the Move class, which is used to represent a move in the game.
"""
from pieces import *

class Move:
    def __init__(self, piece: Piece, current_square: tuple, destination_square: tuple):
        self.piece = piece
        self.current_square = current_square
        self.destination_square = destination_square

    def __str__(self):
        return f"{convert_piece_to_string(self.piece)} from {self.current_square} to {self.destination_square}"