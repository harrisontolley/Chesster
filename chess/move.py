"""move.py:
This file contains the Move class, which is used to represent a move in the game.
"""
from pieces import *
from coordinates import Coordinates

class Move:
    def __init__(self, piece: Piece, current_square: Coordinates, destination_square: Coordinates):
        self.piece = piece
        self.current_square = current_square
        self.destination_square = destination_square

    def __str__(self):
        return f"{convert_piece_to_string(self.piece)} from {self.current_square} to {self.destination_square}"
    
    def get_current_square(self):
        return self.current_square
    
    def get_destination_square(self):
        return self.destination_square

    def get_piece(self):
        return self.piece
    
    def get_piece_type(self):
        return Piece.get_piece_type(self.piece)
    
    def get_piece_color(self):
        return Piece.get_color(self.piece)
    
    def __eq__(self, other) -> bool:
        return self.piece == other.piece and self.current_square == other.current_square and self.destination_square == other.destination_square