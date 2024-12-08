import math
import pygame
import random
import os
from tkinter import messagebox
import tkinter as tk

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
# Center the window on screen
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
os_x = (screen_width - WIDTH) // 2
os_y = (screen_height - HEIGHT) // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{os_x},{os_y}"

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)

# Pacman properties
pacman_x = WIDTH // 2
pacman_y = HEIGHT // 2
pacman_radius = 20
pacman_speed = 5
pacman_direction = 0
mouth_angle = 45

# Power-up properties
power_up_active = False
power_up_timer = 0
power_up_duration = 300  # 5 seconds at 60 FPS
power_up_x = random.randint(50, WIDTH-50)
power_up_y = random.randint(50, HEIGHT-50)
power_up_radius = 10

# Ghost properties
GHOST_SPAWN_DELAY = 180  # 3 seconds at 60 FPS
ghost_spawn_timer = GHOST_SPAWN_DELAY

class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.radius = 20
        self.color = (255, 0, 0)  # Red ghost
        self.active = False  # Start inactive

    def move(self, pacman_x, pacman_y):
        if not self.active:
            return
        # Simple ghost AI - move towards Pacman
        if self.x < pacman_x:
            self.x += self.speed
        elif self.x > pacman_x:
            self.x -= self.speed
        if self.y < pacman_y:
            self.y += self.speed
        elif self.y > pacman_y:
            self.y -= self.speed

# Create ghost
ghost = Ghost(100, 100)

def show_start_screen():
    root = tk.Tk()
    
    # Center the start window
    window_width = 300
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    
    root.title("Pacman")
    
    # Add welcome message
    tk.Label(root, 
            text="Welcome to Pacman!\n\nUse arrow keys to move\nCollect power-ups to defeat ghosts", 
            pady=20).pack()
    
    def start_game():
        root.destroy()
    
    # Add start button
    tk.Button(root, text="Start Game", command=start_game, pady=10).pack()
    
    # Wait for user input
    root.mainloop()

def reset_game():
    global pacman_x, pacman_y, ghost, power_up_active, power_up_timer
    global power_up_x, power_up_y, ghost_spawn_timer, window
    
    # Reset Pacman position
    pacman_x = WIDTH // 2
    pacman_y = HEIGHT // 2
    
    # Reset ghost
    ghost = Ghost(100, 100)
    ghost_spawn_timer = GHOST_SPAWN_DELAY  # Reset spawn timer
    
    # Reset power-up
    power_up_active = False
    power_up_timer = 0
    power_up_x = random.randint(50, WIDTH-50)
    power_up_y = random.randint(50, HEIGHT-50)
    
    # Reset window
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pacman")
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{os_x},{os_y}"

# Show start screen
show_start_screen()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move Pacman based on key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman_x -= pacman_speed
        pacman_direction = 180
    if keys[pygame.K_RIGHT]:
        pacman_x += pacman_speed
        pacman_direction = 0
    if keys[pygame.K_UP]:
        pacman_y -= pacman_speed
        pacman_direction = 90
    if keys[pygame.K_DOWN]:
        pacman_y += pacman_speed
        pacman_direction = 270

    # Keep Pacman within screen bounds
    pacman_x = max(pacman_radius, min(WIDTH - pacman_radius, pacman_x))
    pacman_y = max(pacman_radius, min(HEIGHT - pacman_radius, pacman_y))

    # Handle ghost spawn timer
    if not ghost.active:
        ghost_spawn_timer -= 1
        if ghost_spawn_timer <= 0:
            ghost.active = True

    # Move ghost only if active
    ghost.move(pacman_x, pacman_y)

    # Handle power-up collision
    if not power_up_active:
        distance_to_power = math.sqrt((pacman_x - power_up_x)**2 + (pacman_y - power_up_y)**2)
        if distance_to_power < pacman_radius + power_up_radius:
            power_up_active = True
            power_up_timer = power_up_duration
            ghost.color = BLUE  # Ghost turns blue when vulnerable

    # Update power-up timer
    if power_up_active:
        power_up_timer -= 1
        if power_up_timer <= 0:
            power_up_active = False
            ghost.color = (255, 0, 0)  # Ghost returns to red
            
    # Handle ghost collision
    distance_to_ghost = math.sqrt((pacman_x - ghost.x)**2 + (pacman_y - ghost.y)**2)
    if distance_to_ghost < pacman_radius + ghost.radius and ghost.active:
        if power_up_active:
            ghost.active = False  # Ghost is defeated
            # Show victory message
            root = tk.Tk()
            root.withdraw()  # Hide the tkinter window
            if messagebox.askyesno("Victory!", "You defeated the ghost! Play again?"):
                reset_game()
                pygame.event.clear()  # Clear any pending events
            else:
                running = False
            root.destroy()
        else:
            # Show game over message
            root = tk.Tk()
            root.withdraw()  # Hide the tkinter window
            if messagebox.askyesno("Game Over", "Ghost caught you! Play again?"):
                reset_game()
                pygame.event.clear()  # Clear any pending events
            else:
                running = False
            root.destroy()

    # Clear screen
    window.fill(BLACK)

    # Draw Pacman
    pygame.draw.circle(window, YELLOW, (pacman_x, pacman_y), pacman_radius)
    # Draw Pacman's mouth
    pygame.draw.polygon(window, BLACK, [
        (pacman_x, pacman_y),
        (pacman_x + pacman_radius * math.cos(math.radians(pacman_direction - mouth_angle)),
         pacman_y - pacman_radius * math.sin(math.radians(pacman_direction - mouth_angle))),
        (pacman_x + pacman_radius * math.cos(math.radians(pacman_direction + mouth_angle)),
         pacman_y - pacman_radius * math.sin(math.radians(pacman_direction + mouth_angle)))
    ])

    # Draw power-up if not active
    if not power_up_active:
        pygame.draw.circle(window, PINK, (power_up_x, power_up_y), power_up_radius)

    # Only draw ghost if active
    if ghost.active:
        pygame.draw.circle(window, ghost.color, (int(ghost.x), int(ghost.y)), ghost.radius)

    # Update display
    pygame.display.flip()

    # Control game speed
    clock.tick(60)

pygame.quit()
