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

        self.en_passant_square = '-'
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.castling_availability = 'KQkq'

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



    
    def get_pieces_for_color(self, color):
        '''Returns a list of pieces for a given color.'''
        pieces = []
        for i, piece in enumerate(self.Square):
            if Piece.get_color(piece) == color:
                pieces.append((i, piece))
        return pieces

    
    def get_valid_moves(self, color_to_move):
        # Want to get all valid moves for a color to move
        
        for piece in self.get_pieces_for_color(color_to_move):

            rank, file = 7 - piece[0] // 8, piece[0] % 8

            moves = self.get_piece_moves(piece[1], rank, file)
            print(f"Moves for {piece[1]} at {rank}, {file}: {moves}")


        # all_moves = self.generate_all_possible_moves(color_to_move)
        # if self.is_in_check(color_to_move):
        #     # Player is in check, filter moves to only those that can resolve the check
        #     return self.filter_moves_to_resolve_check(all_moves, color_to_move)
        # else:
        #     # Player is not in check, filter out moves that would put the player in check
        #     return self.filter_moves_to_avoid_self_check(all_moves, color_to_move)

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

        # if piece on starting rank, can move two squares forward
        # if color == Piece.WHITE and rank == 1:
        #     # check can move 1 or two squares forward
        #     if self.Square
        # else:



        # moves = []
        # color = Piece.get_color(piece)
        # direction = 1 if color == Piece.WHITE else -1
        # forward_rank = rank + direction

        # # Forward move
        # if 0 <= forward_rank < 8 and self.Square[forward_rank * 8 + file] == Piece.NONE:
        #     moves.append((forward_rank, file))
        #     # Initial two-square move
        #     start_rank = 1 if color == Piece.WHITE else 6
        #     two_squares_forward = rank + 2 * direction
        #     if rank == start_rank and self.Square[two_squares_forward * 8 + file] == Piece.NONE:
        #         moves.append((two_squares_forward, file))

        # # Captures
        # for capture_file in [file - 1, file + 1]:
        #     if 0 <= forward_rank < 8 and 0 <= capture_file < 8:
        #         target_piece = self.Square[forward_rank * 8 + capture_file]
        #         if target_piece != Piece.NONE and Piece.get_color(target_piece) != color:
        #             moves.append((forward_rank, capture_file))

        # return moves

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
    
    # def is_in_check(self, color):
    #     # Find the king's position
    #     king_position = None
    #     for i, piece in enumerate(self.Square):
    #         if Piece.get_piece_type(piece) == Piece.KING and Piece.get_color(piece) == color:
    #             king_position = (7 - i // 8, i % 8)
    #             break

    #     # Check for threats to the king
    #     opponent_color = Piece.BLACK if color == Piece.WHITE else Piece.BLACK
    #     for i, piece in enumerate(self.Square):
    #         if Piece.get_color(piece) == opponent_color:
    #             moves = self.get_piece_moves(piece, 7 - i // 8, i % 8)
    #             if king_position in [(move[0], move[1]) for move in moves]:
    #                 return True
    #     return False
    
    # def is_in_checkmate(self, color):
    #     if not self.is_in_check(color):
    #         return False
    #     for rank in range(8):
    #         for file in range(8):
    #             piece = self.Square[rank * 8 + file]
    #             if Piece.get_color(piece) != color:
    #                 continue
    #             moves = self.get_piece_moves(piece, rank, file)
    #             for move in moves:
    #                 board_copy = Board()
    #                 board_copy.Square = self.Square.copy()
    #                 board_copy.move_piece(move[0] * 8 + move[1])
    #                 if not board_copy.is_in_check(color):
    #                     return False
    #     return True
    
    # def is_in_stalemate(self, color):
    #     if self.is_in_check(color):
    #         return False
    #     for rank in range(8):
    #         for file in range(8):
    #             piece = self.Square[rank * 8 + file]
    #             if Piece.get_color(piece) != color:
    #                 continue
    #             moves = self.get_piece_moves(piece, rank, file)
    #             for move in moves:
    #                 board_copy = Board()
    #                 board_copy.Square = self.Square.copy()
    #                 board_copy.move_piece(move[0] * 8 + move[1])
    #                 if not board_copy.is_in_check(color):
    #                     return False
    #     return True
    
    # def is_draw(self):
    #     return self.is_in_stalemate(Piece.WHITE) or self.is_in_stalemate(Piece.BLACK) or self.is_in_checkmate(Piece.WHITE) or self.is_in_checkmate(Piece.BLACK)
    
    def clear_en_passant_square(self):
        self.en_passant_square = '-'
    
    def set_en_passant_square(self, square):
        self.en_passant_square = square
    
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
    
    def load_position_from_fen(fen):
        board = Board()
        parts = fen.split()
        piece_placement = parts[0]
        active_color = parts[1]
        castling_availability = parts[2]
        en_passant_square = parts[3]
        halfmove_clock = parts[4]
        fullmove_number = parts[5]


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
