import tkinter as tk
import subprocess as sp
import numpy as np
from tkinter import messagebox

MINE = -1
NONE = 0
RAISE_FLAG = 1
OPEN_BOARD = 2
EMPTY_BG_COLOR = "lightgray"
RAISE_BG_COLOR = "yellow"


class GUI:
    def __init__(self, shape: (int, int) = (9, 9), mines: int = 10, menu_status=0):
        if menu_status == 0:
            self.root = tk.Tk()
            self.create_map(shape, mines)
        elif menu_status == 1:
            self.mode_select()

    def text_to_int(self, text):
        value = 0
        for str in text:
            if str <= '9' and str >= '0':
                value = value*10+int(str)

        return value

    def mode_select(self, shape: (int, int) = (9, 9), mines: int = 10):
        menu = tk.Tk()
        menu.geometry('600x400')
        menu.title("マインスイーパ")

        def click_shape_btn(entry, quantrtity):  # 簡易入力ボタン用処理
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(quantrtity))

        def click_mines_btn(shape_entry, mine_entry, denominator: int):
            shape_num = self.text_to_int(shape_entry.get())
            mine_input_num = (shape_num**2)//denominator
            mine_entry.delete(0, tk.END)
            mine_entry.insert(tk.END, str(mine_input_num))

        shape_lbl = tk.Label(menu, text='マスの一辺を設定')  # マスの入力欄用テキスト
        shape_lbl.place(x=100, y=110)

        shape_input = tk.Entry(width=20)  # 一辺の長さ入力
        shape_input.insert(tk.END, str(shape[0]))
        shape_input.place(x=350, y=110)

        shape_nine_btn = tk.Button(
            menu, text="9", command=lambda: click_shape_btn(shape_input, 9), bg=EMPTY_BG_COLOR)
        shape_nine_btn.place(x=350, y=140)
        shape_fifty_btn = tk.Button(
            menu, text="15", command=lambda: click_shape_btn(shape_input, 15), bg=EMPTY_BG_COLOR)
        shape_fifty_btn.place(x=365, y=140)
        shape_twenty_btn = tk.Button(
            menu, text="20", command=lambda: click_shape_btn(shape_input, 20), bg=EMPTY_BG_COLOR)
        shape_twenty_btn.place(x=390, y=140)

        mine_lbl = tk.Label(menu, text='爆弾の個数を設定')  # mine用テキスト
        mine_lbl.place(x=100, y=210)

        mine_input = tk.Entry(width=20)  # mine入力欄
        mine_input.insert(tk.END, str(mines))
        mine_input.place(x=350, y=210)

        mine_third_btn = tk.Button(
            menu, text="1/3", command=lambda: click_mines_btn(shape_input, mine_input, 3))
        mine_third_btn.place(x=350, y=235)

        mine_forth_btn = tk.Button(
            menu, text="1/4", command=lambda: click_mines_btn(shape_input, mine_input, 4))
        mine_forth_btn.place(x=380, y=235)

        mine_fifth_btn = tk.Button(
            menu, text="1/5", command=lambda: click_mines_btn(shape_input, mine_input, 5))
        mine_fifth_btn.place(x=410, y=235)

        def click_ch_btn():
            shape_one_text = shape_input.get()
            shape_one = self.text_to_int(shape_one_text)
            if shape_one == 0:
                shape_one = 9
            shape = (shape_one, shape_one)
            mine_text = mine_input.get()
            mines = self.text_to_int(mine_text)
            if mines == 0:
                mines = 10
            cheack_status = self.cheack_mine_shape_value(shape, mines)
            if cheack_status:
                menu.destroy()
                self.root = tk.Tk()
                self.create_map(shape, mines)
            else:
                error_label = tk.Label(menu, text="画面のサイズと比べて、爆弾が多すぎます。")
                error_label.place(x=80, y=330)
                hint_label = tk.Label(
                    menu, text="ヒント：爆弾= マスの一辺^2 -1 でとりあえずはok")
                hint_label.place(x=80, y=360)

        button = tk.Button(menu, text="確定する", font=("Times New Roman", 32),
                           bg="green", command=click_ch_btn)
        button.place(x=600/4*3-64, y=340)
        menu.mainloop()

    def cheack_mine_shape_value(self, shape: (int, int), mine):
        size = np.prod(shape)
        if size <= mine:
            return False
        return True

    def create_map(self, shape: (int, int), mines: int):
        self.mine_status = 0
        self.open_status = 0
        self.clear_status = 0
        self.create_map_date(shape, mines)
        self.create_map_view()
        self.root.after(500, self.cheack_status)
        self.root.mainloop()

    def create_map_date(self, shape: (int, int), mines: int):
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
                if self.minemap_board[x][y] == NONE or (self.minemap_board[x][y] != MINE and self.size-self.mine <= 3):
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
                    self.mine_status = 1
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
                                        self.mine_status = 1
                                    self.open_status += 1
                                elif self.minemap_board[x+dx][y+dy] == 0:
                                    search_list = np.zeros(
                                        self.shape, dtype=np.int8)
                                    self.search_board(
                                        0, (x+dx, y+dy), search_list)
        else:
            pass

        if self.open_status == self.size-self.mine:
            self.clear_status = 1

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
        if self.mine_status == 1:
            a = messagebox.askyesno(
                "ゲームオーバ", "ゲームオーバ\nコンティニューしますか？\nしない場合は終了します")
            if a:
                self.mine_status = 0
                self.open_status = 0
                self.clear_status = 0
                self.create_map(self.shape, self.mine)
            else:
                self.root.destroy()
        elif self.clear_status == 1:
            a = messagebox.askyesno(
                "ゲームクリア", "ゲームクリア\nもう一度挑戦しますか？\nしない場合は終了します")
            if a:
                self.mine_status = 0
                self.open_status = 0
                self.clear_status = 0
                self.create_map(self.shape, self.mine)
            else:
                self.root.destroy()

        self.root.after(250, self.cheack_status)


if __name__ == "__main__":
    window = GUI(menu_status=1)
