import tkinter as tk
from tkinter import messagebox

class Sudoku:
    def __init__(self, root):
        self.root = root
        self.root.title("數獨")
        self.board = [[0] * 9 for _ in range(9)]
        self.entries = [[None] * 9 for _ in range(9)]
        self.create_widgets()

    def create_widgets(self):
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=2, font=('Arial', 24), justify='center')
                entry.grid(row=row, column=col, padx=5, pady=5)
                self.entries[row][col] = entry

        solve_button = tk.Button(self.root, text="解決", command=self.solve)
        solve_button.grid(row=9, column=0, columnspan=4)

        clear_button = tk.Button(self.root, text="清除", command=self.clear)
        clear_button.grid(row=9, column=5, columnspan=4)

    def solve(self):
        self.read_board()
        if self.solve_sudoku():
            self.update_board()
        else:
            messagebox.showinfo("數獨", "無法解決此數獨")

    def read_board(self):
        for row in range(9):
            for col in range(9):
                value = self.entries[row][col].get()
                self.board[row][col] = int(value) if value.isdigit() else 0

    def update_board(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, str(self.board[row][col]))

    def clear(self):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                self.board[row][col] = 0

    def solve_sudoku(self):
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty

        for num in range(1, 10):
            if self.is_valid(num, row, col):
                self.board[row][col] = num
                if self.solve_sudoku():
                    return True
                self.board[row][col] = 0

        return False

    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return (row, col)
        return None

    def is_valid(self, num, row, col):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        box_row = row // 3 * 3
        box_col = col // 3 * 3
        for i in range(3):
            for j in range(3):
                if self.board[box_row + i][box_col + j] == num:
                    return False

        return True

if __name__ == "__main__":
    root = tk.Tk()
    game = Sudoku(root)
    root.mainloop()
