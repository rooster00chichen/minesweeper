import tkinter as tk
from gui import *
from control import *

if __name__ == "__main__":
    root = tk.Tk()
    window = GUI(root)
    # print(window.minemap_board)
    window.root.after(500, window.cheack_status)
    root.mainloop()
