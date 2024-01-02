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
        color_table = {
            Piece.WHITE: 'w',
            Piece.BLACK: 'b'
        }
        valid_extensions = ('.png', '.jpg', '.jpeg') 
        for piece_type in range(1, 7):
            for color in [Piece.WHITE, Piece.BLACK]:
                piece = Piece.create_piece(piece_type, color)
                piece_char = convert_piece_to_string(piece)
                image_name = color_table[Piece.get_color(piece)] + piece_char.lower()
                image_path = f"{self.image_path}{image_name}.png"
                if os.path.exists(image_path) and image_path.lower().endswith(valid_extensions):
                    image = Image.open(image_path)
                    image = image.resize((self.square_size, self.square_size))
                    self.piece_images[piece] = ImageTk.PhotoImage(image)

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
                    image = self.piece_images[piece_key]
                    self.canvas.create_image(x0 + self.square_size/2, y0 + self.square_size/2, image=image)

    # def on_square_clicked(self, event):
    #     file = event.x // self.square_size
    #     rank = 7 - event.y // self.square_size
    #     index = rank * 8 + file
    #     print(f"Clicked square index: {index}")
    #     if self.board.selected_piece is None:
    #         self.board.select_piece(index)
    #         if self.board.selected_piece is not None:
    #             self.selected_piece_image = self.canvas.create_image(event.x, event.y, image=self.piece_images[self.board.selected_piece[1]])
    #     else:
    #         target_square_index = rank * 8 + file
    #         piece_type = Piece.get_piece_type(self.board.selected_piece[1])
    #         valid_moves = self.board.get_valid_moves(self.board.current_turn)
    #         print(f"Valid moves for piece: {valid_moves[piece_type]}")
    #         if target_square_index in valid_moves[piece_type]:
    #             print(f"Moving piece from {self.board.selected_piece[0]} to {target_square_index}")
    #             self.board.move_piece(target_square_index)
    #             self.draw_board()
    #             print(self.board.get_fen())
    #         else:
    #             print("Invalid move.")
    #             self.board.deselect_piece()
    #             self.canvas.delete(self.selected_piece_image)
    #             self.selected_piece_image = None
    
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
            self.board.selected_piece = None
            self.selected_piece_image = None


    def on_piece_dragged(self, event):
        if self.selected_piece_image is not None:
            self.canvas.coords(self.selected_piece_image, event.x, event.y)

    def on_piece_dropped(self, event):
        if self.selected_piece_image is not None and self.board.selected_piece is not None:
            file = event.x // self.square_size
            rank = 7 - event.y // self.square_size
            target_square_index = rank * 8 + file
            selected_index, _ = self.board.selected_piece
            valid_moves = self.board.get_valid_moves(self.board.current_turn)

            # Check if the move is valid for the selected piece
            if selected_index in valid_moves and target_square_index in [r * 8 + f for r, f in valid_moves[selected_index]]:
                self.board.move_piece(target_square_index)
            else:
                print("Invalid move. Please try again.")

            self.canvas.delete(self.selected_piece_image)
            self.selected_piece_image = None
            self.board.selected_piece = None
            self.draw_board()


starting_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
# test = "8/8/8/3p3p/8/8/8/B7"
loaded_board = LoadPositionFromFen(starting_position)

root = tk.Tk()
root.title("Chess GUI")

chess_gui = ChessGUI(root, loaded_board)

root.mainloop()
