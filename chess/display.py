import tkinter as tk
from tkinter import Canvas, PhotoImage
from pieces import Piece, convert_piece_to_string
from board import LoadPositionFromFen
import os
from PIL import Image, ImageTk

class ChessGUI:
    def __init__(self, master, board):
        self.master = master
        self.board = board
        self.image_path = "chess/imgs/"

        self.square_size = 100

        self.canvas = Canvas(master, width=800, height=800)
        self.canvas.pack()

        self.load_piece_images()
        self.draw_board()

    def load_piece_images(self):
        self.piece_images = {}

        color_table = {
            Piece.WHITE: 'w',
            Piece.BLACK: 'b'
        }

        valid_extensions = ('.png', '.jpg', '.jpeg', '.gif') 

        for piece_type in range(1, 7):
            for color in [Piece.WHITE, Piece.BLACK]:
                piece = Piece.create_piece(piece_type, color)
                piece_char = convert_piece_to_string(piece)
                image_name = color_table[Piece.get_color(piece)] + piece_char.lower()
                image_path = f"{self.image_path}{image_name}.png"
                if os.path.exists(image_path) and image_path.lower().endswith(valid_extensions):
                    image = Image.open(image_path)
                    image = image.resize((self.square_size, self.square_size))
                    # image = image.resize((self.square_size, self.square_size), Image.ANTIALIAS)
                    self.piece_images[piece] = ImageTk.PhotoImage(image)

        print("Keys in piece_images:", self.piece_images.keys())

    def draw_board(self):
        for rank in range(8):
            for file in range(8):
                x0, y0 = file * self.square_size, (7 - rank) * self.square_size
                x1, y1 = x0 + self.square_size, y0 + self.square_size

                color = "#FFFFFF" if (rank + file) % 2 == 0 else "green"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

                piece = self.board.Square[rank * 8 + file]
                if piece != Piece.NONE:
                    piece_type = Piece.get_piece_type(piece)
                    color = Piece.get_color(piece)
                    piece_key = Piece.create_piece(piece_type, color)
                    print("Generated piece_key:", piece_key)
                    image = self.piece_images[piece_key]
                    self.canvas.create_image(x0 + self.square_size/2, y0 + self.square_size/2, image=image)


starting_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
loaded_board = LoadPositionFromFen(starting_position)

root = tk.Tk()
root.title("Chess GUI")

chess_gui = ChessGUI(root, loaded_board)

root.mainloop()
