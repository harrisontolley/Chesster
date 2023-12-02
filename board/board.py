"""
File for the chess board class.
"""

from pieces.piece import Piece


class Board:
    def __init__(self) -> None:
        self.dimensions =  (8, 8)
        self.piece_array = []
    
    def piece_at_coords(self, coords) -> "Piece":
        """
        Returns the piece at the given coordinates.
        """
        return self.piece_array
    
    def is_piece_at_coords(self, coords) -> bool:
        """
        Returns whether there is a piece at the given coordinates.
        """
        return self.piece_at_coords(coords) != None
    
    def __str__(self) -> str:
        pass