import tkinter as tk
import subprocess as sp
import numpy as np
from tkinter import messagebox

from numpy.core.fromnumeric import shape

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
        self.open_status = 0
        shape_one = int(input("マインスイーパの正方形の一辺を設定："))
        if shape_one == 0:
            shape = (9, 9)
        else:
            shape = (shape_one, shape_one)
        mines = int(input("マインスイーパの爆弾を設定："))
        if mines == 0:
            mines = 9
        self.create_map(shape, mines)

    def create_map(self, shape: (int, int), mines: int):
        self.create_map_date(shape, mines)
        self.create_map_view()

    def create_map_date(self, shape: (int, int), mines: int):
        self.set_board(shape)
        self.set_mines(mines)

        print(self.minemap_board)

    def set_board(self, shape: (int, int)):
        self.shape = shape
        self.size = np.prod(shape)
        self.minemap_board = np.zeros(shape, dtype=np.int8)
        self.world_board = np.zeros(shape, dtype=np.int8)

    def set_mines(self, mines):
        shape = self.shape
        self.mine = mines
        for ix in np.random.choice(range(self.size), mines, replace=False):
            self.minemap_board[divmod(ix, shape[1])] = MINE

        for now_place in range(self.size):
            mine_count = 0
            x, y = divmod(now_place, shape[1])
            if self.minemap_board[x, y] == MINE:
                continue
            else:
                for dx in range(-1, 2, 1):
                    for dy in range(-1, 2, 1):
                        if x+dx < 0 or x+dx >= shape[1] or y+dy < 0 or y+dy >= shape[0]:
                            continue
                        elif self.minemap_board[x+dx, y+dy] == MINE:
                            mine_count += 1
                self.minemap_board[x, y] = mine_count

    def create_map_view(self):
        self.labels = [None]*self.size
        big_size = 45//self.shape[1]
        if big_size == 0:
            big_size = 1
        for j in range(self.shape[0]):
            for i in range(self.shape[1]):
                # まずはテキストなしでラベルを作成
                label = tk.Label(
                    self.root,
                    width=2*big_size,
                    height=1*big_size,
                    bg=EMPTY_BG_COLOR,
                    relief=tk.RAISED,
                    font=(32)
                )
                label.num = self.shape[1]*j+i
                # ラベルを配置
                label.grid(column=i, row=j)
                # 諸々の都合より１次元配列
                self.labels[label.num] = label
                label.bind("<ButtonPress-1>", self.open_cell)
                label.bind("<ButtonPress-2>", self.raise_flag)

    def open_cell(self, e):
        now_label = e.widget
        x, y = divmod(now_label.num, self.shape[1])
        # 最初に触ったマスが0（空）以外だったらそれを強制的に0に変更
        if self.open_status == 0:
            while True:
                if self.minemap_board[x][y] == NONE:
                    break
                else:
                    self.create_map_date(self.shape, self.mine)
        else:
            pass

        if self.world_board[x][y] == NONE:
            if self.minemap_board[x][y] != 0:
                now_label.config(
                    text=str(self.minemap_board[x][y]),
                    relief=tk.SUNKEN,
                    bg=EMPTY_BG_COLOR
                )
                self.world_board[x][y] = OPEN_BOARD
                if self.minemap_board[x][y] == MINE:
                    self.board_status = 1
                self.open_status += 1
            elif self.minemap_board[x][y] == 0:
                search_list = np.zeros(self.shape, dtype=np.int8)
                self.search_board(0, (x, y), search_list)
        elif self.world_board[x][y] == OPEN_BOARD:
            mine_count = 0
            shape = self.shape
            for dx in range(-1, 2, 1):
                for dy in range(-1, 2, 1):
                    if x+dx < 0 or x+dx >= shape[1] or y+dy < 0 or y+dy >= shape[0]:
                        continue
                    elif self.world_board[x+dx, y+dy] == RAISE_FLAG:
                        mine_count += 1
            if mine_count == self.minemap_board[x][y]:
                for dx in range(-1, 2, 1):
                    for dy in range(-1, 2, 1):
                        if x+dx < 0 or x+dx >= shape[1] or y+dy < 0 or y+dy >= shape[0]:
                            continue
                        else:
                            if self.world_board[x+dx][y+dy] == NONE:
                                if self.minemap_board[x+dx][y+dy] != 0:
                                    num = (x+dx)*self.shape[1]+(y+dy)
                                    self.labels[num].config(
                                        text=str(
                                            self.minemap_board[x+dx][y+dy]),
                                        relief=tk.SUNKEN,
                                        bg=EMPTY_BG_COLOR
                                    )
                                    self.world_board[x+dx][y+dy] = OPEN_BOARD
                                    if self.minemap_board[x+dx][y+dy] == MINE:
                                        self.board_status = 1
                                    self.open_status += 1
                                elif self.minemap_board[x+dx][y+dy] == 0:
                                    search_list = np.zeros(
                                        self.shape, dtype=np.int8)
                                    self.search_board(
                                        0, (x+dx, y+dy), search_list)
        else:
            pass

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

    def search_board(self, word, coordinate: (int, int), search_list):
        x, y = coordinate
        num = x*self.shape[1]+y

        if x < 0 or y < 0 or x >= self.shape[1] or y >= self.shape[0]:
            return

        if search_list[x][y] == 1:
            return

        if self.minemap_board[x][y] == word:
            self.labels[num].config(
                text="",
                relief=tk.SUNKEN,
                bg=EMPTY_BG_COLOR
            )
            self.world_board[x][y] = OPEN_BOARD
            self.open_status += 1

            search_list[x][y] = 1
            self.search_board(word, (x-1, y), search_list)
            self.search_board(word, (x+1, y), search_list)
            self.search_board(word, (x-1, y-1), search_list)
            self.search_board(word, (x+1, y-1), search_list)
            self.search_board(word, (x-1, y+1), search_list)
            self.search_board(word, (x+1, y+1), search_list)
            self.search_board(word, (x, y-1), search_list)
            self.search_board(word, (x, y+1), search_list)
        elif self.minemap_board[x][y] != word and self.minemap_board[x][y] != MINE and self.world_board[x][y] == NONE:
            self.labels[num].config(
                text=str(self.minemap_board[x][y]),
                relief=tk.SUNKEN,
                bg=EMPTY_BG_COLOR
            )
            self.world_board[x][y] = OPEN_BOARD
            self.open_status += 1

            search_list[x, y] = 1

    def cheack_status(self):
        if self.board_status == 1:
            a = messagebox.askyesno(
                "ゲームオーバ", "ゲームオーバ\nコンティニューしますか？\nしない場合は終了します")
            if a:
                self.board_status = 0
                self.open_status = 0
                self.create_map(self.shape, self.mine)
            else:
                self.root.destroy()
        elif self.open_status == self.size-self.mine:
            a = messagebox.askyesno(
                "ゲームクリア", "ゲームクリア\nもう一度挑戦しますか？\nしない場合は終了します")
            if a:
                self.board_status = 0
                self.open_status = 0
                self.create_map(self.shape, self.mine)
            else:
                self.root.destroy()

        self.root.after(500, self.cheack_status)
