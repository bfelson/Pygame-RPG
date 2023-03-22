import pygame
from config import *
import math
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        print("Player Object initialized")
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

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        print("Player object updated")
        self.movement()
        print(self.facing)

        self.x += self.vx
        self.y += self.vy

        self.vx = 0
        self.vy = 0

    def movement(self):
        print("Player Object movement checked")
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
            self.vy -= PLAYER_SPEED
            self.facing = 'down'
        
