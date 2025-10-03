# --- IMPORTS ---
import pygame
import pygame_menu

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
# Everything in the game stops if this is False...
game_running = False
# States - "menu": Main menu, "game": Gameplay, "paused": Displays pause menu
current_state = "menu"

username = ""
money = 0

# --- DEFINITIONS ---
def set_username(value):
    global username
    username = value

def start_game():
    global game_running
    global current_state
    if not username == '':
        game_running = True
        current_state = "game"
        MAIN_MENU.disable()
    else:
        print("Please enter your name.")

def pause_game():
    global current_state
    global game_running
    game_running = False
    current_state = "paused"

def toggle_main_menu():
    if MAIN_MENU.is_enabled():
        MAIN_MENU.disable()
    else:
        MAIN_MENU.enable()

# Main menu setup
MAIN_MENU = pygame_menu.Menu(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
MAIN_MENU.add.text_input('Name: ', onchange=set_username)
MAIN_MENU.add.button('Play', start_game)
MAIN_MENU.add.button('Quit', pygame_menu.events.EXIT)

# --- CODE BEGIN HERE ---

# -- MAIN LOOP ---
MAIN_MENU.mainloop(SCREEN)

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    SCREEN.fill(WHITE)
    # Draw stuff here

    pygame.display.flip()

    CLOCK.tick(FPS)

pygame.quit()