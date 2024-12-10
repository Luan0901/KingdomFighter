import pygame
from fighter import Fighter
from pygame import mixer
from button import Button
mixer.init()
pygame.init()

# declare screen resolution
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# define game varriables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0 , 0] # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

sound_played = False

# define fighter varriables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# load music and sounds
pygame.mixer.music.load("assets/audio/music1.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
warrior_fx = pygame.mixer.Sound("assets/audio/warrior.mp3")
wizard_fx = pygame.mixer.Sound("assets/audio/magic.wav")
P1_win_fx = pygame.mixer.Sound("assets/audio/player-1-wins.mp3")
P2_win_fx = pygame.mixer.Sound("assets/audio/player-2-wins.mp3")
# create game window
screen = pygame.display.set_mode(( SCREEN_WIDTH, SCREEN_HEIGHT ))
pygame.display.set_caption("Kingdom Fighter")

# set framerate
clock = pygame.time.Clock()
FPS = 60

# load image
# bg img and draw bg
bg_image_main = pygame.image.load("assets/images/background/background9.jpg").convert_alpha()
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
def draw_bg(scaler_bg):
    screen.blit(scaler_bg, (0, 0))

# button img
restart_img = pygame.image.load("assets/images/background/restart.png").convert_alpha()
main_menu_img = pygame.image.load("assets/images/background/main_menu.png").convert_alpha()



# character





# load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# load win round img
p1_win_img = pygame.image.load("assets/images/icons/p1win.png").convert_alpha()
p2_win_img = pygame.image.load("assets/images/icons/p2win.png").convert_alpha()
KO_img = pygame.image.load("assets/images/icons/K.O.png").convert_alpha()



# define number of steps
WARRIOR_ANIMATION_STEPS = [10, 8 ,1 , 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8 ,1 , 8, 8, 3, 7]

# define fonts
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function for fighter heathbar
def draw_heath_bar(heath, x, y):
    ratio = heath / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 24) )
    pygame.draw.rect(screen, RED, (x, y, 400, 20))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 20))

# Create button
restart_button = Button(SCREEN_WIDTH // 2 - 165, SCREEN_HEIGHT // 2 - 50, restart_img)
main_menu_button = Button(SCREEN_WIDTH // 2 + 65, SCREEN_HEIGHT // 2 - 50, main_menu_img)




fighter_1 = Fighter(1, 200, 310, False,  WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, warrior_fx)
fighter_2 = Fighter(2, 700, 310, True,  WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, wizard_fx)

#game loop
run = True
while run:
    
    clock.tick(FPS)
    draw_bg(pygame.transform.scale(bg_image, (SCREEN_WIDTH,SCREEN_HEIGHT)))
    

    # show player stats
    draw_heath_bar(fighter_1.heath, 20, 20)
    draw_heath_bar(fighter_2.heath, 580, 20)
    
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)
    
    # update countdown
    if intro_count <= 0: 
        # move fighter
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else: 
        # display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
        
    # update fighter
    fighter_1.update()
    fighter_2.update()    
    fighter_1.draw(screen)
    fighter_2.draw(screen)
    
    # check player defeat
    WINNING_SCORE = 3
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()

        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
            
    elif score[0] == WINNING_SCORE:
        draw_bg(pygame.transform.scale(bg_image_main, (SCREEN_WIDTH,SCREEN_HEIGHT)))
        screen.blit(p1_win_img, (360, 150))
        if sound_played != True:
             P1_win_fx.play()
             sound_played = True
        if restart_button.draw(screen):
            score = [0, 0]
            round_over = False
        if main_menu_button.draw(screen):
            map_menu = True
            score = [0, 0]
            round_over = False
            intro_count = 3 
                
    elif score[1] == WINNING_SCORE:
        draw_bg(pygame.transform.scale(bg_image_main, (SCREEN_WIDTH,SCREEN_HEIGHT)))
        screen.blit(p2_win_img, (360, 150))
        if sound_played != True: 
             P2_win_fx.play()
             sound_played = True
        if restart_button.draw(screen):
            score = [0, 0]
            round_over = False
        if main_menu_button.draw(screen):
            map_menu = True
            score = [0, 0]
            round_over = False
            intro_count = 3 
            
    else: 
        screen.blit(KO_img, (390, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 310, False,  WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            fighter_2 = Fighter(2, 700, 310, True,  WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()
            
pygame.quit()