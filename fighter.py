import pygame
class Fighter():
    def __init__(self, player, x, y, flip,  data, sprite_sheet, animation_steps, sound_fx):
        self.attack_sound = sound_fx
        self.player = player
        self.size = data[0]   
        self.image_scale = data[1] 
        self.offset = data[2] 
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0

        self.hit = False
        self.heath = 100
        self.mana = 0
        self.alive = True
        
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
  
    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0 
        dy = 0
        self.running = False
        self.attack_type = 0
        
        
        #get key_presses
        key = pygame.key.get_pressed()
        # can only performe other actions when not attacking
        if self.attacking == False and self.alive == True and round_over == False:
            # check player 1 control
            if self.player == 1:
                # movement
                if key[pygame.K_a]:
                    self.running = True
                    dx = -SPEED
                if key[pygame.K_d]:
                    self.running = True
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
                        
                if key[pygame.K_l] and self.mana == 100:
                    self.special_attack(surface, target)
                    self.attack_type = 3
    
             # check player 2 control
            if self.player == 2:
                # movement
                if key[pygame.K_LEFT]:
                    self.running = True
                    dx = -SPEED
                if key[pygame.K_RIGHT]:
                    self.running = True
                    dx = SPEED
            
                # jump
                if key[pygame.K_UP ] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                
                # attack
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(surface, target)
                    # determine which attack type was used
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2
                        
                if key[pygame.K_KP3] and self.mana == 100:
                    self.special_attack(surface, target)
                    self.attack_type = 3
            
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
                
        # apply attacking cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        #update player position    
        self.rect.x += dx 
        self.rect.y += dy
            
            
    # handle animation updates
    def update(self):
        # check what action the player is perform
        if self.heath <= 0:
            self.alive = False
            self.heath = 0
            self.update_actions(6)
        elif self.hit == True:
            self.update_actions(5)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_actions(3)
            elif self.attack_type == 2:
                self.update_actions(4) 
            elif self.attack_type == 3:
                self.update_actions(7)  
        elif self.jump == True:
            self.update_actions(2)
        elif self.running == True:
            self.update_actions(1)
        else:  
            self.update_actions(0)
        
        animation_cooldown = 50 # animation cooldown between each frame in one action
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        
        # check if enough time has pass since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            #  check if the player is death, then end the stay at the last frame of the death animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            #  check if an attack is execute
            if self.action == 3 or self.action == 4 or self.action == 7:
                self.attacking = False
                self.attack_cooldown = 20
            
            # check if target get hit
            if self.action == 5:
                self.hit = False
                # if player is in the middle of an attack, then attack is stop
                self.attacking = False
                self.attack_cooldown = 20
            
    
    def attack(self, surface, target) :
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect( self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect) :
                if self.mana >= 100:
                    self.mana = 100
                else: 
                    self.mana += 20
                target.hit = True
                target.heath -= 10

            # pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
        
    def special_attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect( self.rect.centerx - (3 * self.rect.width * self.flip),
                                         self.rect.y, 3 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect) :
                self.mana = 0
                target.hit = True
                target.heath -= 50
            
        
    def update_actions(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            
            # reset frame_index and update_time to start counting with the new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
        
        
    def draw(self, surface):
        # flip img for character to face each other
        img = pygame.transform.flip(self.image, self.flip, False) 
        # pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))