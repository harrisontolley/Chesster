"""
File for the piece class, which is parent to all the other chess pieces.
"""
from typing import Optional
from exceptions import InvalidMove

class Piece:
    def __init__(self, coords, board, colour="White") -> None:
        self.total_moves = 0
        self.coords = coords
        self.colour = colour
        self.board = board
        self.valid_moves = self.get_valid_moves()

    def move(self, new_coords) -> None:
        raise NotImplementedError

    def get_valid_moves(self) -> list:
        raise NotImplementedError

    def get_colour(self) -> str:
        return self.colour

    def __str__(self) -> str:
        return f"{self.colour} {self.__class__.__name__} {self.coords}"


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
            self.valid_moves = self.get_valid_moves()
        else:
            raise InvalidMove("Invalid move for pawn.")
        
    def get_valid_moves(self) -> list:
        """
        Gets valid moves for the pawn, this includes the coordinates it can move to and the coordinates it can take a piece at.
        """
        # we can move forward, if there is no piece in front of us
        # we can move forward 2, if there is no piece in front of us and we are in our starting position    
        # we can take a piece diagonally in front of us, if there is a piece there and it is of the opposite colour
        # have to also check pawn is not at the edge of the board
        valid_moves = []
        forward_direction = 1 if self.colour == "White" else -1

        # Check moving forward
        if not self.board.is_piece_at_coords((self.coords[0], self.coords[1] + forward_direction)):
            valid_moves.append((self.coords[0], self.coords[1] + forward_direction))
            # Adds moving forward to valid moves

            # Check if in starting position
            if self.total_moves == 0:
                # Check if there is a piece 2 in front
                if not self.board.is_piece_at_coords((self.coords[0], self.coords[1] + 2 * forward_direction)):
                    valid_moves.append((self.coords[0], self.coords[1] + 2 * forward_direction))
                    # Adds moving forward 2 to valid moves

            # Check if on the edge of the board
            for offset in [-1, 1]:
                diagonal_coords = (self.coords[0] + offset, self.coords[1] + forward_direction)
                if 0 <= diagonal_coords[0] <= 7:
                    # Check if there is a piece diagonally
                    if self.board.is_piece_at_coords(diagonal_coords):
                        # Check if piece is of opposite colour
                        if self.board.piece_at_coords(diagonal_coords).get_colour() != self.colour:
                            valid_moves.append(diagonal_coords)
                            # Adds taking piece diagonally to valid moves

        return valid_moves

