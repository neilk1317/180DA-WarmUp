import paho.mqtt.client as mqtt
import tkinter as tk
import os
from tkinter import *
from PIL import ImageTk, Image

b_width, b_height = 720, 720
square_size = 80
num_squares = 8
x_offset = 80
y_offset = 10

#Create Tkinter Window
window = tk.Tk()
window.title('Chess Test')
window.geometry('800x800')

#Load in the piece images which will be used to create image objects
image_dict = {}
piece_path = 'C:/Users/neilk/Documents/ECE180/Chess/Piece_Images'
for files in os.listdir(piece_path):
    name = files.split('.')[0]
    image_dict[name] = tk.PhotoImage(file=piece_path+'/'+files).subsample(10)

#Initialize grid that will store image objects
grid_dict = {}
chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
nums = ['1', '2', '3', '4', '5', '6', '7', '8']
for char in chars:
    for num in nums:
        grid_dict[char+num] = None

bg = tk.Canvas(window, width=b_width, height=b_height)
for x in range(x_offset, x_offset + square_size * (num_squares - 1) + 1, square_size):
    for y in range(y_offset, y_offset + square_size * (num_squares - 1) + 1, square_size):
        bg.create_rectangle(x, y, x + square_size, y + square_size)
        img = bg.create_image(x + (square_size / 2), y + (square_size / 2), image=image_dict['bishop_white'])


bg.place(x=0,y=0,anchor="nw")
window.mainloop()