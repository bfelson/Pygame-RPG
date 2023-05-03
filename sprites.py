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

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height) #= 32,32
        #after this line, go to block class

        #load in image
        #image_to_load = pygame.image.load('img\single.png') #single picture

        #EVENTUALLY TAKE THESE OUT
        # self.image = pygame.Surface([self.width, self.height])
        # self.image.set_colorkey(BLACK) #makes the specified color to transparent (png)
        # self.image.blit(image_to_load, (0,0)) #blit displays an image on a surface

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()

        self.rect.x += self.vx
        self.rect.y += self.vy

        self.vx = 0
        self.vy = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vx -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.vx += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.vy -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.vy += PLAYER_SPEED
            self.facing = 'down'
        
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