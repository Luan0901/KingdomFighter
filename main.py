import pygame
from fighter import Fighter
from pygame import mixer
from button import Button
mixer.init()
pygame.init()

# declare screen resolution
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# create game window
screen = pygame.display.set_mode(( SCREEN_WIDTH, SCREEN_HEIGHT ))
pygame.display.set_caption("Kingdom Fighter")

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define game varriables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0 , 0] # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
sound_played = False

main_menu = True
map_menu = False
map_selected = False
map_selected_index = None 


# define fighter varriables
# data 
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# define number of steps each character
WARRIOR_ANIMATION_STEPS = [10, 8 ,1 , 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8 ,1 , 8, 8, 3, 7]

# define fonts and colors
count_font = pygame.font.Font("assets/fonts/turok.ttf", 50)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Load music and sounds
pygame.mixer.music.load("assets/audio/music1.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
warrior_fx = pygame.mixer.Sound("assets/audio/warrior.mp3")
wizard_fx = pygame.mixer.Sound("assets/audio/magic.wav")
P1_win_fx = pygame.mixer.Sound("assets/audio/player-1-wins.mp3")
P2_win_fx = pygame.mixer.Sound("assets/audio/player-2-wins.mp3")

# Load image
# map image and main menu image
bg_image_main = pygame.image.load("assets/images/background/background9.jpg").convert_alpha()
map1_img = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
map2_img = pygame.image.load("assets/images/background/background1.jpg").convert_alpha()
map3_img = pygame.image.load("assets/images/background/background8.jpg").convert_alpha()
map4_img = pygame.image.load("assets/images/background/background7.jpg").convert_alpha()
map5_img = pygame.image.load("assets/images/background/background4.jpg").convert_alpha()
map6_img = pygame.image.load("assets/images/background/background6.jpg").convert_alpha()

# title and button image
title = pygame.image.load("assets/images/background/Kingdom.png").convert_alpha()
start_img = pygame.image.load('assets/images/background/start.png').convert_alpha()
exit_img = pygame.image.load('assets/images/background/exit.png').convert_alpha()
restart_img = pygame.image.load('assets/images/background/restart.png').convert_alpha()
main_menu_img = pygame.image.load('assets/images/background/main_menu.png').convert_alpha()
    
# win round image
p1_win_img = pygame.image.load("assets/images/icons/p1win.png").convert_alpha()
p2_win_img = pygame.image.load("assets/images/icons/p2win.png").convert_alpha()
KO_img = pygame.image.load("assets/images/icons/K.O.png").convert_alpha()

# character image


# spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Create button
game_title = Button(SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 15, title)
start_button = Button(SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT // 3, start_img)
exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 1.8, exit_img)
restart_button = Button(SCREEN_WIDTH // 2 - 165, SCREEN_HEIGHT // 2 - 50, restart_img)
main_menu_button = Button(SCREEN_WIDTH // 2 + 65, SCREEN_HEIGHT // 2 - 50, main_menu_img)



# Functions
# drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# drawing heath and mana bar
def draw_heath_bar(heath, x, y):
    ratio = heath / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 24) )
    pygame.draw.rect(screen, RED, (x, y, 400, 20))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 20))

# draw map list
def draw_map_list(map_list):
    for i, map_image in enumerate(map_list):
        x = 150 + (i % 3) * 250
        y = 150 + (i // 3) * 150
        scaler_bg = pygame.transform.scale(map_image, (200, 120))
        screen.blit(scaler_bg, (x, y))
        if map_selected_index == i:  
            pygame.draw.rect(screen, (255, 255, 0), (x - 5, y - 5, 210, 130), 3)
            
# draw background
def draw_bg(scaler_bg):
    screen.blit(scaler_bg, (0, 0))

fighter_1 = Fighter(1, 200, 310, False,  WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, warrior_fx)
fighter_2 = Fighter(2, 700, 310, True,  WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, wizard_fx)

#game loop
run = True
while run:
    
    clock.tick(FPS)
    draw_bg(pygame.transform.scale(bg_image_main, (SCREEN_WIDTH,SCREEN_HEIGHT)))
    
    if main_menu:
        game_title.draw(screen)
        if start_button.draw(screen):
            map_menu = True
            main_menu = False
        if exit_button.draw(screen):
            run = False
            
    elif map_menu:
        draw_text("Choose your map", count_font, WHITE,SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 15)
        draw_map_list([map1_img, map2_img, map3_img, map4_img, map5_img, map6_img]) 
        if map_selected_index != None:
            map_menu = False
            
    elif map_menu == False and  main_menu == False:
        map_image = [map1_img, map2_img, map3_img, map4_img, 
                     map5_img, map6_img][map_selected_index]
        draw_bg(pygame.transform.scale(map_image, (SCREEN_WIDTH,SCREEN_HEIGHT)))
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
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 50)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()
           
        # update fighter
        fighter_1.update()
        fighter_2.update()    
        fighter_1.draw(screen)
        fighter_2.draw(screen)
        
        # check player defeat
        WINNING_SCORE = 1
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
            screen.blit(p1_win_img, (360, 150))
            if sound_played != True:
                P1_win_fx.play()
                sound_played = True
            if restart_button.draw(screen):
                score = [0, 0]
                fighter_1 = Fighter(1, 200, 310, False,  WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, warrior_fx)
                fighter_2 = Fighter(2, 700, 310, True,  WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, wizard_fx)
                intro_count = 3 
                sound_played = False
                round_over = False
            if main_menu_button.draw(screen):
                main_menu = True
                map_selected_index = None
                score = [0, 0]
                sound_played = False
                round_over = True
                intro_count = 3 
                    
        elif score[1] == WINNING_SCORE:
            screen.blit(p2_win_img, (360, 150))
            if sound_played != True: 
                P2_win_fx.play()
                sound_played = True
            if restart_button.draw(screen):
                score = [0, 0]
                fighter_1 = Fighter(1, 200, 310, False,  WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, warrior_fx)
                fighter_2 = Fighter(2, 700, 310, True,  WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, wizard_fx)
                intro_count = 3 
                round_over = False
            if main_menu_button.draw(screen):
                main_menu = True
                map_selected_index = None
                score = [0, 0]
                sound_played = False
                round_over = True
                intro_count = 3 
                
        else: 
            screen.blit(KO_img, (390, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter_1 = Fighter(1, 200, 310, False,  WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, warrior_fx)
                fighter_2 = Fighter(2, 700, 310, True,  WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, wizard_fx)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if map_menu:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, map_image in enumerate([map1_img, map2_img, map3_img, map4_img, map5_img, map6_img]):
                    map_area = pygame.Rect(150 + (i % 3) * 250, 100 + (i // 3) * 180, 200, 120)  
                    if map_area.collidepoint(mouse_x, mouse_y):
                        map_selected_index = i
                        break
            
    pygame.display.update()
            
pygame.quit()