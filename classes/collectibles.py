import pygame
# A biblioteca "os" foi importada para facilitar o caminho das sprites, criando um tipo de caminho relativo
import os

from classes.config import *


class ColetavelChave(pygame.sprite.Sprite):
    _imagem = None  

    def __init__(self, game, x, y):
        self.game = game
        self._layer = PICKUP_LAYER
        self.group = self.game.all_sprites, self.game.pickup
        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.grid_x = x
        self.grid_y = y

        if ColetavelChave._imagem is None:
            diretorio_atual = os.path.dirname(__file__)
            caminho = os.path.join(diretorio_atual, '..', 'assetes', 'sprites', 'tileset_chave.png')
            ColetavelChave._imagem = pygame.image.load(caminho).convert_alpha()

        tile_w = 128 // 3
        chave = ColetavelChave._imagem.subsurface(pygame.Rect(0, 0, tile_w, 114))
        self.image = pygame.transform.scale(chave, (TILESIZE, TILESIZE))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.tipo = 'chave'


class coletavelVida(pygame.sprite.Sprite):
    _imagem = None

    def __init__(self, game, x, y):
        self.game = game
        self._layer = PICKUP_LAYER
        self.group = self.game.all_sprites, self.game.pickup
        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        if coletavelVida._imagem is None:
            diretorio_atual = os.path.dirname(__file__)
            caminho = os.path.join(diretorio_atual, '..', 'assetes', 'sprites', 'coracao.png')
            img = pygame.image.load(caminho).convert_alpha()
            # Recorta só o coração (área central sem transparência)
            # A imagem é 1216x1216, o coração fica aproximadamente entre 200 e 1000
            recorte = img.subsurface(pygame.Rect(200, 150, 800, 900))
            coletavelVida._imagem = recorte

        self.image = pygame.transform.scale(coletavelVida._imagem, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.tipo = 'vida'

class coletavelTempo(pygame.sprite.Sprite):
    _imagem = None

    def __init__(self, game, x, y):
        self.game = game
        self._layer = PICKUP_LAYER
        self.group = self.game.all_sprites, self.game.pickup
        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        if coletavelTempo._imagem is None:
            diretorio_atual = os.path.dirname(__file__)
            caminho = os.path.join(diretorio_atual, '..', 'assetes', 'sprites', 'relogio.png')
            img = pygame.image.load(caminho).convert_alpha()
            recorte = img.subsurface(pygame.Rect(150, 150, 850, 850))
            coletavelTempo._imagem = recorte

        self.image = pygame.transform.scale(coletavelTempo._imagem, (TILESIZE, TILESIZE))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.tipo = 'tempo'
