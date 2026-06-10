import pygame
import random

from enum import Enum
from classes.config import *


class RoomType(Enum):
    PADRAO = (21, 15)
    GRANDE = (43, 31)
    L_SHAPE = (43, 31)
    CURTO_H = (9, 15)
    CURTO_V = (21, 9)
    LONGO_H = (9, 31)
    LONGO_V = (43, 9)
    I_SHAPE_H = (43, 9)
    I_SHAPE_V = (9, 43)


class SpecialRoomType(Enum):
    T_PADRAO = (21, 15)
    T_CURTO_H = (9, 15)
    T_CURTO_V = (21, 9)

    SH_PADRAO = (21, 15)

    SE_PADRAO = (21, 15)

    B_PADRAO = (21, 15)
    B_LONGO_H = (9, 31)
    B_LONGO_V = (43, 9)


class RoomNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = {'N': None, 'S': None, 'E': None, 'O': None}
        self.layout = []  # Vai guardar a lista de strings (tilemap) da sala

    def generate_layout(self):
        """Gera a matriz de strings da sala baseada nas portas."""
        LARGURA = 21
        ALTURA = 15
        layout_temp = []

        for y in range(ALTURA):
            row = ""
            for x in range(LARGURA):
                # Checa se é borda (Parede)
                if x == 0 or x == LARGURA - 1 or y == 0 or y == ALTURA - 1:
                    # Lógica para criar as portas ('O' de Open Door, por exemplo)
                    if y == 0 and x == LARGURA // 2 and self.neighbors['N']:
                        row += 'N'  # Porta Norte
                    elif y == ALTURA - 1 and x == LARGURA // 2 and self.neighbors['S']:
                        row += 'S'  # Porta Sul
                    elif x == 0 and y == ALTURA // 2 and self.neighbors['O']:
                        row += 'O'  # Porta Oeste
                    elif x == LARGURA - 1 and y == ALTURA // 2 and self.neighbors['E']:
                        row += 'E'  # Porta Leste
                    else:
                        row += 'W'  # Parede normal
                else:
                    # Miolo da sala (espaço vazio por padrão)
                    # Você pode adicionar lógica de obstáculos ('B', 'H') aqui depois
                    row += '.'
            layout_temp.append(row)

        self.layout = layout_temp


class MapGenerator:
    def __init__(self, num_rooms=7):
        self.num_rooms = num_rooms
        # Dicionário para facilitar a busca por coordenadas (x,y)
        self.grid = {}
        self.map = []  # A lista solicitada que guardará os objetos RoomNode

    def generate(self):
        # 1. Cria a sala inicial no centro (0, 0)
        start_room = RoomNode(0, 0)
        self.grid[(0, 0)] = start_room
        rooms_created = 1

        # 2. Algoritmo de "Random Walker" para posicionar as salas
        while rooms_created < self.num_rooms:
            # Pega uma sala aleatória que já existe
            rx, ry = random.choice(list(self.grid.keys()))

            # Direções: (Nome, deltaX, deltaY, Direção Oposta)
            directions = [
                ('N', 0, -1, 'S'),
                ('S', 0, 1, 'N'),
                ('E', 1, 0, 'W'),
                ('W', -1, 0, 'E')
            ]

            d_name, dx, dy, op_name = random.choice(directions)
            nx, ny = rx + dx, ry + dy

            # Se o espaço estiver vazio, cria uma sala nova
            if (nx, ny) not in self.grid:
                new_room = RoomNode(nx, ny)
                self.grid[(nx, ny)] = new_room

                # Conecta as salas no grafo
                self.grid[(rx, ry)].neighbors[d_name] = new_room
                new_room.neighbors[op_name] = self.grid[(rx, ry)]

                rooms_created += 1

        # 3. Gera o layout de strings para cada sala e preenche a lista self.map
        for coords, room in self.grid.items():
            # Para a sala inicial, vamos colocar o Player ('P') no centro
            room.generate_layout()
            if coords == (0, 0):
                # Substitui o centro pelo 'P'
                row_list = list(room.layout[7])
                row_list[10] = 'P'
                room.layout[7] = "".join(row_list)

            self.map.append(room)

        return self.map, start_room


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = WALLS_LAYER
        self.group = self.game.all_sprites, self.game.walls

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        # Marrom em RGB
        self.image.fill((150, 75, 00))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ROCK_LAYER
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


class Hole(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = HOLE_LAYER
        self.group = self.game.all_sprites, self.game.holes

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        # Cinza em RGB
        self.image.fill((50, 50, 50))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Door_Open(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = DOOR_OPEN_LAYER
        self.group = self.game.all_sprites, self.game.doors_open

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        # Cinza em RGB
        self.image.fill((139, 139, 139))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
