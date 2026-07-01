import pygame
import random
import os

from classes.config import *
from classes.collectibles import *


#Dicionário das salas:
salas_layout = {
    (0, 0): [
        "WWWWWWWWWWNWWWWWWWWWW",
        "W...................W",
        "W...................W",
        "W...................W",
        "W...................W",
        "W...................W",
        "W...................W",
        "W.........P.........W",
        "W...................W",
        "W...................W",
        "W...................W",
        "W...................W",
        "W...................W",
        "W...................W",
        "WWWWWWWWWWWWWWWWWWWWW"
    ],

    (0, -1): [
        "WWWWWWWWWWNWWWWWWWWWW",
        "WV..IW.............MW",  
        "W.W.W.WWWWWWWWWWWWW.W",
        "W.W.W.WI....W..A.V..W",
        "W.WWW.WWW.W.W.WWWWW.W",
        "WM.IWM....W..MWI....W",
        "W.W.WWWWWWWWWWW.WWWWW",
        "W.W........V..W.W..IW",
        "W.WWWWWWWWW.W.W.W.WWW",
        "W.WI...M..W.W.W.WV..W",
        "W.WWW.WWW.W.W.W.WWW.W",
        "W.....WIW.W.WIW.W...W",
        "WWWWWWW.W.W.WWW.W.W.W",
        "WV..................W",
        "WWWWWWWWWWSWWWWWWWWWW"
 ],

    (0, -2): [
        "WWWWWWWWWWWWWWWWWWWWW",
        "WC......W..........CW",
        "W.W.WWWWW.WWWWWWW.WWW",
        "W.WM...........VW...W",
        "W.WWWWWWWWWWWWWWWWW.W",
        "WM........W.......W.W",
        "WWWWWWWWW.W.WWWWW.W.W",
        "W.......WCW.W..VW...W",
        "W.WWWWW.WWW.W.WWWWW.W",
        "W...WC......W....CW.W",
        "WWW.W.WWWWWWW.W.WWW.W",
        "W...WMWM...VW.W.....W",
        "W.WWWWW.WWW.W.WWWWWWW",
        "WA..........WM......E", 
        "WWWWWWWWWWSWWWWWWWWWW",
    ],

    (1, -2): [
        "WWWWWWWWWWWWWWWWWWWWW",
        "W..UM..V.......MW...W",
        "W.W.W.W.W.W.WWW.W.W.W",
        "W.W...W.WV..W...WVW.W",
        "W.WWWWW.WWWWW.WWWWW.W",
        "W...W......UW.WU.M..W",
        "WWWWW.WWWWW.W.W.WWW.W",
        "WM....W...W.W...WUW.W",
        "W.WWWWW.W.W.WWWWW.W.W",
        "W.W....MW.........W.W",
        "W.W.WWWWWWWWWWWWW.W.W",
        "W.W.....WU..A..V...VW",
        "W.WWWWW.WWWWWWW.WWWWW",
        "O.............W.....E", 
        "WWWWWWWWWWWWWWWWWWWWW"
    ],

    (2, -2): [
        "WWWWWWWWWWWWWWWWWWWWW",
        "W...................W",
        "W...................W",
        "W...................W",
        "W...................W",
        "W.............H.....W",
        "W...................W",
        "W...................W",
        "W...................W",
        "W...................W",
        "W...................W",
        "W...................W",
        "O...................W",
        "W...................W",
        "WWWWWWWWWWWWWWWWWWWWW"
    ]
}

class RoomNode:
    def __init__(self, x, y, layout):
        self.x = x
        self.y = y
        self.vizinho = {'N' : None, 'S' : None, 'E' : None, 'O' : None}
        self.layout = layout
        self.foi_visitada = False

#Colocar cada sala do dicionário em um roomnode:
sala_inicial = RoomNode(0,0,salas_layout[(0,0)])
sala_labirinto1 = RoomNode(0,-1,salas_layout[(0,-1)])
sala_labirinto2 = RoomNode(0,-2,salas_layout[(0,-2)])
sala_labirinto3 = RoomNode(1,-2,salas_layout[(1,-2)])
sala_final = RoomNode(2,-2,salas_layout[(2,-2)])

#Dicionário para guardar os roomnodes:
salas = {(0,0) : sala_inicial, (0,-1) : sala_labirinto1, (0, -2) : sala_labirinto2, (1,-2) : sala_labirinto3, (2,-2) : sala_final}
        

class MapGenerator:
    def __init__(self):
        self.grid = {}
        self.map = []

    def generate(self, salas):
        #Primeira sala, vai ser a já definida:
        start_room = salas[(0,0)]
        self.grid[(0, 0)] = start_room
        sala_anterior = (0, 0)
        self.map.append(self.grid[(0,0)])
      

        for chave in salas:
            if chave != (0,0):
                nova_sala = salas[chave]
                self.grid[chave] = nova_sala

                #procurar direção do vizinho:
                x = int(chave[0]) - int(sala_anterior[0])
                y = int(chave[1]) - int(sala_anterior[1])

                if(x != 0):
                    if(x == -1):
                        vizinho_novo = 'E'
                        vizinho_anterior = 'O'
                    else:
                        vizinho_novo = 'O'
                        vizinho_anterior = 'E'
                else:
                    if(y == -1):
                        vizinho_novo = 'S'
                        vizinho_anterior = 'N'
                    else:
                        vizinho_novo = 'N'
                        vizinho_anterior = 'S'
                    
                #Atualizar os vizinhos
                self.grid[sala_anterior].vizinho[vizinho_anterior] = nova_sala
                nova_sala.vizinho[vizinho_novo] = self.grid[sala_anterior]

                #Guardar a sala anterior
                sala_anterior = chave

                self.map.append(self.grid[chave])

        return self.map, start_room

class Wall(pygame.sprite.Sprite):
    # Carrega a imagem uma única vez para todos os tiles 
    _imagem_tileset = None

    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = (self.game.all_sprites, self.game.walls)
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        if Wall._imagem_tileset is None:
            diretorio_atual = os.path.dirname(__file__)
            caminho = os.path.join(diretorio_atual, '..', 'assetes', 'sprites', 'treepacknewest.png')
            Wall._imagem_tileset = pygame.image.load(caminho).convert_alpha()

        tile = Wall._imagem_tileset.subsurface(pygame.Rect(96, 320, 64, 64))

        self.image = pygame.transform.scale(tile, (TILESIZE, TILESIZE))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.group = self.game.all_sprites, self.game.blocks

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        # Marrom em RGB
        self.image.fill((146, 142, 133))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y



class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direcao):

        self.game = game
        self._layer = DOOR_LAYER
        self.group = self.game.all_sprites, self.game.doors

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.direcao = direcao

        if self.direcao in ['O', 'E']:
            self.width = 32
            self.height = 48
        else:
            self.width = 48
            self.height = 32

        self.image = pygame.Surface([self.width, self.height])
        # Cinza em RGB
        self.image.fill((139, 139, 139))

        self.rect = self.image.get_rect()

        if self.direcao == 'O':
            self.rect.midleft = (self.x, self.y + TILESIZE // 2)

        elif self.direcao == 'E':
            self.rect.midright = (self.x + TILESIZE, self.y + TILESIZE // 2)

        elif self.direcao == 'N':
            self.rect.midtop = (self.x + TILESIZE // 2, self.y)

        elif self.direcao == 'S':
            self.rect.midbottom = (self.x + TILESIZE // 2, self.y + TILESIZE)

