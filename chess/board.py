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
        opponent_color = Piece.BLACK if self.current_turn == Piece.WHITE else Piece.WHITE
        if self.is_in_check(opponent_color):
            print(f"Player with color {opponent_color} is in check.")
        print(self)


    def get_fen(self):
        fen = ""
        for rank in range(8):
            empty_count = 0
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
            if rank < 7:
                fen += "/"
        
        active_color = 'w' if self.current_turn == Piece.WHITE else 'b'
        fen += " " + active_color
        return fen

    
    def get_valid_moves(self, color_to_move):
        all_moves = self.generate_all_possible_moves(color_to_move)
        if self.is_in_check(color_to_move):
            # Player is in check, filter moves to only those that can resolve the check
            return self.filter_moves_to_resolve_check(all_moves, color_to_move)
        else:
            # Player is not in check, filter out moves that would put the player in check
            return self.filter_moves_to_avoid_self_check(all_moves, color_to_move)

    def generate_all_possible_moves(self, color):
        moves = {}
        for i, piece in enumerate(self.Square):
            if Piece.get_color(piece) == color:
                rank, file = 7 - i // 8, i % 8
                moves[i] = self.get_piece_moves(piece, rank, file)
        print("All possible moves: ", moves)
        return moves
    
    def filter_moves_to_resolve_check(self, moves, color):
        valid_moves = {}
        for from_index, to_moves in moves.items():
            for move in to_moves:
                to_index = move[0] * 8 + move[1]
                if not self.simulate_move_and_check(from_index, to_index, color):
                    valid_moves.setdefault(from_index, []).append(move)
        return valid_moves

    def filter_moves_to_avoid_self_check(self, moves, color):
        valid_moves = {}
        for from_index, to_moves in moves.items():
            for move in to_moves:
                to_index = move[0] * 8 + move[1]
                if not self.simulate_move_and_check(from_index, to_index, color):
                    valid_moves.setdefault(from_index, []).append(move)
        return valid_moves

    def simulate_move_and_check(self, from_index, to_index, color):
        # Simulate the move
        original_piece = self.Square[from_index]
        captured_piece = self.Square[to_index]
        self.Square[to_index] = original_piece
        self.Square[from_index] = Piece.NONE

        # Check for check status after the move
        is_in_check_after_move = self.is_in_check(color)

        # Revert the move
        self.Square[from_index] = original_piece
        self.Square[to_index] = captured_piece

        return is_in_check_after_move
    
    def filter_moves_leading_to_self_check(self, moves, color):
        """Filter out moves that would lead to self-check."""
        valid_moves = {}
        for from_index, to_moves in moves.items():
            for move in to_moves:
                to_index = move[0] * 8 + move[1]
                if not self.move_simulate_and_check(from_index, to_index):
                    valid_moves.setdefault(from_index, []).append(move)
        return valid_moves

    def filter_moves_in_check(self, moves, color):
        """Return only moves that get the player out of check."""
        valid_moves = {}
        for from_index, to_moves in moves.items():
            for move in to_moves:
                to_index = move[0] * 8 + move[1]
                if not self.move_simulate_and_check(from_index, to_index):
                    valid_moves.setdefault(from_index, []).append(move)
        return valid_moves
    


    def filter_check_moves(self, moves, color):
        """Filters moves to only those that remove check."""
        valid_moves = {}
        for from_index, to_moves in moves.items():
            valid_moves_for_piece = []
            for move in to_moves:
                to_index = move[0] * 8 + move[1]
                if not self.move_simulate(from_index, to_index):
                    valid_moves_for_piece.append(move)
            if valid_moves_for_piece:
                valid_moves[from_index] = valid_moves_for_piece
        return valid_moves

    def move_simulate(self, from_index, to_index):
        """Simulates a move and checks if it results in the player being in check."""
        # Store original state
        original_piece = self.Square[from_index]
        captured_piece = self.Square[to_index]
        original_turn = self.current_turn

        # Perform the move
        self.Square[to_index] = original_piece
        self.Square[from_index] = Piece.NONE

        # Change turn to opponent's to check if the move results in a check
        self.current_turn = Piece.BLACK if self.current_turn == Piece.WHITE else Piece.WHITE
        in_check = self.is_in_check(Piece.get_color(original_piece))

        # Revert the move and turn
        self.Square[from_index] = original_piece
        self.Square[to_index] = captured_piece
        self.current_turn = original_turn

        return in_check
    
    def move_simulate_and_check(self, from_index, to_index):
        """Simulate a move and check if it leads to self-check."""
        piece = self.Square[from_index]
        captured_piece = self.Square[to_index]
        self.Square[to_index] = piece
        self.Square[from_index] = Piece.NONE
        in_check = self.is_in_check(Piece.get_color(piece))
        self.Square[from_index] = piece
        self.Square[to_index] = captured_piece
        return in_check

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
        # Find the king's position
        king_position = None
        for i, piece in enumerate(self.Square):
            if Piece.get_piece_type(piece) == Piece.KING and Piece.get_color(piece) == color:
                king_position = (7 - i // 8, i % 8)
                break

        # Check for threats to the king
        opponent_color = Piece.BLACK if color == Piece.WHITE else Piece.BLACK
        for i, piece in enumerate(self.Square):
            if Piece.get_color(piece) == opponent_color:
                moves = self.get_piece_moves(piece, 7 - i // 8, i % 8)
                if king_position in [(move[0], move[1]) for move in moves]:
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
    parts = fen.split()
    piece_placement = parts[0]
    active_color = parts[1]

    rank, file = 7, 0  # Start from the top-left corner of the board
    for char in piece_placement:
        if char == '/':
            rank -= 1
            file = 0
        elif char.isdigit():
            file += int(char)
        else:
            color = Piece.WHITE if char.isupper() else Piece.BLACK
            piece_type = {
                'P': Piece.PAWN, 'N': Piece.KNIGHT, 'B': Piece.BISHOP,
                'R': Piece.ROOK, 'Q': Piece.QUEEN, 'K': Piece.KING
            }.get(char.upper(), 0)
            board.Square[rank * 8 + file] = Piece.create_piece(piece_type, color)
            file += 1

    board.current_turn = Piece.WHITE if active_color == 'w' else Piece.BLACK
    return board
