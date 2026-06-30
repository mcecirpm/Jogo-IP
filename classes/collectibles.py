import pygame
# A biblioteca "os" foi importada para facilitar o caminho das sprites, criando um tipo de caminho relativo
import os

from classes.config import *


class ColetavelChave(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PICKUP_LAYER
        self.group = self.game.all_sprites, self.game.pickup

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.grid_x = x   # <- adiciona
        self.grid_y = y   # <- adiciona

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255, 20, 147))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.tipo = 'chave'


class coletavelVida(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PICKUP_LAYER
        self.group = self.game.all_sprites, self.game.pickup

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.tipo = 'vida'


class coletavelTempo(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PICKUP_LAYER
        self.group = self.game.all_sprites, self.game.pickup

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.tipo = 'tempo'

class Chave_temporaria(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PICKUP_LAYER
        self.group = self.game.all_sprites, self.game.pickup

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.tipo = 'tempo'


class ItemPassivo(pygame.sprite.Sprite):
    def __init__(self, game, x, y, nome_item, dados_item):
        self.game = game
        self._layer = PICKUP_LAYER
        self.group = self.game.all_sprites, self.game.pickup

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        # Ciano (temporário, substitua pela sprite depois)
        self.image.fill((0, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.tipo = 'passivo'
        self.nome_item = nome_item
        self.dados_item = dados_item
