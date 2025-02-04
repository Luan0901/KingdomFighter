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
sound_played = False # Make sure not to loop fx
map_selected_index = None  # index of the selected map in map list
player_selection = 0 # 1: Warrior, 2: Wizard, 3: Hero, 4: Knight

# state
main_menu = True 
map_menu = False
map_selected = False
character_selection = False

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

MARTIALHERO_SIZE = 200
MARTIALHERO_SCALE = 3.45
MARTIALHERO_OFFSET = [85, 71.5]
MARTIALHERO_DATA = [MARTIALHERO_SIZE, MARTIALHERO_SCALE, MARTIALHERO_OFFSET]

KNIGHT_SIZE = 180
KNIGHT_SCALE = 3.45
KNIGHT_OFFSET = [78, 62.7]
KNIGHT_DATA = [KNIGHT_SIZE, KNIGHT_SCALE, KNIGHT_OFFSET]

# define number of steps each character
WARRIOR_ANIMATION_STEPS = [10, 8 ,3 , 7, 7, 3, 7, 8]
WIZARD_ANIMATION_STEPS = [8, 8 ,1 , 8, 8, 3, 7, 16]
MARTIALHERO_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6, 12]
KNIGHT_ANIMATION_STEPS = [11, 8, 3, 7, 7, 4, 11, 14]  

# define fonts and colors
count_font = pygame.font.Font("assets/fonts/turok.ttf", 50)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Load music and sounds
pygame.mixer.music.load("assets/audio/music1.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
warrior_fx = pygame.mixer.Sound("assets/audio/warrior.mp3")
wizard_fx = pygame.mixer.Sound("assets/audio/magic.wav")
knight_fx = pygame.mixer.Sound("assets/audio/knight.mp3")
hero_fx = pygame.mixer.Sound("assets/audio/hero.wav")
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

# character image for character selection
character1_img = pygame.image.load("assets/images/background/character1.png").convert_alpha()
scaled_character1_img = pygame.transform.scale(character1_img, (275, 275))
character2_img = pygame.image.load("assets/images/background/character2.png").convert_alpha()
scaled_character2_img = pygame.transform.scale(character2_img, (250, 250))
character3_img = pygame.image.load("assets/images/background/character3.png").convert_alpha()
scaled_character3_img = pygame.transform.scale(character3_img, (200, 200))
character4_img= pygame.image.load("assets/images/background/character4.png").convert_alpha()
scaled_character4_img = pygame.transform.scale(character4_img, (250, 250))  

# spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
martialhero_sheet = pygame.image.load("assets/images/martialhero/Sprites/martialhero.png").convert_alpha()
knight_sheet = pygame.image.load("assets/images/knight/Sprites/knight.png").convert_alpha()

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
    
def draw_mana_bar(mana, x, y):
    ratio = mana / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 104, 14) )
    pygame.draw.rect(screen, WHITE, (x, y, 100, 10))
    pygame.draw.rect(screen, BLUE, (x, y, 100 * ratio, 10))
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

# choose character
def character_selection_screen():
    global player_selection
    selected_character = None
    while selected_character is None:
        warrior_button_rect = pygame.Rect(50, 100, 200, 200)
        screen.blit(scaled_character1_img, warrior_button_rect)
        wizard_button_rect = pygame.Rect(600, 50, 200, 200)
        screen.blit(scaled_character2_img, wizard_button_rect)
        martialhero_button_rect = pygame.Rect(600, 350, 200, 200)
        screen.blit(scaled_character3_img, martialhero_button_rect)
        knight_button_rect = pygame.Rect(50, 350, 200, 200)
        screen.blit(scaled_character4_img, knight_button_rect)
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if warrior_button_rect.collidepoint(x, y):
                    selected_character = "Warrior"
                    player_selection = 1
                elif wizard_button_rect.collidepoint(x, y):
                    selected_character = "Wizard"
                    player_selection = 2
                elif martialhero_button_rect.collidepoint(x, y):
                    selected_character = "Hero"
                    player_selection = 3
                elif knight_button_rect.collidepoint(x, y):
                    selected_character = "Knight"
                    player_selection = 4
                    
        draw_text("Select Character ", count_font, RED, SCREEN_WIDTH / 2 - 200, 50)
       
        character_data = {
            1: ("Warrior", 120, 270),
            2: ("Wizard", 650, 270),
            3: ("Hero", 650, 520),
            4: ("Knight", 120, 520)
        }

        for key, (name, x, y) in character_data.items():
            if player_selection == key:
                draw_text(name, count_font, RED, x, y)
            else:
                draw_text(name, count_font, WHITE, x, y)

        pygame.display.update()
        clock.tick(FPS)

    return selected_character  

