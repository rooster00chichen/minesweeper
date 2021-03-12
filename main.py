import tkinter as tk
from gui import *

if __name__ == "__main__":
    shape_one = int(input("画面の一辺のサイズを設定："))
    if shape_one == 0:
        shape_one = 9
    shape = (shape_one, shape_one)
    mine = int(input("爆弾の個数を選択:"))
    if mine == 0:
        mine = 9
    window = GUI(shape=shape, mines=mine, menu_status=0)
