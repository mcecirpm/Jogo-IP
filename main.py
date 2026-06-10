import pygame
import sys
import json

from classes.config import *
from classes.salas import *
from classes.character import *
from classes.enemies import *
from classes.collectibles import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH_TELA, HEIGTH_TELA))
        self.clock = pygame.time.Clock()
        self.runnning = True

    def createRoom(self, layout):
        # Primeiro para pegar a string que compõe o mapa
        for pos, row in enumerate(layout):
            # Segundo para pegar os caracteres da string
            for value, column in enumerate(row):
                if column == "W":
                    Wall(self, value, pos)
                elif column == "P":
                    if not hasattr(self, 'player') or self.player is None:
                        self.player = Player(self, value, pos, True)
                    else:
                        self.player.rect.x = value * TILESIZE
                        self.player.rect.y = pos * TILESIZE
                elif column == "H":
                    Hole(self, value, pos)
                elif column == "B":
                    Block(self, value, pos)
                elif column in ['N', 'S', 'E', 'O']:
                    Door_Open(self, value, pos)

    def troca_sala(self, novo_layout):
        # Função para trocar a sala, destruindo os sprites atuais e criando novos com base no layout fornecido
        # Limpar as paredes, blocos, buracos atuais e portas abertas
        for sprite in self.walls:
            sprite.kill()
        for sprite in self.blocks:
            sprite.kill()
        for sprite in self.holes:
            sprite.kill()
        for sprite in self.door_open:
            sprite.kill()

        # Atualiza a sala atual
        self.current_room = novo_layout
        # Carrega o novo layout
        self.createRoom(self.current_room.layout)

    def new(self):
        # Quando começa um novo jogo
        self.playing = True

        self.andar = 1

        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.walls = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.holes = pygame.sprite.LayeredUpdates()

        self.doors_open = pygame.sprite.LayeredUpdates()
        self.doors_closed = pygame.sprite.LayeredUpdates()

        self.projectiles = pygame.sprite.LayeredUpdates()

        self.enemies = pygame.sprite.LayeredUpdates()
        self.pickup = pygame.sprite.LayeredUpdates()

        self.player = None

        # Define quantas salas quer no andar
        gerador = MapGenerator(num_rooms=8)
        self.map, self.current_room = gerador.generate()

        # Carrega a sala inicial (Start Room)
        self.createRoom(self.current_room.layout)

    def events(self):
        # Game loop event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.runnning = False

    def uptade(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # Loop do jogo
        while self.playing:
            self.events()
            self.uptade()
            self.draw()
        self.runnning = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass


g = Game()
g.intro_screen()
g.new()

while g.runnning:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
