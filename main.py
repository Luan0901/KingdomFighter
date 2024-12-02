import pygame
from fighter import Fighter
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# define fighter varriables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]



screen = pygame.display.set_mode(( SCREEN_WIDTH, SCREEN_HEIGHT ))
pygame.display.set_caption("Kingdom Fighter")

# set framerate
clock = pygame.time.Clock()
FPS = 60

bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# load background image
def draw_bg():
    scale_bg = pygame.transform.scale(bg_image,(SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scale_bg, (0, 0))

# load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# define number of steps
WARRIOR_ANIMATION_STEPS = [10, 8 ,1 , 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8 ,1 , 8, 8, 3, 7]

# function for fighter heathbar
def draw_heath_bar(heath, x, y):
    ratio = heath / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 24) )
    pygame.draw.rect(screen, RED, (x, y, 400, 20))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 20))
    
fighter_1 = Fighter(200, 310, False,  WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
fighter_2 = Fighter(700, 310, True,  WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)

#game loop
run = True
while run:
    
    clock.tick(FPS)
    draw_bg()
    
    # show player stats
    draw_heath_bar(fighter_1.heath, 20, 20)
    draw_heath_bar(fighter_2.heath, 580, 20)
    
    
    
    #move fighters
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
    # fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
    
    fighter_1.draw(screen)
    fighter_2.draw(screen)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()
            
pygame.quit()