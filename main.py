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
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Gamba Game"
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
CENTER = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
FPS = 60

# Text setup
FONT_SIZE = 40
FONT = pygame.font.Font(None, FONT_SIZE)

TEXT_X_MARGIN = 5
TEXT_Y_MARGIN = 5
MONEY_TEXT_POSITION = (TEXT_X_MARGIN, TEXT_Y_MARGIN)

SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(SCREEN_TITLE)
CLOCK = pygame.time.Clock()

# list to hold ids for unique ids
UNIQUE_EVENT_IDS = []

TIMED_TEXT_OBJECTS = []

def generate_event_id():
    global UNIQUE_EVENT_IDS
    id = 1
    while id in UNIQUE_EVENT_IDS:
        id += 1
    UNIQUE_EVENT_IDS.append(id)
    return pygame.USEREVENT + id

# load icon images
SLOT_ICON_IMAGES = [
    pygame.image.load("images/icons/cherry.png").convert_alpha(),
    pygame.image.load("images/icons/seven.png").convert_alpha(),
    pygame.image.load("images/icons/clover.png").convert_alpha(),
    pygame.image.load("images/icons/bell.png").convert_alpha(),
    pygame.image.load("images/icons/single_bar.png").convert_alpha(),
    pygame.image.load("images/icons/double_bar.png").convert_alpha(),
    pygame.image.load("images/icons/triple_bar.png").convert_alpha(),
    pygame.image.load("images/icons/diamond.png").convert_alpha(),
    pygame.image.load("images/icons/horseshoe.png").convert_alpha()
]

SLOT_BASE_IMAGE = pygame.image.load("images/slot_base.gif").convert_alpha()
SLOT_BASE_IMAGE = pygame.transform.scale_by(SLOT_BASE_IMAGE, (2.3, 2))
# class setup for icons
class icon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = rand.choice(SLOT_ICON_IMAGES)
        self.rect = self.image.get_rect()   
        self.rect.center = (x, y)

    def choose_random_image(self):
        self.image = rand.choice(SLOT_ICON_IMAGES)

