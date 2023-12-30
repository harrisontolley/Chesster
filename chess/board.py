""" board.py:
This module contains the Board class, which represents the chess board.
"""
from pieces import Piece, convert_piece_to_string

class Board:
    Square = [0] * 64

    def __init__(self):
        self.current_turn = Piece.WHITE
        self.selected_piece = None
        self.selected_square = None
        self.original_square = None
        self.destination_square = None

    def __str__(self):
        board_str = ""
        for rank in range(7, -1, -1):  # Start from the bottom rank
            for file in range(8):
                piece = self.Square[rank * 8 + file]
                board_str += convert_piece_to_string(piece)
            board_str += "\n"
        return board_str
    
    def select_piece(self, index):
        if self.Square[index] == Piece.NONE:  # If the square is empty, do nothing
            return
        # If it's not the turn of the piece's color, do nothing
        if Piece.get_color(self.Square[index]) != self.current_turn:
            return
        self.selected_piece = (index, self.Square[index])
        self.selected_square = (7 - index // 8, index % 8)  # Set selected_square here
        self.original_square = self.selected_square  # Store the original square

    def deselect_piece(self):
        self.selected_piece = None
        self.selected_square = None
        self.original_square = None  # Clear the original square
        self.destination_square = None  # Clear the destination square

    def move_piece(self, index):
        # Calculate the rank and file of the destination square
        file = index % 8
        rank = 7 - index // 8

        # Move the piece to the new square
        self.Square[self.selected_piece[0]] = Piece.NONE
        self.Square[index] = self.selected_piece[1]
        self.selected_piece = None
        self.destination_square = (rank, file)  # Store the destination square
        self.selected_square = None
        # Switch the turn
        self.current_turn = Piece.BLACK if self.current_turn == Piece.WHITE else Piece.WHITE

    def get_fen(self):
        fen = ""
        empty_count = 0
        for rank in range(8):
            for file in range(8):
                piece = self.Square[rank * 8 + file]
                if piece == Piece.NONE:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    fen += convert_piece_to_string(piece)
            if empty_count > 0:
                fen += str(empty_count)
                empty_count = 0
            if rank < 7:
                fen += "/"
        return fen
    
    def get_valid_moves(self, colour_to_move):
        moves = []
        for rank in range(8):
            for file in range(8):
                piece = self.Square[rank * 8 + file]
                if Piece.get_color(piece) == colour_to_move:
                    moves += self.get_piece_moves(piece, rank, file)
        return moves

    def get_piece_moves(self, piece, rank, file):
        piece_type = Piece.get_piece_type(piece)
        color = Piece.get_color(piece)
        if piece_type == Piece.PAWN:
            return self.get_pawn_moves(piece, rank, file)
        elif piece_type == Piece.KNIGHT:
            return self.get_knight_moves(piece, rank, file)
        elif piece_type == Piece.BISHOP:
            return self.get_bishop_moves(piece, rank, file)
        elif piece_type == Piece.ROOK:
            return self.get_rook_moves(piece, rank, file)
        elif piece_type == Piece.QUEEN:
            return self.get_queen_moves(piece, rank, file)
        elif piece_type == Piece.KING:
            return self.get_king_moves(piece, rank, file)
        return []
    
    def get_pawn_moves(self, piece, rank, file):
        moves = []
        color = Piece.get_color(piece)
        direction = 1 if color == Piece.WHITE else -1
        if rank + direction in range(8) and self.Square[(rank + direction) * 8 + file] == Piece.NONE:
            moves.append((rank + direction, file))
            if (rank == 1 and color == Piece.WHITE) or (rank == 6 and color == Piece.BLACK):
                if self.Square[(rank + 2 * direction) * 8 + file] == Piece.NONE:
                    moves.append((rank + 2 * direction, file))
        if rank + direction in range(8) and file - 1 in range(8) and self.Square[(rank + direction) * 8 + file - 1] != Piece.NONE and Piece.get_color(self.Square[(rank + direction) * 8 + file - 1]) != color:
            moves.append((rank + direction, file - 1))
        if rank + direction in range(8) and file + 1 in range(8) and self.Square[(rank + direction) * 8 + file + 1] != Piece.NONE and Piece.get_color(self.Square[(rank + direction) * 8 + file + 1]) != color:
            moves.append((rank + direction, file + 1))
        return moves
    
    def get_knight_moves(self, piece, rank, file):
        moves = []
        color = Piece.get_color(piece)
        for i in range(-2, 3):
            for j in range(-2, 3):
                if abs(i) + abs(j) == 3:
                    if rank + i in range(8) and file + j in range(8):
                        if self.Square[(rank + i) * 8 + file + j] == Piece.NONE or Piece.get_color(self.Square[(rank + i) * 8 + file + j]) != color:
                            moves.append((rank + i, file + j))
        return moves
    
    def get_bishop_moves(self, piece, rank, file):
        moves = []
        color = Piece.get_color(piece)
        for i in range(1, 8):
            if rank + i in range(8) and file + i in range(8):
                if self.Square[(rank + i) * 8 + file + i] == Piece.NONE:
                    moves.append((rank + i, file + i))
                elif Piece.get_color(self.Square[(rank + i) * 8 + file + i]) != color:
                    moves.append((rank + i, file + i))
                    break
                else:
                    break
        for i in range(1, 8):
            if rank - i in range(8) and file + i in range(8):
                if self.Square[(rank - i) * 8 + file + i] == Piece.NONE:
                    moves.append((rank - i, file + i))
                elif Piece.get_color(self.Square[(rank - i) * 8 + file + i]) != color:
                    moves.append((rank - i, file + i))
                    break
                else:
                    break
        for i in range(1, 8):
            if rank + i in range(8) and file - i in range(8):
                if self.Square[(rank + i) * 8 + file - i] == Piece.NONE:
                    moves.append((rank + i, file - i))
                elif Piece.get_color(self.Square[(rank + i) * 8 + file - i]) != color:
                    moves.append((rank + i, file - i))
                    break
                else:
                    break
        for i in range(1, 8):
            if rank - i in range(8) and file - i in range(8):
                if self.Square[(rank - i) * 8 + file - i] == Piece.NONE:
                    moves.append((rank - i, file - i))
                elif Piece.get_color(self.Square[(rank - i) * 8 + file - i]) != color:
                    moves.append((rank - i, file - i))
                    break
                else:
                    break
        return moves
    
    def get_rook_moves(self, piece, rank, file):
        moves = []
        color = Piece.get_color(piece)
        for i in range(1, 8):
            if rank + i in range(8):
                if self.Square[(rank + i) * 8 + file] == Piece.NONE:
                    moves.append((rank + i, file))
                elif Piece.get_color(self.Square[(rank + i) * 8 + file]) != color:
                    moves.append((rank + i, file))
                    break
                else:
                    break
        for i in range(1, 8):
            if rank - i in range(8):
                if self.Square[(rank - i) * 8 + file] == Piece.NONE:
                    moves.append((rank - i, file))
                elif Piece.get_color(self.Square[(rank - i) * 8 + file]) != color:
                    moves.append((rank - i, file))
                    break
                else:
                    break
        for i in range(1, 8):
            if file + i in range(8):
                if self.Square[rank * 8 + file + i] == Piece.NONE:
                    moves.append((rank, file + i))
                elif Piece.get_color(self.Square[rank * 8 + file + i]) != color:
                    moves.append((rank, file + i))
                    break
                else:
                    break
        for i in range(1, 8):
            if file - i in range(8):
                if self.Square[rank * 8 + file - i] == Piece.NONE:
                    moves.append((rank, file - i))
                elif Piece.get_color(self.Square[rank * 8 + file - i]) != color:
                    moves.append((rank, file - i))
                    break
                else:
                    break
        return moves
    
    def get_queen_moves(self, piece, rank, file):
        moves = []
        moves += self.get_bishop_moves(piece, rank, file)
        moves += self.get_rook_moves(piece, rank, file)
        return moves
    
    def get_king_moves(self, piece, rank, file):
        moves = []
        color = Piece.get_color(piece)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if rank + i in range(8) and file + j in range(8):
                    if self.Square[(rank + i) * 8 + file + j] == Piece.NONE or Piece.get_color(self.Square[(rank + i) * 8 + file + j]) != color:
                        moves.append((rank + i, file + j))
        return moves
    
    def is_in_check(self, color):
        for rank in range(8):
            for file in range(8):
                piece = self.Square[rank * 8 + file]
                if Piece.get_color(piece) != color:
                    continue
                moves = self.get_piece_moves(piece, rank, file)
                for move in moves:
                    if self.Square[move[0] * 8 + move[1]] == Piece.create_piece(Piece.KING, color):
                        return True
        return False
    
    def is_in_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        for rank in range(8):
            for file in range(8):
                piece = self.Square[rank * 8 + file]
                if Piece.get_color(piece) != color:
                    continue
                moves = self.get_piece_moves(piece, rank, file)
                for move in moves:
                    board_copy = Board()
                    board_copy.Square = self.Square.copy()
                    board_copy.move_piece(move[0] * 8 + move[1])
                    if not board_copy.is_in_check(color):
                        return False
        return True
    
    def is_in_stalemate(self, color):
        if self.is_in_check(color):
            return False
        for rank in range(8):
            for file in range(8):
                piece = self.Square[rank * 8 + file]
                if Piece.get_color(piece) != color:
                    continue
                moves = self.get_piece_moves(piece, rank, file)
                for move in moves:
                    board_copy = Board()
                    board_copy.Square = self.Square.copy()
                    board_copy.move_piece(move[0] * 8 + move[1])
                    if not board_copy.is_in_check(color):
                        return False
        return True
    
    def is_draw(self):
        return self.is_in_stalemate(Piece.WHITE) or self.is_in_stalemate(Piece.BLACK) or self.is_in_checkmate(Piece.WHITE) or self.is_in_checkmate(Piece.BLACK)
    
def LoadPositionFromFen(fen):
    board = Board()
    rank, file = 7, 0  # Start from the top-left corner of the board

    for char in fen:
        if char == ' ':
            break  # Ignore the rest of the FEN string after the position part

        if char == '/':
            rank -= 1
            file = 0
        elif char.isdigit():
            file += int(char)
        else:
            color = Piece.WHITE if char.isupper() else Piece.BLACK
            piece_type = 0

            char_lower = char.lower()
            if char_lower == 'k':
                piece_type = Piece.KING
            elif char_lower == 'p':
                piece_type = Piece.PAWN
            elif char_lower == 'n':
                piece_type = Piece.KNIGHT
            elif char_lower == 'b':
                piece_type = Piece.BISHOP
            elif char_lower == 'r':
                piece_type = Piece.ROOK
            elif char_lower == 'q':
                piece_type = Piece.QUEEN

            board.Square[rank * 8 + file] = Piece.create_piece(piece_type, color)
            file += 1

    return board