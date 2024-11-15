import tkinter as tk
from tkinter import messagebox

class Connect4:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("四子棋")
        self.canvas = tk.Canvas(self.root, width=700, height=600, bg="blue")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)
        self.board = [[0] * 7 for _ in range(6)]
        self.current_player = 1
        self.draw_board()

    def draw_board(self):
        for row in range(6):
            for col in range(7):
                self.canvas.create_oval(col * 100 + 5, row * 100 + 5, col * 100 + 95, row * 100 + 95, fill="white")

    def click(self, event):
        col = event.x // 100
        if col < 0 or col >= 7:
            return
        for row in range(5, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.draw_piece(row, col, self.current_player)
                if self.check_winner(row, col):
                    messagebox.showinfo("游戏结束", f"玩家 {self.current_player} 获胜!")
                    self.reset_game()
                self.current_player = 3 - self.current_player
                break

    def draw_piece(self, row, col, player):
        color = "red" if player == 1 else "yellow"
        self.canvas.create_oval(col * 100 + 5, row * 100 + 5, col * 100 + 95, row * 100 + 95, fill=color)

    def check_winner(self, row, col):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for i in range(1, 4):
                if self.get_piece(row + i * dy, col + i * dx) == self.current_player:
                    count += 1
                else:
                    break
            for i in range(1, 4):
                if self.get_piece(row - i * dy, col - i * dx) == self.current_player:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False

    def get_piece(self, row, col):
        if 0 <= row < 6 and 0 <= col < 7:
            return self.board[row][col]
        return None

    def reset_game(self):
        self.board = [[0] * 7 for _ in range(6)]
        self.canvas.delete("all")
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = Connect4(root)
    root.mainloop()
