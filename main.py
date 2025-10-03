# --- IMPORTS ---
import pygame

# --- INITS ---
pygame.init()

# --- CONSTANTS ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Window constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Gamba Game"
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

FPS = 60

SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(SCREEN_TITLE)
CLOCK = pygame.time.Clock()

# --- VARIABLES ---
game_running = True

# --- DEFINITIONS ---

# --- CODE BEGIN HERE ---

# -- MAIN LOOP ---
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    SCREEN.fill(BLACK)
    # Draw stuff here

    pygame.display.flip()

    CLOCK.tick(FPS)

pygame.quit()