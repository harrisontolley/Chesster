"""square.py:
This file contains the Square class, which is used to represent a square on the chess board.
"""

class Coordinates:
    def __init__(self, file: int, rank: int):
        self.file = file
        self.rank = rank

    def __str__(self):
        return f"({self.rank}, {self.file})"

    def __eq__(self, other):
        return self.rank == other.rank and self.file == other.file

    def __repr__(self):
        return str(self)

    def get_board_index(self):
        return self.rank * 8 + self.file