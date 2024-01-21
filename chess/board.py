""" board.py:
This module contains the Board class, which represents the chess board.
"""
from pieces import Piece, convert_piece_to_string
from move import Move
from coordinates import Coordinates

class Board:
    # Tiles are the traditional chess tiles, indexed from a1 to h8
    # Squares are the indices of the board array, indexed from 0 to 63
    # Coordinates are a traditional coordinate system, indexed from (0, 0) to (7, 7) -> (file, rank) or (x, y) - The same as a cartesian plane

    def __init__(self):
        self.current_turn = Piece.WHITE
        self.en_passant_square = '-'
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.castling_availability = 'KQkq'

        self.Square = [0] * 64
    
    @staticmethod
    def convert_tile_to_index(square: str) -> int:
        file = ord(square[0]) - ord('a')
        rank = int(square[1]) - 1
        return rank * 8 + file

    @staticmethod
    def convert_index_to_tile(index: int) -> str:
        file = chr((index % 8) + ord('a'))
        rank = index // 8 + 1
        return f"{file}{rank}"
    
    @staticmethod
    def convert_index_to_coordinates(index: int) -> Coordinates:
        file = index % 8
        rank = index // 8
        return Coordinates(file, rank)
    
    def __str__(self):
        board_str = ""
        for rank in range(7, -1, -1):  # Start from the bottom rank
            for file in range(8):
                piece = self.Square[rank * 8 + file]
                board_str += convert_piece_to_string(piece)
            board_str += "\n"
        return board_str

    def move_piece(self, move: Move):
            # Move the piece
            current_index = move.get_current_coordinates().get_board_index()
            destination_index = move.get_destination_coordinates().get_board_index()

            self.Square[current_index] = Piece.NONE
            self.Square[destination_index] = move.get_piece()

            self.switch_turn()

    def move_is_legal(self, move: Move) -> bool:
        # return True # ! DELETE WHEN IMPL.

        all_possible_moves = self.get_all_possible_moves(self.get_current_turn())
        if move in all_possible_moves:
            return True
        else:
            return False


    def get_all_pieces_of_color(self, color) -> [(Piece, int)]:
        pieces = []
        for idx, piece in enumerate(self.Square):
            if piece != Piece.NONE and Piece.get_color(piece) == color:
                pieces.append((piece, idx))

        return pieces


    def get_all_possible_moves(self, color):
        moves = {}
        piece_idx_array = self.get_all_pieces_of_color(color)

        for piece_idx in piece_idx_array:
            piece = piece_idx[0]
            idx = piece_idx[1]

            current_coords = Coordinates(idx % 8, idx // 8)
            
            piece_moves = self.get_piece_moves(piece, current_coords)

            moves.update(piece_moves)
        
        return moves


    def switch_turn(self):
        self.current_turn = Piece.BLACK if self.current_turn == Piece.WHITE else Piece.WHITE


    def get_piece_moves(self, piece, current_coords: Coordinates):
        piece_type = Piece.get_piece_type(piece)
        if piece_type == Piece.PAWN:
            return self.get_pawn_moves(piece, current_coords)
        elif piece_type == Piece.KNIGHT:
            return self.get_knight_moves(piece, current_coords)
        elif piece_type == Piece.BISHOP:
            return self.get_bishop_moves(piece, current_coords)
        elif piece_type == Piece.ROOK:
            return self.get_rook_moves(piece, current_coords)
        elif piece_type == Piece.QUEEN:
            return self.get_queen_moves(piece, current_coords)
        elif piece_type == Piece.KING:
            return self.get_king_moves(piece, current_coords)
        return []


    def get_pawn_moves(self, piece, current_coords: Coordinates):
        moves = {}
        color = Piece.get_color(piece)

        # Direction pawns can move (1 for white, -1 for black)
        direction = -1 if color == Piece.BLACK else 1

        # Forward move
        pushed_coords = Coordinates(current_coords.get_file(), current_coords.get_rank() + direction)
        if 0 <= pushed_coords.get_rank() < 8:

            if self.Square[pushed_coords.get_board_index()] == Piece.NONE:
                single_push = Move(piece, current_coords, pushed_coords)
                moves[single_push] = single_push

                # Double move from starting position
                starting_rank = 1 if color == Piece.WHITE else 6

                if current_coords.get_rank() == starting_rank:

                    double_pushed_coords = Coordinates(current_coords.get_file(), current_coords.get_rank() + 2 * direction)

                    if self.Square[double_pushed_coords.get_board_index()] == Piece.NONE:
                        double_push = Move(piece, current_coords, double_pushed_coords)
                        en_passant_move = Move(piece, current_coords, double_pushed_coords, can_en_passant=True)
                        moves[double_push] = en_passant_move

        # Captures
        for offset in [-1, 1]:
            capture_coords = Coordinates(current_coords.get_file() + offset, current_coords.get_rank() + direction)

            capture_file = capture_coords.get_file()
            capture_rank = capture_coords.get_rank()

            if 0 <= capture_file < 8 and 0 <= capture_rank < 8:
                capture_index = capture_coords.get_board_index()

                if self.Square[capture_index] != Piece.NONE and Piece.get_color(self.Square[capture_index]) != color:
                    taken_piece_coords = Coordinates(capture_file, capture_rank)

                    capture_move = Move(piece, current_coords, taken_piece_coords)
                    moves[capture_move] = capture_move

        # En passant
        if self.en_passant_square != '-':
            en_passant_index = self.convert_tile_to_index(self.get_en_passant_tile())

            en_passant_coordinates = self.convert_index_to_coordinates(en_passant_index)

            for offset in [-1, 1]:
                taking_coordinates = Coordinates(current_coords.get_file() + offset, current_coords.get_rank() + direction) # doesn't need bounds checking as irrelevant here
                if taking_coordinates == en_passant_coordinates:
                    pawn_capture = Move(piece, current_coords, taking_coordinates)
                    en_passant_capture = Move(piece, current_coords, en_passant_coordinates, is_en_passant=True)

                    moves[pawn_capture] = en_passant_capture
                    break

        return moves


    def get_knight_moves(self, piece, current_coords: Coordinates):
        moves = {}
        color = Piece.get_color(piece)
        
        current_rank = current_coords.get_rank()
        current_file = current_coords.get_file()
        
        for y_offset in range(-2, 3):
            for x_offset in range(-2, 3):
                if abs(x_offset) + abs(y_offset) == 3:
                    if current_rank + y_offset in range(8) and current_file + x_offset in range(8):

                        destination_coords = Coordinates(current_file + x_offset, current_rank + y_offset)

                        if self.Square[destination_coords.get_board_index()] == Piece.NONE or Piece.get_color(self.Square[destination_coords.get_board_index()]) != color:
                            knight_move = Move(piece, current_coords, destination_coords)
                            moves[knight_move] = knight_move

        return moves


    def get_bishop_moves(self, piece, current_coords):
        moves = {}
        color = Piece.get_color(piece)
        
        current_file = current_coords.get_file()
        current_rank = current_coords.get_rank()

        for NE_offset in range(1, 8):
            if current_rank + NE_offset in range(8) and current_file + NE_offset in range(8):
                destination_coords = Coordinates(current_file + NE_offset, current_rank + NE_offset)

                if self.Square[destination_coords.get_board_index()] == Piece.NONE:
                    bishop_move = Move(piece, current_coords, destination_coords)
                    moves[bishop_move] = bishop_move
                elif Piece.get_color(self.Square[destination_coords.get_board_index()]) != color:
                    bishop_move = Move(piece, current_coords, destination_coords)
                    moves[bishop_move] = bishop_move                    
                    break
                else:
                    break
        for SE_offset in range(1, 8):
            if current_rank - SE_offset in range(8) and current_file + SE_offset in range(8):
                destination_coords = Coordinates(current_file + SE_offset, current_rank - SE_offset)

                if self.Square[destination_coords.get_board_index()] == Piece.NONE:
                    bishop_move = Move(piece, current_coords, destination_coords)
                    moves[bishop_move] = bishop_move                    
                elif Piece.get_color(self.Square[destination_coords.get_board_index()]) != color:
                    bishop_move = Move(piece, current_coords, destination_coords)
                    moves[bishop_move] = bishop_move
                    break
                else:
                    break
        for NW_offset in range(1, 8):
            if current_rank + NW_offset in range(8) and current_file - NW_offset in range(8):
                destination_coords = Coordinates(current_file - NW_offset, current_rank + NW_offset)

                if self.Square[destination_coords.get_board_index()] == Piece.NONE:
                    bishop_move = Move(piece, current_coords, destination_coords)
                    moves[bishop_move] = bishop_move
                elif Piece.get_color(self.Square[destination_coords.get_board_index()]) != color:
                    bishop_move = Move(piece, current_coords, destination_coords)
                    moves[bishop_move] = bishop_move
                    break
                else:
                    break
        for SW_offset in range(1, 8):
            if current_rank - SW_offset in range(8) and current_file - SW_offset in range(8):
                destination_coords = Coordinates(current_file - SW_offset, current_rank - SW_offset)
                
                if self.Square[destination_coords.get_board_index()] == Piece.NONE:
                    bishop_move = Move(piece, current_coords, destination_coords)
                    moves[bishop_move] = bishop_move
                elif Piece.get_color(self.Square[destination_coords.get_board_index()]) != color:
                    bishop_move = Move(piece, current_coords, destination_coords)
                    moves[bishop_move] = bishop_move
                    break
                else:
                    break
        return moves


    def get_rook_moves(self, piece, current_coords: Coordinates):
        moves = {}
        color = Piece.get_color(piece)

        current_file = current_coords.get_file()
        current_rank = current_coords.get_rank()

        for north in range(1, 8):
            if current_rank + north in range(8):
                destination_coords = Coordinates(current_file, current_rank + north)

                if self.Square[destination_coords.get_board_index()] == Piece.NONE:
                    rook_move = Move(piece, current_coords, destination_coords)
                    moves[rook_move] = rook_move
                elif Piece.get_color(self.Square[destination_coords.get_board_index()]) != color:
                    rook_move = Move(piece, current_coords, destination_coords)
                    moves[rook_move] = rook_move
                    break
                else:
                    break
        for south in range(1, 8):
            if current_rank - south in range(8):
                destination_coords = Coordinates(current_file, current_rank - south)

                if self.Square[destination_coords.get_board_index()] == Piece.NONE:
                    rook_move = Move(piece, current_coords, destination_coords)
                    moves[rook_move] = rook_move
                elif Piece.get_color(self.Square[destination_coords.get_board_index()]) != color:
                    rook_move = Move(piece, current_coords, destination_coords)
                    moves[rook_move] = rook_move
                    break
                else:
                    break
        for east in range(1, 8):
            if current_file + east in range(8):
                destination_coords = Coordinates(current_file + east, current_rank)

                if self.Square[destination_coords.get_board_index()] == Piece.NONE:
                    rook_move = Move(piece, current_coords, destination_coords)
                    moves[rook_move] = rook_move
                elif Piece.get_color(self.Square[destination_coords.get_board_index()]) != color:
                    rook_move = Move(piece, current_coords, destination_coords)
                    moves[rook_move] = rook_move
                    break
                else:
                    break
        for west in range(1, 8):
            if current_file - west in range(8):
                destination_coords = Coordinates(current_file - west, current_rank)

                if self.Square[destination_coords.get_board_index()] == Piece.NONE:
                    rook_move = Move(piece, current_coords, destination_coords)
                    moves[rook_move] = rook_move
                elif Piece.get_color(self.Square[destination_coords.get_board_index()]) != color:
                    rook_move = Move(piece, current_coords, destination_coords)
                    moves[rook_move] = rook_move
                    break
                else:
                    break
        return moves


    def get_queen_moves(self, piece, current_coords: Coordinates):
        moves = {}
        moves.update(self.get_bishop_moves(piece, current_coords))
        moves.update(self.get_rook_moves(piece, current_coords))
        return moves
    
    def get_king_moves(self, piece, current_coords: Coordinates):
        moves = {}
        color = Piece.get_color(piece)

        current_file = current_coords.get_file()
        current_rank = current_coords.get_rank()

        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                if current_rank + y_offset in range(8) and current_file + x_offset in range(8):
                    destination_coords = Coordinates(current_file + x_offset, current_rank + y_offset)

                    if self.Square[destination_coords.get_board_index()] == Piece.NONE or Piece.get_color(self.Square[destination_coords.get_board_index()]) != color:
                        king_move = Move(piece, current_coords, destination_coords)
                        moves[king_move] = king_move
        
        if self.can_castle_king_side(color):
            if self.Square[current_coords.get_board_index() + 1] == Piece.NONE and self.Square[current_coords.get_board_index() + 2] == Piece.NONE:
                king_move = Move(piece, current_coords, Coordinates(current_file + 2, current_rank))
                king_side_castle = Move(piece, current_coords, Coordinates(current_file + 2, current_rank), is_castling=True)
                moves[king_move] = king_side_castle
        
        if self.can_castle_queen_side(color):
            if self.Square[current_coords.get_board_index() - 1] == Piece.NONE and self.Square[current_coords.get_board_index() - 2] == Piece.NONE and self.Square[current_coords.get_board_index() - 3] == Piece.NONE:
                king_move = Move(piece, current_coords, Coordinates(current_file - 2, current_rank))
                queen_side_castle = Move(piece, current_coords, Coordinates(current_file - 2, current_rank), is_castling=True)
                moves[king_move] = queen_side_castle

        return moves

    def clear_en_passant_square(self):
        self.en_passant_square = '-'
    
    def set_en_passant_square(self, idx):
        if idx is not None:
            self.en_passant_square = Board.convert_index_to_tile(idx)
        else:
            self.en_passant_square = '-'

    
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


    def load_position_from_fen(fen: str):
        board = Board()
        parts = fen.split()
        piece_placement = parts[0]
        active_color = parts[1]
        castling_availability = parts[2]
        en_passant_square = parts[3]
        halfmove_clock = parts[4]
        fullmove_number = parts[5]

        board.castling_availability = castling_availability
        board.en_passant_square = en_passant_square
        board.halfmove_clock = halfmove_clock
        board.fullmove_number = fullmove_number

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

    def get_en_passant_tile(self) -> str:
        return self.en_passant_square
    
    def get_current_turn(self) -> int:
        return self.current_turn

    def can_castle_king_side(self, color) -> bool:
        if color == Piece.WHITE:
            return 'K' in self.castling_availability
        else:
            return 'k' in self.castling_availability
    
    def can_castle_queen_side(self, color) -> bool:
        if color == Piece.WHITE:
            return 'Q' in self.castling_availability
        else:
            return 'q' in self.castling_availability
    
    def remove_castle_rights(self, color):
        if color == Piece.WHITE:
            self.castling_availability = self.castling_availability.replace('K', '')
            self.castling_availability = self.castling_availability.replace('Q', '')
        else:
            self.castling_availability = self.castling_availability.replace('k', '')
            self.castling_availability = self.castling_availability.replace('q', '')

    def take_en_passant(self, move: Move):
        if move.get_is_en_passant() and move.taken_piece_idx is not None:
            print("TAKING EN PASSANT")
            print(move.get_taken_piece_idx())
            print(Board.convert_index_to_coordinates(move.get_taken_piece_idx()))
            self.Square[move.get_taken_piece_idx()] = Piece.NONE