"""
File for the chess board class.
"""

from pieces.pieces import *
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

    def get_king(self, colour) -> "King":
        """
        Returns the king of the given colour.
        """
        for piece in self.piece_array:
            if isinstance(piece, King) and piece.get_colour() == colour:
                return piece
        return None # This should never happen, but just in case