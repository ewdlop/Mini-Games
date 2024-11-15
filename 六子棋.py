import pygame
import sys
import json
from datetime import datetime

# 游戏基本设置
WINDOW_SIZE = 800  # 窗口大小
BOARD_SIZE = 15    # 棋盘大小(15x15)
GRID_SIZE = WINDOW_SIZE // (BOARD_SIZE + 1)  # 格子大小
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)

class connect6:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('六子棋')
        self.reset_game()
        
    def reset_game(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'black'
        self.history = []  # 用于悔棋
        self.game_over = False
        self.winner = None
        
    def check_win(self, x, y):
        directions = [(1,0), (0,1), (1,1), (1,-1)]  # 横、竖、正斜、反斜
        player = self.board[y][x]
        
        for dx, dy in directions:
            count = 1
            # 正向检查
            for i in range(1, 6):
                new_x, new_y = x + dx*i, y + dy*i
                if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
                    break
                if self.board[new_y][new_x] != player:
                    break
                count += 1
            # 反向检查
            for i in range(1, 6):
                new_x, new_y = x - dx*i, y - dy*i
                if not (0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE):
                    break
                if self.board[new_y][new_x] != player:
                    break
                count += 1
            
            if count >= 6:
                return True
        return False
    
    def undo_move(self):
        if self.history:
            last_move = self.history.pop()
            self.board[last_move[1]][last_move[0]] = None
            self.current_player = 'white' if self.current_player == 'black' else 'black'
            self.game_over = False
            self.winner = None
            
    def save_game(self):
        game_state = {
            'board': self.board,
            'current_player': self.current_player,
            'history': self.history
        }
        filename = f"game_save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(game_state, f)
            
    def load_game(self, filename):
        try:
            with open(filename, 'r') as f:
                game_state = json.load(f)
                self.board = game_state['board']
                self.current_player = game_state['current_player']
                self.history = game_state['history']
                self.game_over = False
                self.winner = None
        except:
            print("无法加载游戏存档")

    def draw_game_over(self):
        if self.game_over:
            font = pygame.font.Font(None, 74)
            text = f"{'黑方' if self.winner == 'black' else '白方'}胜利!"
            text_surface = font.render(text, True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
            self.screen.blit(text_surface, text_rect)

    def draw_board(self):
        self.screen.fill(BROWN)
        # 画网格线
        for i in range(BOARD_SIZE):
            pygame.draw.line(self.screen, BLACK, 
                           (GRID_SIZE, GRID_SIZE * (i + 1)),
                           (WINDOW_SIZE - GRID_SIZE, GRID_SIZE * (i + 1)))
            pygame.draw.line(self.screen, BLACK,
                           (GRID_SIZE * (i + 1), GRID_SIZE),
                           (GRID_SIZE * (i + 1), WINDOW_SIZE - GRID_SIZE))
    
    def draw_stones(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j]:
                    color = BLACK if self.board[i][j] == 'black' else WHITE
                    pygame.draw.circle(self.screen, color,
                                    (GRID_SIZE * (j + 1), GRID_SIZE * (i + 1)),
                                    GRID_SIZE // 2 - 2)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:  # Z键悔棋
                        self.undo_move()
                    elif event.key == pygame.K_s:  # S键保存
                        self.save_game()
                    elif event.key == pygame.K_l:  # L键读取最新存档
                        # 这里简化处理，实际应该让用户选择存档
                        self.load_game("最新的存档文件名.json")
                    
                if not self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    grid_x = round((x - GRID_SIZE) / GRID_SIZE)
                    grid_y = round((y - GRID_SIZE) / GRID_SIZE)
                    
                    if 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE:
                        if self.board[grid_y][grid_x] is None:
                            self.board[grid_y][grid_x] = self.current_player
                            self.history.append((grid_x, grid_y))
                            
                            if self.check_win(grid_x, grid_y):
                                self.game_over = True
                                self.winner = self.current_player
                            else:
                                self.current_player = 'white' if self.current_player == 'black' else 'black'
            
            self.draw_board()
            self.draw_stones()
            if self.game_over:
                self.draw_game_over()
            pygame.display.flip()

if __name__ == '__main__':
    game = connect6()
    game.run()