character_data = {
    "Warrior": (WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, warrior_fx),
    "Wizard": (WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, wizard_fx),
    "Hero": (MARTIALHERO_DATA, martialhero_sheet, MARTIALHERO_ANIMATION_STEPS, hero_fx),
    "Knight": (KNIGHT_DATA, knight_sheet, KNIGHT_ANIMATION_STEPS, knight_fx),
}

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
            character_selection = True

    elif character_selection:
        selected_character_p1 = character_selection_screen()
        if selected_character_p1 in character_data:
            data, sheet, animation_steps, fx = character_data[selected_character_p1]
            fighter_1 = Fighter(1, 200, 310, False, data, sheet, animation_steps, fx)
            
        selected_character_p2 = character_selection_screen()
        if selected_character_p2 in character_data:
            data, sheet, animation_steps, fx = character_data[selected_character_p2]
            fighter_2 = Fighter(2, 700, 310, True, data, sheet, animation_steps, fx)
        
        if selected_character_p1 != None and selected_character_p2 != None:
            character_selection = False
    
    elif map_menu == False and main_menu == False and character_selection == False:
        map_image = [map1_img, map2_img, map3_img, map4_img, map5_img, map6_img][map_selected_index]
        draw_bg(pygame.transform.scale(map_image, (SCREEN_WIDTH,SCREEN_HEIGHT)))
        
        # show player stats
        draw_heath_bar(fighter_1.heath, 20, 20)
        draw_heath_bar(fighter_2.heath, 580, 20)
        draw_mana_bar(fighter_1.mana, 20, 45)
        draw_mana_bar(fighter_2.mana, 580, 45)
        
        # score
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
            screen.blit(p1_win_img, (360, 150))
            if sound_played != True:
                P1_win_fx.play()
                sound_played = True
                
            if restart_button.draw(screen):
                score = [0, 0]
                intro_count = 3 
                sound_played = False
                round_over = False
                if selected_character_p1 in character_data:
                    data, sheet, animation_steps, fx = character_data[selected_character_p1]
                    fighter_1 = Fighter(1, 200, 310, False, data, sheet, animation_steps, fx)
                if selected_character_p2 in character_data:
                    data, sheet, animation_steps, fx = character_data[selected_character_p2]
                    fighter_2 = Fighter(2, 700, 310, True, data, sheet, animation_steps, fx)
                
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
                intro_count = 3 
                round_over = False
                if selected_character_p1 in character_data:
                    data, sheet, animation_steps, fx = character_data[selected_character_p1]
                    fighter_1 = Fighter(1, 200, 310, False, data, sheet, animation_steps, fx)
                if selected_character_p2 in character_data:
                    data, sheet, animation_steps, fx = character_data[selected_character_p2]
                    fighter_2 = Fighter(2, 700, 310, True, data, sheet, animation_steps, fx)
                    
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
                if selected_character_p1 in character_data:
                    data, sheet, animation_steps, fx = character_data[selected_character_p1]
                    fighter_1 = Fighter(1, 200, 310, False, data, sheet, animation_steps, fx)
                if selected_character_p2 in character_data:
                    data, sheet, animation_steps, fx = character_data[selected_character_p2]
                    fighter_2 = Fighter(2, 700, 310, True, data, sheet, animation_steps, fx)
                
        
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