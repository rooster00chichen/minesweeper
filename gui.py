import tkinter as tk
from typing import Sequence
import numpy as np

MINE = -1


class GUI:
    def __init__(self, root):
        pass

    def create_map(self, shape: (int, int) = (9, 9), mines: int = 10):
        self.set_board(shape)
        self.set_mines(mines)

    def set_board(self, shape: (int, int)):
        self.shape = shape
        self.size = np.prod(shape)
        self.setup_board = np.zeros(shape, dtype=np.int8)
        self.world_board = np.zeros(shape, dtype=np.int8)

    def set_mines(self, mines):
        shape = self.shape
        self.mine = mines
        for ix in np.random.choice(range(self.size), mines):
            self.setup_board[divmod(ix, shape[1])] = MINE

        for now_place in range(self.size):
            mine_count = 0
            x, y = divmod(now_place, shape[1])
            for dx in range(-1, 2, 1):
                for dy in range(-1, 2, 1):
                    if x+dx < 0 or x+dx >= shape[1] or y+dy < 0 or y+dy >= shape[0]:
                        continue
                    elif self.setup_board[x+dx, y+dy] == -1:
                        mine_count += 1

            if self.setup_board[x, y] == -1:
                self.setup_board[x, y] = -1
            else:
                self.setup_board[x, y] = mine_count

        self.world_board = self.setup_board
