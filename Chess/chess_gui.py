import paho.mqtt.client as mqtt
import tkinter as tk
import numpy as np
import chess
import os
from tkinter import *

class Chess_Gui(tk.Canvas):
    
    def __init__(self, board:chess.Board, parent, b_width, b_height, *args, **kwargs):
        self.board = board

        tk.Canvas.__init__(self, parent, width=b_width, height = b_height, *args, **kwargs)
        self.parent = parent
        self.b_width, self.b_height = 720, 720
        self.square_size = 80
        self.num_squares = 8
        self.x_offset = 80
        self.y_offset = 10

        #Load in the piece images which will be used to create image objects
        self.image_dict = {}

        #self.piece_path = 'C:/Users/neilk/Documents/ECE180/Chess/Piece_Images'
        self.piece_path = 'D:/Documents/ECE-180DA/Lab 1/180DA-Warmup/Chess/Piece_Images'
        for files in os.listdir(self.piece_path):
            name = files.split('.')[0]
            self.image_dict[name] = tk.PhotoImage(file=self.piece_path+'/'+files).subsample(10)

        #Initialize grid that will store image objects
        self.grid_dict = {}
        self.letters = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        self.nums = np.array(['1', '2', '3', '4', '5', '6', '7', '8'])
        for letter in self.letters:
            for num in self.nums:
                self.grid_dict[letter+num] = None
        
        self.setup_board()

    def grid_location(self, letter:str, num:str):
        """
        Extracts the NW Canvas location of the specified square by the letter and number

        letter: Letter of the chess board column
        num: Number of the chess board row
        """
        char_offset = np.where(self.letters == letter)[0][0]
        num_offset = np.where(self.nums == num)[0][0]
        x = self.x_offset + char_offset * self.square_size
        y = self.y_offset + (self.num_squares-num_offset-1) * self.square_size

        #returns NW position of square
        return x,y

    def place_image(self, letter:str, num:str, img_name:str):
        """
        Places a new image at the specified square by the letter and number. Any existing image is overwritten.

        letter: Letter of the chess board column
        num: Number of the chess board row
        """
        x,y = self.grid_location(letter, num)
        img = self.create_image(x + (self.square_size / 2), y + (self.square_size / 2), image=self.image_dict[img_name])

        #Overwrites any existing image
        existing_img = self.grid_dict[letter+num]
        if existing_img is not None:
            self.delete(existing_img)
        self.grid_dict[letter+num] = img
    
    def symbol_to_img_name(self, symbol:str):
        """
        Helper function to convert python-chess symbol to image name used for displaying

        symbol: Symbol of the piece 
        """
        if symbol.isupper():
            my_color = 'white'
        else:
            my_color = 'black'
        
        idx = chess.PIECE_SYMBOLS.index(symbol.lower())
        piece_name = chess.PIECE_NAMES[idx]
        img_name = piece_name + "_" + my_color
        return img_name

    def board_to_img(self, board:chess.Board):
        """
        Parses the board object and updates the display based on the current locations of pieces
        Call this function after a move has been pushed to the board.

        board: chess.Board object to be used to generate the display. 
        """
        board_dict = board.piece_map()
        for key in range(64):
            if key in board_dict.keys():
                val = board_dict[key]
                key = chess.square_name(key)    #Converts to letter+num format
                letter = key[0]
                num = key[1]

                val = val.symbol()              #Gets character of symbol
                img_name = self.symbol_to_img_name(val)

                self.place_image(letter, num, img_name)
            else:
                key = chess.square_name(key)
                existing_img = self.grid_dict[key]
                if existing_img is not None:
                    self.delete(existing_img)

    def move_image(self, start_letter:str, start_num:str, end_letter:str, end_num:str):
        """
        Moves the image from the starting square to the ending square. Overwrites any existing image at end square.

        start_letter: Letter of the starting chess board column
        start_num: Number of the starting chess board row
        end_letter: Letter of the ending chess board column
        end_num: Number of the ending chess board row
        """

        start_x,start_y = self.grid_location(start_letter, start_num)
        end_x, end_y = self.grid_location(end_letter, end_num)

        start_img = self.grid_dict[start_letter+start_num]
        existing_img = self.grid_dict[end_letter+end_num]

        #Check that the start square has an image and then overwrite any existing end square image
        if start_img is not None:
            if existing_img is not None:
                self.delete(existing_img)
            #Updates the grid dict and moves the image
            self.grid_dict[start_letter+start_num] = None
            self.grid_dict[end_letter+end_num] = start_img
            self.move(start_img, end_x - start_x, end_y - start_y)

    def setup_board(self):
        """
        Setups the intiail board by drawing the grid and creating the initial piece images
        """
    
        #Draw board grid
        for x in range(self.x_offset, self.x_offset + self.square_size * (self.num_squares - 1) + 1, self.square_size):
            for y in range(self.y_offset, self.y_offset + self.square_size * (self.num_squares - 1) + 1, self.square_size):
                self.create_rectangle(x, y, x + self.square_size, y + self.square_size)
        
        #Place starting pieces
        for letter in self.letters:
            for num in ['1', '2', '7', '8']:
                if num == '1':
                    if letter in ['a','h']:
                        self.place_image(letter, num, 'rook_white')
                    elif letter in ['b','g']:
                        self.place_image(letter, num, 'knight_white')
                    elif letter in ['c','f']:
                        self.place_image(letter, num, 'bishop_white')
                    elif letter == 'd':
                        self.place_image(letter, num, 'queen_white')
                    else:
                        self.place_image(letter, num, 'king_white')
                elif num == '2':
                    self.place_image(letter, num, 'pawn_white')
                elif num == '7':
                    self.place_image(letter, num, 'pawn_black')
                else:
                    if letter in ['a','h']:
                        self.place_image(letter, num, 'rook_black')
                    elif letter in ['b','g']:
                        self.place_image(letter, num, 'knight_black')
                    elif letter in ['c','f']:
                        self.place_image(letter, num, 'bishop_black')
                    elif letter == 'd':
                        self.place_image(letter, num, 'queen_black')
                    else:
                        self.place_image(letter, num, 'king_black') 

# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ece180d/central")

# The callback of the client when it disconnects.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

# The default message callback.
# (won't be used if only publishing, but can still exist)
def on_message(client, userdata, message):
    gui = userdata['gui']
    board = userdata['board']
    if(message.topic == "ece180d/central"):
        results = str(message.payload.decode())
        start_letter = results[0]
        start_num = results[1]
        end_letter = results[2]
        end_num = results[3]
        
        start_square = chess.parse_square(start_letter+start_num)
        end_square = chess.parse_square(end_letter+end_num)
        move = board.find_move(start_square, end_square)
        board.push(move)

        gui.board_to_img(board)
        #gui.move_image(start_letter,  start_num, end_letter, end_num)



if __name__ == "__main__":
    #Create Tkinter Window
    board = chess.Board()
    window = tk.Tk()
    window.title('Chess Test')
    window.geometry('800x800')
    gui = Chess_Gui(board,window, 720, 720)
    gui.place(x=0,y=0,anchor="nw")

    client_userdata = {'gui':gui, 'board':board}
    client = mqtt.Client(userdata=client_userdata)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.connect_async('mqtt.eclipseprojects.io')
    client.loop_start()
    window.mainloop()
    client.loop_stop()
