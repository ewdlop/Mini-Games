import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600

# Center the window on screen
screen_info = pygame.display.Info()
os_x = (screen_info.current_w - WIDTH) // 2
os_y = (screen_info.current_h - HEIGHT) // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{os_x},{os_y}"

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paddle properties
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
PADDLE_SPEED = 5

# Ball properties
BALL_SIZE = 15
BALL_SPEED_X = 7
BALL_SPEED_Y = 7

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.score = 0

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= PADDLE_SPEED
        if not up and self.rect.bottom < HEIGHT:
            self.rect.y += PADDLE_SPEED

    def draw(self):
        pygame.draw.rect(window, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = BALL_SPEED_X * random.choice((1, -1))
        self.speed_y = BALL_SPEED_Y * random.choice((1, -1))
        self.rect = pygame.Rect(self.x, self.y, BALL_SIZE, BALL_SIZE)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x
        self.rect.y = self.y

        # Wall collision
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def draw(self):
        pygame.draw.rect(window, WHITE, self.rect)

# Create game objects
player = Paddle(50, HEIGHT//2 - PADDLE_HEIGHT//2)
opponent = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
ball = Ball()

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.move(up=True)
    if keys[pygame.K_s]:
        player.move(up=False)
    
    # Simple AI for opponent
    if opponent.rect.centery < ball.rect.centery:
        opponent.move(up=False)
    if opponent.rect.centery > ball.rect.centery:
        opponent.move(up=True)

    # Move ball
    ball.move()

    # Paddle collision
    if ball.rect.colliderect(player.rect) or ball.rect.colliderect(opponent.rect):
        ball.speed_x *= -1

    # Score points
    if ball.rect.left <= 0:
        opponent.score += 1
        ball.reset()
    if ball.rect.right >= WIDTH:
        player.score += 1
        ball.reset()

    # Draw everything
    window.fill(BLACK)
    player.draw()
    opponent.draw()
    ball.draw()

    # Draw scores
    font = pygame.font.Font(None, 74)
    score_text = font.render(f"{player.score} - {opponent.score}", True, WHITE)
    window.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

    # Draw center line
    pygame.draw.aaline(window, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    pygame.display.flip()
    clock.tick(60)

pygame.quit() 