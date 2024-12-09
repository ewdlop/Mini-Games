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
pygame.display.set_caption("Breakout")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Paddle properties
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 8

# Ball properties
BALL_SIZE = 10
BALL_SPEED = 5

# Brick properties
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = WIDTH // (BRICK_WIDTH + 2)
BRICK_PADDING = 2

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - PADDLE_WIDTH//2, 
                              HEIGHT - 40, 
                              PADDLE_WIDTH, 
                              PADDLE_HEIGHT)

    def move(self):
        mouse_x, _ = pygame.mouse.get_pos()
        self.rect.centerx = mouse_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        pygame.draw.rect(window, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed_x = BALL_SPEED * random.choice((1, -1))
        self.speed_y = -BALL_SPEED
        self.rect = pygame.Rect(self.x, self.y, BALL_SIZE, BALL_SIZE)
        self.active = False

    def move(self):
        if not self.active:
            return

        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x
        self.rect.y = self.y

        # Wall collision
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1
        if self.rect.bottom >= HEIGHT:
            self.reset()

    def draw(self):
        pygame.draw.rect(window, WHITE, self.rect)

class Brick:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color
        self.active = True

    def draw(self):
        if self.active:
            pygame.draw.rect(window, self.color, self.rect)

def create_bricks():
    bricks = []
    colors = [RED, RED, ORANGE, ORANGE, YELLOW, YELLOW, GREEN, GREEN]
    
    for row in range(BRICK_ROWS):
        color = colors[row]
        for col in range(BRICK_COLS):
            x = col * (BRICK_WIDTH + BRICK_PADDING)
            y = row * (BRICK_HEIGHT + BRICK_PADDING) + 50
            brick = Brick(x, y, color)
            bricks.append(brick)
    return bricks

# Create game objects
paddle = Paddle()
ball = Ball()
bricks = create_bricks()
score = 0

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not ball.active:
            ball.active = True

    # Move paddle
    paddle.move()

    # Move ball
    ball.move()

    # Ball-paddle collision
    if ball.rect.colliderect(paddle.rect):
        ball.speed_y = -abs(ball.speed_y)  # Always bounce up
        # Adjust x speed based on where ball hits paddle
        relative_intersect_x = (paddle.rect.centerx - ball.rect.centerx)
        normalized_intersect = relative_intersect_x / (PADDLE_WIDTH/2)
        bounce_angle = normalized_intersect * 60  # Max angle: 60 degrees
        ball.speed_x = -BALL_SPEED * normalized_intersect

    # Ball-brick collision
    for brick in bricks:
        if brick.active and ball.rect.colliderect(brick.rect):
            brick.active = False
            ball.speed_y *= -1
            score += 10

    # Draw everything
    window.fill(BLACK)
    paddle.draw()
    ball.draw()
    for brick in bricks:
        brick.draw()

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (10, 10))

    # Draw "Click to start" message if ball is inactive
    if not ball.active:
        start_font = pygame.font.Font(None, 48)
        start_text = start_font.render("Click to start", True, WHITE)
        text_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        window.blit(start_text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
