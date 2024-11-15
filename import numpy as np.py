import numpy as np

class Connect5:
    def __init__(self, rows=15, cols=15):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.current_player = 1

    def make_move(self, row, col):
        if self.board[row][col] == 0:
            self.board[row][col] = self.current_player
            self.current_player = 3 - self.current_player
            return True
        return False

    def check_winner(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != 0:
                    if self._check_direction(row, col, 1, 0) or \
                       self._check_direction(row, col, 0, 1) or \
                       self._check_direction(row, col, 1, 1) or \
                       self._check_direction(row, col, 1, -1):
                        return self.board[row][col]
        return 0

    def _check_direction(self, row, col, dr, dc):
        player = self.board[row][col]
        count = 1
        for i in range(1, 5):
            r, c = row + i*dr, col + i*dc
            if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == player:
                count += 1
            else:
                break
        for i in range(1, 5):
            r, c = row - i*dr, col - i*dc
            if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == player:
                count += 1
            else:
                break
        return count >= 5

    def print_board(self):
        for row in self.board:
            print(' '.join(['X' if cell == 1 else 'O' if cell == 2 else '.' for cell in row]))

def play_game():
    game = Connect5()
    while True:
        game.print_board()
        row = int(input(f"玩家 {game.current_player}，请输入行号 (0-14): "))
        col = int(input(f"玩家 {game.current_player}，请输入列号 (0-14): "))
        if game.make_move(row, col):
            winner = game.check_winner()
            if winner != 0:
                game.print_board()
                print(f"玩家 {winner} 获胜！")
                break
        else:
            print("无效的移动，请重试。")

if __name__ == "__main__":
    play_game()
