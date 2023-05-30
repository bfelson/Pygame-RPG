import pygame
from config import *
import math
import random

#https://tinyurl.com/penguinpython4a

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert() #convert speeds up performance

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height]) #new surface

        #display sheet on the new surface at 0,0, with properties (x,y,w,h)
        sprite.blit(self.sheet, (0,0), (x, y, width, height)) 

        sprite.set_colorkey(BLACK)
        return sprite
    
    #after making this class, go to main.py and initialize the spritesheets

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.vx = 0
        self.vy = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height) #= 32,32

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

                #load in images of animations, all located in character.png
        self.down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height),]
    
        self.up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height),]
        
        self.left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height),]
        
        self.right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height),]


    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.vx
        self.collide_blocks('x')
        self.rect.y += self.vy
        self.collide_blocks('y')

        self.collide_enemy()

        self.vx = 0
        self.vy = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED #adding x = moving right
            self.vx -= PLAYER_SPEED #keep this so that player technically stays in middle
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.vx += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.vy -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.vy += PLAYER_SPEED
            self.facing = 'down'

        
        if self.facing == 'down':
            #if standing still, set to static image
            #otherwise, from down animation loop get correct images
            if self.vy == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height) 
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                #using 0.1, animation will change every 10 frames
                self.animation_loop += 0.1
                #only 3 images in list
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            #if standing still, set to static image
            #otherwise, from down animation loop get correct images
            if self.vy == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height) 
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                #using 0.1, animation will change every 10 frames
                self.animation_loop += 0.1
                #only 3 images in list
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            #if standing still, set to static image
            #otherwise, from down animation loop get correct images
            if self.vx == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height) 
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                #using 0.1, animation will change every 10 frames
                self.animation_loop += 0.1
                #only 3 images in list
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            #if standing still, set to static image
            #otherwise, from down animation loop get correct images
            if self.vx == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height) 
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                #using 0.1, animation will change every 10 frames
                self.animation_loop += 0.1
                #only 3 images in list
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill() #test for now
            self.game.playing = False

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) #check if player rect inside of blocks rect, false means dont delete on collide
            if hits:
                if self.vx > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.rect.x = hits[0].rect.right
            
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False) #check if player rect inside of blocks rect, false means dont delete on collide
            if hits:
                if self.vy > 0: #down
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.vx = 0
        self.vy = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1 #add last
        self.movement_loop = 0 #add last
        self.max_travel = random.randint(7, 30) #back and forth between 7 and 30 pixels

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 2, self.width, self.height),]
    
        self.up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 34, self.width, self.height),]
        
        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 98, self.width, self.height),]
        
        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite(68, 66, self.width, self.height),]
        
    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.vx
        self.rect.y += self.vy

        self.vx = 0
        self.vy = 0
        #remember to add to create_tilemap at this point, plus put E in tilemap

    def movement(self):
        if self.facing == 'left':
            self.vx -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.vx += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):
        if self.facing == 'left':
            #if standing still, set to static image
            #otherwise, from down animation loop get correct images
            if self.vx == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height) 
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                #using 0.1, animation will change every 10 frames
                self.animation_loop += 0.1
                #only 3 images in list
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            #if standing still, set to static image
            #otherwise, from down animation loop get correct images
            if self.vx == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height) 
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                #using 0.1, animation will change every 10 frames
                self.animation_loop += 0.1
                #only 3 images in list
                if self.animation_loop >= 3:
                    self.animation_loop = 1




class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        #self.image = pygame.Surface([self.width, self.height])
        #self.image.fill(BLUE)
        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('Roboto-Regular.ttf', fontsize)
        self.content = content
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg #foreground
        self.bg = bg #background

        self.image = pygame.Surface((self.width, self.height)) #pygame rect
        self.image.fill(self.bg)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)#second parameter is anti-aliasing
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect) #draw text onto text rect

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]: #left clicking
                return True
            return False;
        return False