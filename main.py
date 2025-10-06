# --- IMPORTS ---
import pygame
import pygame_menu
import random as rand
import numpy as np


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
# States - "menu": Main menu, "game": Gameplay
current_state = "menu"

# --- DEFINITIONS ---
def start_game():
    global game_running
    game_running = True

# Main menu setup
MAIN_MENU = pygame_menu.Menu(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_BLUE)
MAIN_MENU.add.text_input('Name: ')
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


# Gambling shenanganery, Will inplement once chances are done


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