import pygame

from classes.config import *


class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PICKUP_LAYER
        self.group = self.game.all_sprites, self.game.pickup

        pygame.sprite.Sprite.__init__(self, self.group)

        self.width = 16
        self.height = 16

        self.x = x
        self.y = y

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((140, 140, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Bomb(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PICKUP_LAYER
        self.group = self.game.all_sprites, self.game.pickup

        pygame.sprite.Sprite.__init__(self, self.group)

        self.width = 16
        self.height = 16

        self.x = x
        self.y = y

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((200, 200, 200))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
