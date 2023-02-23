import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

window = tk.Tk()
window.title('Chess Test')
window.geometry('800x800')

bg = tk.Canvas(window, width=720, height=720)

for x in range(80,641, 80):
    for y in range(10, 571, 80):
        bg.create_rectangle(x, y, x+80, y+80)

bg.place(x=0,y=0,anchor="nw")

# img = (Image.open('chessboard_blank.png'))
# img = img.resize((700,700), Image.ANTIALIAS)
# img = ImageTk.PhotoImage(img)
# background = tk.Label(window, image=img, bd=0)
# background.place(x=0,y=0, anchor="nw")

window.mainloop()