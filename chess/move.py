"""move.py:
This file contains the Move class, which is used to represent a move in the game.
"""
from pieces import *
from coordinates import Coordinates

class Move:
    def __init__(self, piece: Piece, current_coords: Coordinates, destination_coords: Coordinates, can_en_passant=False, is_castling=False, is_promotion=False, promotion_piece=Piece.NONE):
        self.piece = piece
        self.current_coords = current_coords
        self.destination_coords = destination_coords
        self.can_en_passant = can_en_passant
        self.get_is_castling = is_castling
        self.get_is_promotion = is_promotion
        self.promotion_piece = promotion_piece

        self.en_passant_idx = None
        if self.get_can_en_passant():
            print("over here")
            self.en_passant_idx = Coordinates(self.destination_coords.get_file(), self.current_coords.get_rank() + 1 if Piece.get_color(piece) == Piece.WHITE else self.current_coords.get_rank() - 1).get_board_index()

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
    
    def get_can_en_passant(self):
        return self.can_en_passant
    
    def get_is_castling(self):
        return self.is_castling
    
    def get_is_promotion(self):
        return self.is_promotion
    
    def get_promotion_piece(self):
        return self.promotion_piece
    
    def get_en_passant_idx(self):
        return self.en_passant_idx