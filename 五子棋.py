"""
五子棋 (Gomoku) 游戏实现
使用 tkinter 进行图形界面开发
"""

import tkinter as tk
from tkinter import messagebox

class Gomoku:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("五子棋")
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="#D3D3D3")  # 修改背景颜色为浅灰色
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)
        self.board = [[0] * 15 for _ in range(15)]
        self.current_player = 1
        self.draw_board()

    def draw_board(self):
        for i in range(15):
            self.canvas.create_line(40 * i, 0, 40 * i, 600)
            self.canvas.create_line(0, 40 * i, 600, 40 * i)

    def click(self, event):
        x, y = event.x // 40, event.y // 40
        if self.board[y][x] == 0:
            self.board[y][x] = self.current_player
            self.draw_piece(x, y, self.current_player)
            if self.check_winner(x, y):
                messagebox.showinfo("游戏结束", f"玩家 {self.current_player} 获胜!")
                self.reset_game()
            self.current_player = 3 - self.current_player

    def draw_piece(self, x, y, player):
        color = "black" if player == 1 else "white"
        self.canvas.create_oval(x * 40 + 5, y * 40 + 5, x * 40 + 35, y * 40 + 35, fill=color)

    def check_winner(self, x, y):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for i in range(1, 5):
                if self.get_piece(x + i * dx, y + i * dy) == self.current_player:
                    count += 1
                else:
                    break
            for i in range(1, 5):
                if self.get_piece(x - i * dx, y - i * dy) == self.current_player:
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False

    def get_piece(self, x, y):
        if 0 <= x < 15 and 0 <= y < 15:
            return self.board[y][x]
        return None


    # 重置游戏
    # 清空棋盘数组
    # 清除画布上的所有内容
    # 重新绘制棋盘线条
    def reset_game(self):
        """
        重置游戏
        清空棋盘数组
        清除画布上的所有内容
        重新绘制棋盘线条
        """
        self.board = [[0] * 15 for _ in range(15)]
        self.canvas.delete("all")
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = Gomoku(root)
    root.mainloop()
