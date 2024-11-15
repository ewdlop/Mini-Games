import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.player = 'X'
        self.board = ['' for _ in range(9)]
        self.buttons = []
        self.create_menu()
        self.create_board()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)  # 确保菜单栏被配置到主窗口

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Game", command=self.new_game)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_board(self):
        for i in range(9):
            button = tk.Button(self.root, text='', font='normal 20 bold', height=3, width=6, 
                               command=lambda i=i: self.click(i))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

    def click(self, index):
        if self.board[index] == '' and not self.check_winner():
            self.board[index] = self.player
            self.buttons[index].config(text=self.player)
            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"Player {self.player} wins!")
            elif '' not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            else:
                self.player = 'O' if self.player == 'X' else 'X'

    def check_winner(self):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), 
                          (0, 3, 6), (1, 4, 7), (2, 5, 8), 
                          (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != '':
                return True
        return False

    def new_game(self):
        self.board = ['' for _ in range(9)]
        self.player = 'X'
        for button in self.buttons:
            button.config(text='')

    def show_about(self):
        messagebox.showinfo("About", "Tic Tac Toe game using Tkinter")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
