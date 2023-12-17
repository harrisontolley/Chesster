import tkinter as tk
from tkinter import Canvas, PhotoImage
from pieces import Piece, convert_piece_to_string
from board import LoadPositionFromFen
import os


print("Current working directory:", os.getcwd())


class ChessGUI:
    def __init__(self, master, board):
        self.master = master
        self.board = board
        self.image_path = "C:/Users/htoll/Desktop/Projects/Chesster/imgs/"

        self.canvas = Canvas(master, width=400, height=400)
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
                print("Constructed image path:", image_path)
                print("Image path:", image_path)
                print("File exists:", os.path.exists(image_path))
                print("Valid extension:", image_path.lower().endswith(valid_extensions))

                if os.path.exists(image_path) and image_path.lower().endswith(valid_extensions):
                    self.piece_images[piece] = PhotoImage(file=image_path)
        print("Keys in piece_images:", self.piece_images.keys())

    def draw_board(self):
        for rank in range(8):
            for file in range(8):
                x0, y0 = file * 50, (7 - rank) * 50
                x1, y1 = x0 + 50, y0 + 50

                color = "white" if (rank + file) % 2 == 0 else "black"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

                piece = self.board.Square[rank * 8 + file]
                if piece != Piece.NONE:
                    piece_type = Piece.get_piece_type(piece)
                    color = Piece.get_color(piece)
                    piece_key = Piece.create_piece(piece_type, color)
                    print("Generated piece_key:", piece_key)
                    image = self.piece_images[piece_key]
                    self.canvas.create_image(x0 + 25, y0 + 25, image=image)

import os

def list_files_in_directory(directory):
    try:
        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                print(f"File: {file_path}")
                print(f"Readable: {os.access(file_path, os.R_OK)}")
    except PermissionError:
        print(f"Permission denied for directory: {directory}")
    except FileNotFoundError:
        print(f"Directory not found: {directory}")

# Use the function
list_files_in_directory("C:/Users/htoll/Desktop/Projects/Chesster/imgs/")



# starting_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
# loaded_board = LoadPositionFromFen(starting_position)

# root = tk.Tk()
# root.title("Chess GUI")

# chess_gui = ChessGUI(root, loaded_board)

# root.mainloop()
