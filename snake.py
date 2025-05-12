# Import the necessary libraries
import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Set up the display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the clock
clock = pygame.time.Clock()

class SnakeGame:
    def __init__(self):
        self.snake = [(200, 200), (220, 200), (240, 200)]
        self.direction = 'RIGHT'
        self.apple = self.generate_apple()

    def generate_apple(self):
        while True:
            x = random.randint(0, WIDTH - 20) // 20 * 20
            y = random.randint(0, HEIGHT - 20) // 20 * 20
            if (x, y) not in self.snake:
                return x, y

    def draw(self):
        win.fill(BLACK)
        for x, y in self.snake:
            pygame.draw.rect(win, GREEN, (x, y, 20, 20))
        pygame.draw.rect(win, RED, (*self.apple, 20, 20))
        text = font.render(f'Score: {len(self.snake)}', True, WHITE)
        win.blit(text, (10, 10))
        pygame.display.update()

    def move(self):
        head = self.snake[-1]
        if self.direction == 'RIGHT':
            new_head = (head[0] + 20, head[1])
        elif self.direction == 'LEFT':
            new_head = (head[0] - 20, head[1])
        elif self.direction == 'UP':
            new_head = (head[0], head[1] - 20)
        elif self.direction == 'DOWN':
            new_head = (head[0], head[1] + 20)

        self.snake.append(new_head)
        if self.apple == new_head:
            self.apple = self.generate_apple()
        else:
            self.snake.pop(0)

        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in self.snake[:-1]):
            return False
        return True

    def play(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction!= 'DOWN':
                        self.direction = 'UP'
                    elif event.key == pygame.K_DOWN and self.direction!= 'UP':
                        self.direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and self.direction!= 'RIGHT':
                        self.direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and self.direction!= 'LEFT':
                        self.direction = 'RIGHT'

            if not self.move():
                break
            self.draw()
            clock.tick(10)

        win.fill(BLACK)
        text = font.render('Game Over', True, WHITE)
        win.blit(text, (WIDTH // 2 - 50, HEIGHT // 2 - 18))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()

if __name__ == '__main__':
    game = SnakeGame()
    game.play()
