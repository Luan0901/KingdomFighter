import pygame
class Fighter():
    def __init__(self, x, y, flip,  data, sprite_sheet, animation_steps):
        # data[0] refer to frame size in each row in sprite_sheet
        # data[1] refer to image scale, each character has they own scale depend on the sprie_sheet
        # data[2] refer to image offset 
        self.size = data[0]   
        self.image_scale = data[1] 
        self.offset = data[2] 
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        
        # actions are refered to each row in sprite_ sheet 
        #  0: idle, 
        #  1: run, 
        #  2: jump, 
        #  3: attack 1, 
        #  4: attack 2, 
        #  5: get hit, 
        #  6: death
        self.action = 0 
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.heath = 100
        
    def load_images(self, sprite_sheet, animation_steps):
        # extract animation from sprite sheet 
        animation_list = []
        # enumerate return a objects that have index, value of the iterable objects
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size ,self.size ,self.size)
                
                # changing each frame in animation with scale (different character will have different size scale)
                # then add it into temp_img_list which is each row in sprite_sheet
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))    
            animation_list.append(temp_img_list) 
        return animation_list
  
    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0 
        dy = 0
        
        #get key_presses
        key = pygame.key.get_pressed()
        # can only performe other actions when not attacking
        if self.attacking == False:
            
            # movement
            if key[pygame.K_a]:
                dx = -SPEED
            if key[pygame.K_d]:
                dx = SPEED
        
            # jump
            if key[pygame.K_w ] and self.jump == False:
                self.vel_y = -30
                self.jump = True
            
            # attack
            if key[pygame.K_j] or key[pygame.K_k]:
                self.attack(surface, target)
                # determine which attack type was used
                if key[pygame.K_j]:
                    self.attack_type = 1
                if key[pygame.K_k]:
                    self.attack_type = 2
            
            self.vel_y += GRAVITY
            dy += self.vel_y 
        
            # ensure player on screen
            if self.rect.left + dx < 0:
                dx = -self.rect.left
                
            if self.rect.right + dx > screen_width:
                dx = screen_width - self.rect.right
                
            if self.rect.bottom + dy > screen_height - 110:
                self.vel_y = 0
                self.jump = False
                dy = screen_height - 110 - self.rect.bottom
                
            if self.rect.top + dy < 0:
                self.vel_y = 0
                dy = -self.rect.top
            
            # ensure players face each other
            if target.rect.centerx < self.rect.centerx:
                self.flip = True
            else:
                self.flip = False
            
            #update player position    
            self.rect.x += dx 
            self.rect.y += dy
    
    def attack(self, surface, target) :
        self.attacking = True
        attacking_rect = pygame.Rect( self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect) :
            target.heath -= 10

        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
        
        
    def draw(self, surface):
        # flip img for character to face each other
        img = pygame.transform.flip(self.image, self.flip, False) 
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))