class slot_base(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = SLOT_BASE_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

SLOT_BASE_GROUP = pygame.sprite.Group()
SLOT_BASE_GROUP.add(slot_base(CENTER[0], CENTER[1]))

# custom userevent for icon switching
ICON_SWITCH_EVENT = generate_event_id()
SPIN_CYCLE_EVENT = generate_event_id()
SPIN_TIME = 2000
# timer setup for icon switching event
pygame.time.set_timer(ICON_SWITCH_EVENT, 200)

# create a sprite group and populate it with three icons
ICONS_GROUP = pygame.sprite.Group()
for i in range(3):
    ICONS_GROUP.add(icon((i * 135 + CENTER[0]) - 135, CENTER[1] - 220))
    
LEVER_ANIM_FRAMES = [
    *[pygame.transform.scale_by(pygame.image.load(f"images/lever_{i}.gif").convert_alpha(), 2)
    for i in range(1, 7)]
]

# custom userevent for the lever animation
LEVER_ANIM_EVENT = generate_event_id()
pygame.time.set_timer(LEVER_ANIM_EVENT, 50)

class lever(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.current_frame = 0
        self.cycled = True
        self.image = LEVER_ANIM_FRAMES[self.current_frame]
        self.direction = "down"
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def step_animation(self):
        global spinning
        # play downward pull animation
        if self.direction == "down" and not self.current_frame == 5:
            self.current_frame += 1
            self.image = LEVER_ANIM_FRAMES[self.current_frame]
        # play upward pull animation
        elif self.direction == "up" and not self.current_frame == 0:
            self.current_frame -= 1
            self.image = LEVER_ANIM_FRAMES[self.current_frame]
        # switch direction once the animation reaches the last frame
        if self.current_frame == 5:
            self.direction = "up"
        elif self.current_frame == 0 and self.cycled == False:
            self.direction = "down"
            self.cycled = True
            spinning = False

LEVER_GROUP = pygame.sprite.Group()
LEVER_GROUP.add(lever(CENTER[0] + 360, CENTER[1]))
LEVER = LEVER_GROUP.sprites()

# --- VARIABLES ---
# States - "menu": Main menu, "game": Gameplay, "paused": Displays pause menu
current_state = "menu"
# This flag helps insure the pause menu doesn't get updated while it is disabled
resume_requested = False

username = ""
money = 0
bet_amount = 10

spinning = False
no_money_timedtext_visable = False

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

def event_handler(events):
    global money
    global no_money_timedtext_visable
    global spinning
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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            print("Clicked", mouse_pos)
            if LEVER[0].rect.collidepoint(mouse_pos) and current_state == "game" and not spinning:
                if money - bet_amount < 0:
                    if not no_money_timedtext_visable:
                        no_money_timedtext_visable = True
                        text = "Not enough money!"
                        width = FONT.size(text)[0]
                        TimedText(text, FONT_SIZE * 2, BLACK, 2, (CENTER[0] - width, CENTER[1] + 200))
                else:
                    money -= bet_amount
                    print("Clicked Lever")
                    spinning = True
                    pygame.time.set_timer(SPIN_CYCLE_EVENT, SPIN_TIME, 1)
                    LEVER[0].cycled = False
            
        elif event.type == ICON_SWITCH_EVENT and spinning:
            for icon in ICONS_GROUP:
                icon.choose_random_image()

        elif event.type == SPIN_CYCLE_EVENT and spinning:
            spinning = False
            for j, icon in enumerate(ICONS_GROUP):
                # switch each icon to it's final image as returned from Isaac's code
                pass

        elif event.type == LEVER_ANIM_EVENT and not LEVER[0].cycled:
            LEVER[0].step_animation()
        
        elif TIMED_TEXT_OBJECTS is not []:
            for timedtext in TIMED_TEXT_OBJECTS:
                if event.type == timedtext.id:
                    timedtext.visable = False
                    TIMED_TEXT_OBJECTS.remove(timedtext)
                    if timedtext.text == "Not enough money!":
                        no_money_timedtext_visable = False

class TimedText:
    def __init__(self, text, size, color, time, location):
        self.visable = True
        self.id = generate_event_id()
        self.font = pygame.font.Font(None, size)
        self.text = text
        self.display_text = self.font.render(text, True, color)
        pygame.time.set_timer(self.id, (time * 1000), loops=1)
        self.location = location
        TIMED_TEXT_OBJECTS.append(self)
    
    def draw(self):
            if self.visable:
                SCREEN.blit(self.display_text, self.location)

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
    event_handler(events)
    
    if current_state == "game":
        SCREEN.fill(BG_GRAY)

        # update money text
        money_text = FONT.render("Money: " + str(money), True, BLACK)
        # renders money text
        SCREEN.blit(money_text, MONEY_TEXT_POSITION)
        LEVER_GROUP.draw(SCREEN)
        SLOT_BASE_GROUP.draw(SCREEN)
        ICONS_GROUP.draw(SCREEN)
        
        if TIMED_TEXT_OBJECTS is not []:
            for timedtext in TIMED_TEXT_OBJECTS:
                timedtext.draw()

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
# TODO Get chances perfectt
'''
icons = ["7", "diamond", "bell", "horseshoe", "clover", "cherry", "triple bar", "double bar", "bar"]
num1= None
num2= None
num3= None

nums = []

mean = 0
std_dev = 1

bar = .3
bar2 = .6
bar3 = .9
cherry = 1.2
clover = 1.5
horseshoe = 1.8
bell = 2.1
diamond = 2.4

def spin():
    global nums
    nums = []
    for n in range(3):
        nums.append(np.random.normal(loc=mean, scale=std_dev))
def rank(num):
    if abs(num) <= bar:
        new_icon = (icons[8])
    elif abs(num) <= bar2:
        new_icon = (icons[7])
    elif abs(num) <= bar3:
        new_icon = (icons[6])
    elif abs(num) <= cherry:
        new_icon = (icons[5])
    elif abs(num) <= clover:
        new_icon = (icons[4])
    elif abs(num) <= horseshoe:
        new_icon = (icons[3])
    elif abs(num) <= bell:
        new_icon = (icons[2])
    elif abs(num) <= diamond:
        new_icon = (icons[1])
    else:
        new_icon = (icons[0])   
    return(new_icon)
def roll(money):
    global nums
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
    final = money
    final = abs(multi)*final
    return(final)

bet = 100
rollagain= True
while rollagain == True:
    # bet = 100 # float(input("How much money do you want to bet? ->"))
    rolls = 1 # int(input("How many times would you like to roll? ->"))
    hhh = (input("->")) 

    for r in range(rolls):
        bet = roll(bet)
    print("Current Balence", round(bet, 2))
    # rollagain = input("Roll again? ->")
    # if rollagain == "y":
    #     rollagain = True
    # else:
    #     rollagain = False

'''