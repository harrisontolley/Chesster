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
        # self.canvas.bind("<Button-1>", self.on_square_clicked)
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
                square_index = self.board.convert_file_rank_to_index(file, rank)
                square_label = Board.index_to_square(square_index)

                # Draw the square label
                label_color = 'black'
                # if (rank + file) % 2 == 0 else 'white'
                self.canvas.create_text(x0 + 10, y1 - 10, text=square_label, fill=label_color)

                # Draw the piece image
                piece = self.board.Square[square_index]
                if piece != Piece.NONE:
                    piece_type = Piece.get_piece_type(piece)
                    color = Piece.get_color(piece)
                    piece_key = Piece.create_piece(piece_type, color)
                    image = self.piece_images[piece_key]
                    self.canvas.create_image(x0 + self.square_size/2, y0 + self.square_size/2, image=image)


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
        # print(f"Clicked square: {index} {self.board.index_to_square[index]} {(file, rank)}")


    def on_piece_dragged(self, event):
        if self.selected_piece_image is not None:
            self.canvas.coords(self.selected_piece_image, event.x, event.y)


    def on_piece_dropped(self, event):
            if self.selected_piece_image is not None and self.board.selected_piece is not None:
                selected_index, piece = self.board.selected_piece

                current_square = (selected_index % 8, selected_index // 8)
                destination_square = (event.x // self.square_size, 7 - event.y // self.square_size)

                move = Move(piece, current_square, destination_square)
                self.board.move_piece(move)

                # Redraw the board and reset the selected piece
                self.canvas.delete(self.selected_piece_image)
                self.selected_piece_image = None
                self.board.selected_piece = None
                self.draw_board()

starting_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# test = "8/8/8/3p2pp/8/8/8/B7  w KQkq - 0 1"
loaded_board = Board.load_position_from_fen(starting_position)

root = tk.Tk()
root.title("Chesster")

chess_gui = ChessGUI(root, loaded_board)

root.mainloop()
