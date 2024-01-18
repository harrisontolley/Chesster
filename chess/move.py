"""move.py:
This file contains the Move class, which is used to represent a move in the game.
"""
from pieces import *
from coordinates import Coordinates

class Move:
    def __init__(self, piece: Piece, current_coords: Coordinates, destination_coords: Coordinates):
        self.piece = piece
        self.current_coords = current_coords
        self.destination_coords = destination_coords

    def __str__(self):
        return f"{convert_piece_to_string(self.piece)} from {self.current_coords} to {self.destination_coords}"
    
    def get_current_coordinates(self):
        return self.current_coords
    
    def get_destination_coordinates(self):
        return self.destination_coords

    def get_piece(self):
        return self.piece
    
    def get_piece_type(self):
        return Piece.get_piece_type(self.piece)
    
    def get_piece_color(self):
        return Piece.get_color(self.piece)
    
    def __eq__(self, other) -> bool:
        return self.piece == other.piece and self.current_coords == other.current_coords and self.destination_coords == other.destination_coords