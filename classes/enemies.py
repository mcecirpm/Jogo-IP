import pygame
import random
import math
import json

from classes.config import *


class Inimigo_pausado(pygame.sprite.Sprite):
    def __init__(self, game, x, y, fly, body, hp):
        self.game = game
        self._layer = PLAYER_BODY_LAYER
        self.group = self.game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.group)

        self.width = 20
        self.height = 16

        self.x_change = 0
        self.y_change = 0

        self.x = x
        self.y = y

        self.fly = fly
        self.body = body

        self.hp = hp

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((250, 150, 50))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.pos = pygame.math.Vector2(self.rect.center)

    def uptade(self):
        pos_inimigo = pygame.math.Vector2(self.rect.center)
        pos_player = pygame.math.Vector2(self.game.player.rect.center)

        direction = pos_player - pos_inimigo

        if direction.length() > 0:
            direction = direction.normalize()

        self.pos += direction * SPEED_INIMIGO
        self.rect.center = self.pos

    def collide_walls(self, direction):
        if direction == "x":
            hits_wall = pygame.sprite.spritecollide(
                self, self.game.walls, False)

            if hits_wall:
                if self.x_change > 0:
                    self.rect.x = hits_wall[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits_wall[0].rect.right

        if direction == "y":
            hits_wall = pygame.sprite.spritecollide(
                self, self.game.walls, False)

            if hits_wall:
                if self.y_change > 0:
                    self.rect.y = hits_wall[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits_wall[0].rect.bottom
