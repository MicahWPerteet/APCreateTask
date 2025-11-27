# --- IMPORTS ---
import pygame
import pygame_menu
import random as rand
import numpy as np

# '''

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
CENTER = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

FPS = 60

# Text setup
FONT_SIZE = 30
FONT = pygame.font.Font(None, FONT_SIZE)

TEXT_X_MARGIN = 5
TEXT_Y_MARGIN = 5
MONEY_TEXT_POSITION = (TEXT_X_MARGIN, TEXT_Y_MARGIN)

SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(SCREEN_TITLE)
CLOCK = pygame.time.Clock()

# load icon images
SLOT_ICON_IMAGES = [
    pygame.image.load(f"images/placeholder/slot_icon_{i}.gif").convert_alpha()
    for i in range(1, 4)
]
# class setup for icons
class icon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = rand.choice(SLOT_ICON_IMAGES)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# create a sprite group and populate it with three icons
icons = pygame.sprite.Group()
for i in range(3):
    icons.add(icon((i * 100 + CENTER[0]) - 100, CENTER[1]))

'''
LEVER_ANIM_FRAMES = [
    pygame.image.load(f"lever_frame_{i}.gif").convert_alpha()
    for i in range(1, 6)
]

LEVER_ANIM_FRAME_RATE = 10 # 5 frame animation takes .5 seconds

class lever(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = LEVER_ANIM_FRAMES[0]
        self.rect = self.image.get_rect()
        self.rect.center(x, y)
        
    def play_animation(self):
        # play downward pull animation
        for frame in LEVER_ANIM_FRAMES:
            self.image = frame
'''

# --- VARIABLES ---
# States - "menu": Main menu, "game": Gameplay, "paused": Displays pause menu
current_state = "menu"
# This flag helps insure the pause menu doesn't get updated while it is disabled
resume_requested = False

username = ""
money = 0

spinning = False

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
    PAUSE_MENU_MONEY_LABEL.set_title("Money: " + str(money))
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
PAUSE_MENU.add.label("Money: " + str(money), label_id="pause_money_label")
PAUSE_MENU_MONEY_LABEL = PAUSE_MENU.get_widget("pause_money_label")
PAUSE_MENU.add.label("") # blank label for spacing (do not remove)
PAUSE_MENU.add.button("Resume", resume_game)
PAUSE_MENU.add.button("Quit", pygame_menu.events.EXIT)

# --- CODE BEGIN HERE ---
# --- MAIN LOOP ---
# starts the main loop for the main menu
MAIN_MENU.mainloop(SCREEN)

while True:
    # event handling
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: # quit button functionality
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN: # keypress event checker
            if current_state == "game":
                if event.key == pygame.K_p:
                    pause_game()
                if event.key == pygame.K_m:
                    money += 10

    if current_state == "game":
        SCREEN.fill(BG_GRAY)

        # update money text
        money_text = FONT.render("Money: " + str(money), True, BLACK)
        # renders money text
        SCREEN.blit(money_text, MONEY_TEXT_POSITION)
        icons.draw(SCREEN)

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
# TODO Get chances working
'''
icons = ["7", "bell", "clover", "cherry", "triple bar", "double bar", "bar"]
num1= None
num2= None
num3= None

nums = []
output = []

mean = 0
std_dev = 1

bar = .4
bar2 = .8
bar3 = 1.2
cherry = 1.6
clover = 2
bell = 2.4

def spin():
    global nums
    nums = []
    for n in range(3):
        nums.append(np.random.normal(loc=mean, scale=std_dev))
def rank(num):
    global output
    if abs(num) <= bar:
        new_icon = (icons[6])
    elif abs(num) <= bar2:
        new_icon = (icons[5])
    elif abs(num) <= bar3:
        new_icon = (icons[4])
    elif abs(num) <= cherry:
        new_icon = (icons[3])
    elif abs(num) <= clover:
        new_icon = (icons[2])
    elif abs(num) <= bell:
        new_icon = (icons[1])
    else:
        new_icon = (icons[0])   
    return(new_icon)
def roll():
    global nums, icons, output
    output = []
    multi = .7
    spin()
    for i in range(3):
        output.append(rank(nums[i]))
    print("rolling...")
    print(output)
    print(nums[0],nums[1],nums[2])
    if output[0] == output[1] and output[1] == output [2]:
        multi = nums[1]*3
        print("Full", output[1], "straight")
    elif output[0] == output[1] or output[1] == output[2]: 
        multi = nums[1]*2
        print(output[1], "straight")
    return(abs(multi))
    
rollagain= True
while rollagain == True:
    bet = 100 # float(input("How much money do you want to bet? ->"))
    total = bet
    rolls = 1 # int(input("How many times would you like to roll? ->"))
    hhh = (input("->")) # placeholder variable to change the final multiplie. Current idea: .3

    for r in range(rolls):
        multi = roll()
        total = multi*total
        earn = total - bet

    print("ammount changed", round(earn))
    cash = bet+earn
    print("You made", round(cash, 2))
    # rollagain = input("Roll again? ->")
    # if rollagain == "y":
    #     rollagain = True
    # else:
    #     rollagain = False
'''