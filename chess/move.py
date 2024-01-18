"""move.py:
This file contains the Move class, which is used to represent a move in the game.
"""
from pieces import *
from coordinates import Coordinates

class Move:
    def __init__(self, piece: Piece, current_coords: Coordinates, destination_coords: Coordinates, is_en_passant=False, is_castling=False, is_promotion=False, promotion_piece=Piece.NONE):
        self.piece = piece
        self.current_coords = current_coords
        self.destination_coords = destination_coords
        self.get_is_en_passant = is_en_passant
        self.get_is_castling = is_castling
        self.get_is_promotion = is_promotion
        self.promotion_piece = promotion_piece

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
    
    def get_is_en_passant(self):
        return self.is_en_passant
    
    def get_is_castling(self):
        return self.is_castling
    
    def get_is_promotion(self):
        return self.is_promotion
    
    def get_promotion_piece(self):
        return self.promotion_piece