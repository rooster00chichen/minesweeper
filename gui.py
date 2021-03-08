import tkinter as tk
import subprocess as sp
import numpy as np

MINE = -1
NONE = 0
RAISE_FLAG = 1
OPEN_BOARD = 2
EMPTY_BG_COLOR = "lightgray"
RAISE_BG_COLOR = "yellow"


class GUI:
    def __init__(self, root):
        self.root = root
        self.board_status = 0
        self.create_map()

    def create_map(self):
        self.create_map_date()
        self.create_map_view()

    def create_map_date(self, shape: (int, int) = (9, 9), mines: int = 10):
        self.set_board(shape)
        self.set_mines(mines)

    def set_board(self, shape: (int, int)):
        self.shape = shape
        self.size = np.prod(shape)
        self.minemap_board = np.zeros(shape, dtype=np.int8)
        self.world_board = np.zeros(shape, dtype=np.int8)

    def set_mines(self, mines):
        shape = self.shape
        self.mine = mines
        for ix in np.random.choice(range(self.size), mines):
            self.minemap_board[divmod(ix, shape[1])] = MINE

        for now_place in range(self.size):
            mine_count = 0
            x, y = divmod(now_place, shape[1])
            for dx in range(-1, 2, 1):
                for dy in range(-1, 2, 1):
                    if x+dx < 0 or x+dx >= shape[1] or y+dy < 0 or y+dy >= shape[0]:
                        continue
                    elif self.minemap_board[x+dx, y+dy] == MINE:
                        mine_count += 1

            if self.minemap_board[x, y] == MINE:
                self.minemap_board[x, y] = MINE
            else:
                self.minemap_board[x, y] = mine_count

    def create_map_view(self):
        for j in range(self.shape[0]):
            for i in range(self.shape[1]):
                # まずはテキストなしでラベルを作成
                label = tk.Label(
                    self.root,
                    width=2*5,
                    height=1*5,
                    bg=EMPTY_BG_COLOR,
                    relief=tk.RAISED,
                    font=(32)
                )
                label.num = 9*j+i
                # ラベルを配置
                label.grid(column=i, row=j)

                label.bind("<ButtonPress-1>", self.open_cell)
                label.bind("<ButtonPress-2>", self.raise_flag)

    def open_cell(self, e):
        now_label = e.widget
        x, y = divmod(now_label.num, self.shape[1])

        if self.world_board[x][y] == NONE:
            now_label.config(
                text=str(self.minemap_board[x][y]),
                relief=tk.SUNKEN,
                bg=EMPTY_BG_COLOR
            )
            self.world_board[x][y] = OPEN_BOARD
            if self.minemap_board[x][y] == MINE:
                self.board_status = 1
        else:
            return

    def raise_flag(self, e):
        now_label = e.widget
        x, y = divmod(now_label.num, self.shape[1])

        if self.world_board[x, y] == OPEN_BOARD:
            return
        elif self.world_board[x, y] == NONE:
            now_label.config(
                text="F",
                bg=RAISE_BG_COLOR
            )
            self.world_board[x, y] = RAISE_FLAG
        elif self.world_board[x, y] == RAISE_FLAG:
            now_label.config(
                text="",
                bg=EMPTY_BG_COLOR
            )
            self.world_board[x, y] = NONE

    def cheack_status(self):
        if self.board_status == 1:
            a = sp.run(
                ["osascript", "-e", 'display dialog "終了->キャンセル\nコンティニュー->OK"'])
            self.root.destroy()

        self.root.after(250, self.cheack_status)
