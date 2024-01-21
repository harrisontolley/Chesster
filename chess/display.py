"""display.py:
File containing the ChessGUI class, which is used to display and manage the chess board state.
"""
import tkinter as tk
from tkinter import Canvas
from pieces import Piece, convert_piece_to_string
from board import Board
import os
from PIL import Image, ImageTk
from move import Move
from coordinates import Coordinates

class ChessGUI:
    def __init__(self, master, board):
        self.master = master
        self.board = board
        self.image_path = "imgs/"
        self.square_size = 75
        self.canvas = Canvas(master, 
                             width=(400 * (self.square_size / 50)), 
                             height=(400 * (self.square_size / 50)))
        self.canvas.pack()
        self.selected_piece_image = None
        self.load_piece_images()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_piece_clicked)
        self.canvas.bind("<B1-Motion>", self.on_piece_dragged)
        self.canvas.bind("<ButtonRelease-1>", self.on_piece_dropped)

    def load_piece_images(self):
        self.piece_images = {}
        color_table = {Piece.WHITE: 'w', Piece.BLACK: 'b'}
        for piece_type in range(1, 7):
            for color in [Piece.WHITE, Piece.BLACK]:
                piece = Piece.create_piece(piece_type, color)
                piece_char = convert_piece_to_string(piece)
                image_name = f"{color_table[color]}{piece_char.lower()}.png"
                image_path = os.path.join(self.image_path, image_name)
                if os.path.exists(image_path):
                    self.piece_images[piece] = ImageTk.PhotoImage(
                        Image.open(image_path).resize((self.square_size, self.square_size)))

    def draw_board(self):
        for rank in range(8):
            for file in range(8):
                x0, y0 = file * self.square_size, (7 - rank) * self.square_size
                x1, y1 = x0 + self.square_size, y0 + self.square_size
                color = "#b4afa5" if (rank + file) % 2 == 1 else "#a17b37"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

                # Get the square label
                coordinates = Coordinates(file, rank)
                square_index = coordinates.get_board_index()
                square_label = Board.convert_index_to_tile(square_index)

                # Draw the square label
                self.canvas.create_text(x0 + 10, y1 - 10, text=square_label, fill='black')

                # Draw the piece image
                piece = self.board.Square[square_index]
                if piece != Piece.NONE:
                    piece_type = Piece.get_piece_type(piece)
                    color = Piece.get_color(piece)
                    piece_key = Piece.create_piece(piece_type, color)
                    image = self.piece_images[piece_key]
                    self.canvas.create_image(x0 + self.square_size/2, y0 + self.square_size/2, image=image)

        # print("EN PASSANT SQUARE", self.get_board().get_en_passant_tile())

    def on_piece_clicked(self, event):
        file = event.x // self.square_size
        rank = 7 - event.y // self.square_size
        index = rank * 8 + file
        piece = self.board.Square[index]

        # Check if the piece belongs to the player whose turn it is
        if piece != Piece.NONE and Piece.get_color(piece) == self.board.current_turn:
            self.board.selected_piece = (index, piece)
            self.selected_piece_image = self.canvas.create_image(event.x, event.y, image=self.piece_images[piece])
        else:
            # If the piece does not belong to the current player, do not select it
            self.selected_piece_image = None
            return
        # print(f"Clicked square: {index} {(file, rank)}") # {self.get_board().index_to_square[index]} 


    def on_piece_dragged(self, event):
        if self.selected_piece_image is not None:
            self.canvas.coords(self.selected_piece_image, event.x, event.y)

    def on_piece_dropped(self, event):
            if self.selected_piece_image is not None and self.board.selected_piece is not None:
                selected_index, piece = self.board.selected_piece

                current_square = Coordinates(selected_index % 8, selected_index // 8)
                destination_square = Coordinates(event.x // self.square_size, 7 - event.y // self.square_size)

                default_move = Move(piece, current_square, destination_square)

                legal_moves = self.board.get_all_possible_moves(self.board.get_current_turn())

                if default_move in legal_moves:

                    special_move = legal_moves[default_move]

                    self.get_board().move_piece(special_move)

                    # Handle removing the piece that was captured by en passant
                    if special_move.get_is_en_passant():
                        self.get_board().take_en_passant(special_move)

                    # Check if the move was can be captured en passant
                    if special_move.get_can_en_passant():
                        en_passant_idx = special_move.get_en_passant_idx()
                        if en_passant_idx is not None:
                            self.get_board().set_en_passant_square(en_passant_idx)
                    else:
                        self.get_board().clear_en_passant_square()
                    
                    # Handle promotion
                    if special_move.get_is_promotion():
                        # prompt user for promotion piece type
                        color = Piece.get_color(piece)
                        chosen_piece = self.show_promotion_options(color)

                        # set the promotion piece
                        special_move.set_promotion_piece(chosen_piece)

                        self.get_board().promote_piece(special_move)

                    # Redraw the board and reset the selected piece
                    self.canvas.delete(self.selected_piece_image)

                else:
                    self.canvas.coords(self.selected_piece_image, event.x, event.y)

                self.selected_piece_image = None
                self.board.selected_piece = None
                self.draw_board() # redraw board after move

    def get_board(self) -> Board:
        return self.board
    
    def show_promotion_options(self, color):
        chosen_piece = None
        while chosen_piece is None:
            popup = tk.Toplevel(self.master)
            popup.title("Pawn Promotion")
            popup.geometry("200x100")
            popup.grab_set()  # Makes the popup window modal

            button_frame = tk.Frame(popup)
            button_frame.pack(expand=True, fill="both")

            def on_promotion_choice(piece_type):
                nonlocal chosen_piece  # Refer to the outer variable
                chosen_piece = Piece.create_piece(piece_type, color)
                popup.destroy()

            # Buttons for each promotion option
            buttons = {
                Piece.QUEEN: tk.Button(button_frame, text="Queen", command=lambda: on_promotion_choice(Piece.QUEEN)),
                Piece.ROOK: tk.Button(button_frame, text="Rook", command=lambda: on_promotion_choice(Piece.ROOK)),
                Piece.BISHOP: tk.Button(button_frame, text="Bishop", command=lambda: on_promotion_choice(Piece.BISHOP)),
                Piece.KNIGHT: tk.Button(button_frame, text="Knight", command=lambda: on_promotion_choice(Piece.KNIGHT))
            }

            # Arrange buttons in the popup
            for piece_type, button in buttons.items():
                button.pack(side="left", expand=True)

            self.master.wait_window(popup)  # Wait for the user to make a choice

        return chosen_piece

    def on_promotion_choice(self, piece_type, color):
        self.promotion_choice = Piece.create_piece(piece_type, color)

starting_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# test = "8/8/8/3p2pp/8/8/8/B7  w KQkq - 0 1"
loaded_board = Board.load_position_from_fen(starting_position)

root = tk.Tk()
root.title("Chesster")

chess_gui = ChessGUI(root, loaded_board)

root.mainloop()
