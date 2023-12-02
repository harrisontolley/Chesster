"""
File for the piece class, which is parent to all the other chess pieces.
"""
from typing import Optional

class Piece:
    def __init__(self, coords, board, colour="White" or "Black") -> None:
        self.coords = coords
        self.colour = colour
        self.board = board
        
        self.valid_moves = self.get_valid_moves()
    
    def move(self, new_coords) -> None:
        """
        Moves the piece to the new coordinates, taking the piece at the new coordinates if there is one.
        """
        raise NotImplementedError
    
    def get_valid_moves(self) -> list:
        """
        Returns a list of valid moves for the piece.
        """
        raise NotImplementedError
    
    def get_colour(self) -> str:
        """
        Returns the colour of the piece.
        """
        return self.colour

    
    def __str__(self) -> str:
        """
        String representation of the piece.
        Example: "White Pawn (1, 1)"
        """
        return self.colour + " " + self.__class__.__name__ + " " + str(self.coords)
    

class Pawn(Piece):
    def __init__(self, coords, board, colour="White" or "Black") -> None:
        super().__init__(coords, board, colour)
    
    def move(self, new_coords) -> None:
        """
        Moves the pawn to the new coordinates, if coordinates are valid.
        """
        # ! ATM this doesnt account for possible piece taking
        if new_coords in self.valid_moves:
            self.coords = new_coords
        else:
            raise InvalidMove("Invalid move for pawn.")
    
    def get_valid_moves(self) -> list:
        """
        Gets valid moves for the pawn, this includes the coordinates it can move to and the coordinates it can take a piece at.
        """
        valid_moves = []        
        if self.colour == "White":
            # check if pawn can take a piece left or right
            if self.board.is_piece_at_coords((self.coords[0] + 1, self.coords[1] + 1)):
                valid_moves.append((self.coords[0] + 1, self.coords[1] + 1))


            return [(self.coords[0], self.coords[1] + 1), (self.coords[0], self.coords[1] + 2)]
        else:
            return [(self.coords[0], self.coords[1] - 1), (self.coords[0], self.coords[1] - 2)]
    
