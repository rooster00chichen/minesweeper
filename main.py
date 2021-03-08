import tkinter as tk
from gui import *
from control import *

if __name__ == "__main__":
    root = tk.Tk()
    window = GUI(root)
    window.create_map()
    print(window.world_board)
