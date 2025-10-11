# --- IMPORTS ---
import pygame
import pygame_menu
import random as rand
import numpy as np

# import test
if not pygame.font:
    print("Warning: fonts disabled")

# --- INITS ---
pygame.init()

# --- CONSTANTS ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG_GRAY = (211, 211, 211)

# Window constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Gamba Game"
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

FPS = 60

SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(SCREEN_TITLE)
CLOCK = pygame.time.Clock()

# Creates background surface
BACKGROUND = pygame.Surface(SCREEN.get_size())
BACKGROUND = BACKGROUND.convert()

# --- VARIABLES ---
# States - "menu": Main menu, "game": Gameplay, "paused": Displays pause menu
current_state = "menu"
# This flag helps insure the pause menu doesn't get updated while it is disabled
resume_requested = False

username = ""
money = 0

# --- DEFINITIONS ---
def set_username(input):
    global username
    username = input

def update_money(modifier):
    global money
    money += modifier


def start_game():
    global current_state
    if not username == '':
        current_state = "game"
        print(username)
        MAIN_MENU.disable()
    else:
        print("Please enter your name")

def pause_game():
    if not PAUSE_MENU.is_enabled():
        PAUSE_MENU.enable()
    global current_state
    current_state = "paused"

def resume_game():
    global resume_requested
    resume_requested = True

# Main menu setup
MAIN_MENU = pygame_menu.Menu(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
MAIN_MENU.add.text_input("Name: ", onchange=set_username)
MAIN_MENU.add.button("Play", start_game)
MAIN_MENU.add.button("Quit", pygame_menu.events.EXIT)

# Pause menu setup
PAUSE_MENU = pygame_menu.Menu("Paused", SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
PAUSE_MENU.add.label("Money: " + str(money))
PAUSE_MENU.add.label("")
PAUSE_MENU.add.button("Resume", resume_game)
PAUSE_MENU.add.button("Quit", pygame_menu.events.EXIT)

# --- CODE BEGIN HERE ---

# --- MAIN LOOP ---
# starts the main loop for the main menu
MAIN_MENU.mainloop(SCREEN)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and current_state == "game":
                pause_game()

    if current_state == "game":
        SCREEN.fill(WHITE)
        


        pygame.display.flip()

    elif current_state == "paused":
        if PAUSE_MENU.is_enabled():
            PAUSE_MENU.update(events)

            if resume_requested:
                PAUSE_MENU.disable()
                current_state = "game"
                resume_requested = False
            else:
                PAUSE_MENU.draw(SCREEN)
                pygame.display.flip()
    
    CLOCK.tick(FPS)

# Gambling shenanganery, Will inplement once chances are done
'''

icons = ["7", "bell", "clover", "cherry", "triple bar", "double bar", "bar"]
num1= None
num2= None
num3= None

mean = 0
std_dev = 1

bar = .4
bar2 = .8
bar3 = 1.2
cherry = 1.6
clover = 2
bell = 2.4


def spin():
    global num1, num2, num3
    num1 = np.random.normal(loc=mean, scale=std_dev)
    num2 = np.random.normal(loc=mean, scale=std_dev)
    num3 = np.random.normal(loc=mean, scale=std_dev)
def rank(num):
    if abs(num) <= bar:
        num = icons[6]
    elif abs(num) <= bar2:
        num = icons[5]
    elif abs(num) <= bar3:
        num = icons[4]
    elif abs(num) <= cherry:
        num = icons[3]
    elif abs(num) <= clover:
        num = icons[2]
    elif abs(num) <= bell:
        num = icons[1]
    else:
        num = icons[0]    
    return(num)
def roll():
    global num1, num2, num3, icons
    spin()
    num1 = rank(num1)
    num2 = rank(num2)
    num3 = rank(num3)
    print("rolling...")
    output = [num1, num2, num3]
    print(output)
    if output[0] == output[1] and output[1] == output [2]:
        print("Full", num2, "straight")
    elif output[0] == output[1] or output[1] == output[2]: 
        print(num2, "straight")

for i in range(5):
    roll()

'''