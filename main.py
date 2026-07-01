from turtle import pos

import pygame
import sys
import json
import os

from random import choices
from classes.config import *
from classes.labirinto import MapGenerator, salas, Wall, Block, Door
from classes.character import *
from classes.enemies import *
from classes.collectibles import *
from classes.hud import HUD


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (WIDTH_TELA, HEIGTH_TELA),
            pygame.FULLSCREEN | pygame.SCALED
        )
        self.clock = pygame.time.Clock()
        self.runnning = True

        self.espera_porta = 0
        # Tipo de cronômetro
        self.EVENTO_RELOGIO = pygame.USEREVENT + 1
        pygame.time.set_timer(self.EVENTO_RELOGIO, 1000)

        # Sistema de leitura do json
        diretorio_atual = os.path.dirname(__file__)
        caminho_json = os.path.join(
            diretorio_atual, 'assetes', 'dict_geral', 'items_passive.json')

        with open(caminho_json, 'r', encoding='utf-8') as f:
            self.banco_dados = json.load(f)

    # Método de sorteio
    def sortear_item(self, tipo_sala):
        itens_validos = []
        pesos = []

        for nome, dados in self.banco_dados.items():
            pool = dados.get("pool", "")
            qualidade = dados.get("qualidade", 1)

            if 'Fragmento' in nome:
                continue

            if tipo_sala in pool or 'tesouro - chefe' in pool:
                itens_validos((nome, dados))

            peso = 1.0 / max(qualidade, 0.1)
            pesos.append(peso)

        if not itens_validos:
            return None

        item_escolhido = choices(itens_validos, weights=pesos, k=1)
        return item_escolhido

    def createRoom(self, layout):
        # Primeiro para pegar a string que compõe o mapa
        for pos, row in enumerate(layout):
            # Segundo para pegar os caracteres da string
            for value, column in enumerate(row):
                if column == "W":
                    Wall(self, value, pos)
                elif column == "P":
                    if not hasattr(self, 'player') or self.player is None:
                        self.player = Player(
                            self, value, pos, self.player_status, False)
                elif column == "B":
                    Block(self, value, pos)

                elif column in ['N', 'S', 'E', 'O']:
                    Door(self, value, pos, column)
                elif column == "V":
                    if self.primeira_visita:
                        coletavelVida(self, value, pos)
                elif column == "M":
                    if self.primeira_visita:
                        coletavelTempo(self, value, pos)
                elif column == "U":
                    MulaSemCabeca(self, value, pos)
                elif column == "C":
                    Curupira(self, value, pos)
                elif column == "I":
                    Iara(self, value, pos)
                elif column == "K":
                    if self.primeira_visita:
                        Chave_temporaria(self, value, pos)
                elif column == "A":
                    chave_pos = (self.sala_atual.x, self.sala_atual.y, value, pos)
                    if chave_pos not in self.chaves_coletadas:
                        ColetavelChave(self, value, pos)
                elif column == "H":
                    Cacador(self, value, pos)

    def troca_sala(self, novo_layout):
        for sprite in self.walls:
            sprite.kill()
        for sprite in self.blocks:
            sprite.kill()
        for sprite in self.holes:
            sprite.kill()
        for sprite in self.doors:
            sprite.kill()
        for sprite in self.pedestal:
            sprite.kill()
        for sprite in self.enemies:
            sprite.kill()
        for sprite in self.pickup:
            sprite.kill()
        for sprite in self.projectiles:
            sprite.kill()

        self.sala_atual = novo_layout
        self.primeira_visita = not self.sala_atual.foi_visitada  
        self.sala_atual.foi_visitada = True

        self.createRoom(self.sala_atual.layout)

    def new(self):
        # Quando começa um novo jogo
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()

        self.walls = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.holes = pygame.sprite.LayeredUpdates()
        self.pedestal = pygame.sprite.LayeredUpdates()

        self.doors = pygame.sprite.LayeredUpdates()

        self.projectiles = pygame.sprite.LayeredUpdates()

        self.enemies = pygame.sprite.LayeredUpdates()
        self.pickup = pygame.sprite.LayeredUpdates()

        self.player = None
        self.player_status = {
            "hp_max": 30,
            "vida_extra": 0,
            "dano": 3.5,
            "multi_atq": 1.0,
            "alcance": 7.0,
            "atq_speed": 1.0,
            "frequencia": 0.0,
            "speed": 1.0,
            "qtd_proj": 1
        }

        self.chaves_coletadas = set() 

        self.aviso_porta_timer = 0

        # Define quantas salas quer no andar
        gerador = MapGenerator()
        self.map, self.sala_atual = gerador.generate(salas)

        self.primeira_visita = True  
        self.sala_atual.foi_visitada = True  

        # Carrega a sala inicial (Start Room)
        self.createRoom(self.sala_atual.layout)

        # Criação do hud depois do player, porque ele lê dados do self.player
        self.hud = HUD(self)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.runnning = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.runnning = False

                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()

            if event.type == self.EVENTO_RELOGIO:
                if self.player is not None:
                    if self.player.tempo > 0:
                        self.player.tempo -= 1
                    else:
                        self.playing = False

    def toggle_fullscreen(self):
        self.fullscreen = not getattr(self, 'fullscreen', True)
        if self.fullscreen:
            self.screen = pygame.display.set_mode(
                (WIDTH_TELA, HEIGTH_TELA), pygame.FULLSCREEN | pygame.SCALED
            )
        else:
            self.screen = pygame.display.set_mode((WIDTH_TELA, HEIGTH_TELA))

    def uptade(self):
        self.all_sprites.update()

        if self.player:
            self.check_door_collisions()
            
            #Verfica se o jogador morreu, se sim, termina o jogo
            if self.player.hp <= 0:
                self.playing = False

        if self.espera_porta > 0:
            self.espera_porta -= 1

    def draw(self):
        self.screen.fill(BLACK)
        # Textura do cenário
        self.all_sprites.draw(self.screen)

        # Desenha vida, tempo e inventário "por cima"
        self.hud.draw(self.screen)

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

    def menu(self):
        self.in_menu = True

        diretorio_atual = os.path.dirname(__file__)
        caminho_fonte = os.path.join(diretorio_atual, 'assetes', 'fonts', 'PixelifySans-Regular.ttf')
        caminho_bg = os.path.join(diretorio_atual, 'assetes', 'sprites', 'menu_bg.png')

        bg = pygame.image.load(caminho_bg).convert()
        bg = pygame.transform.scale(bg, (WIDTH_TELA, HEIGTH_TELA))

        fonte_botao = pygame.font.Font(caminho_fonte, 20)

        # Botões posicionados sobre os botões da imagem
        botao_jogar = pygame.Rect(WIDTH_TELA//2 - 100, 330, 200, 50)
        botao_como_jogar = pygame.Rect(WIDTH_TELA//2 - 100, 395, 200, 50)

        while self.in_menu and self.runnning:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.in_menu = False
                    self.runnning = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.in_menu = False
                    self.runnning = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if botao_jogar.collidepoint(mouse_pos):
                        self.in_menu = False
                        self.new()
                        self.main()
                    if botao_como_jogar.collidepoint(mouse_pos):
                        self.tela_como_jogar()

            self.screen.blit(bg, (0, 0))

            pygame.display.update()
            self.clock.tick(FPS)


    def tela_como_jogar(self):
        voltando = True

        diretorio_atual = os.path.dirname(__file__)
        caminho_fonte = os.path.join(diretorio_atual, 'assetes', 'fonts', 'PixelifySans-Regular.ttf')
        caminho_bg = os.path.join(diretorio_atual, 'assetes', 'sprites', 'como_jogar_bg.png')

        bg = pygame.image.load(caminho_bg).convert()
        bg = pygame.transform.scale(bg, (WIDTH_TELA, HEIGTH_TELA))

        fonte_texto = pygame.font.Font(caminho_fonte, 16)
        fonte_titulo = pygame.font.Font(caminho_fonte, 28)

        instrucoes = [
            "- Use WASD para se mover",
            "- Use as setas para direcionar os projeteis",
            "- Colete itens para fortalecer seu personagem",
            "- Encontre as 3 chaves para a sala f inal",
            "- Derrote os inimigos para sobreviver",
            "Pressione ESC para voltar",
        ]

        while voltando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runnning = False
                    self.in_menu = False
                    voltando = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    voltando = False

            self.screen.blit(bg, (0, 0))

            titulo = fonte_titulo.render("Como Jogar:", True, WHITE)
            self.screen.blit(titulo, titulo.get_rect(center=(WIDTH_TELA//2, 130)))

            for i, linha in enumerate(instrucoes):
                texto = fonte_texto.render(linha, True, WHITE)
                self.screen.blit(texto, texto.get_rect(center=(WIDTH_TELA//2, 165 + i*35)))

            pygame.display.update()
            self.clock.tick(FPS)
    def check_door_collisions(self):
        # O 'False' significa que a porta NÃO será deletada ao ser tocada
        hits = pygame.sprite.spritecollide(self.player, self.doors, False)

        if hits and not self.espera_porta > 0:
            # Pega a primeira porta que o jogador encostou
            porta_tocada = hits[0]
            direcao = porta_tocada.direcao

            # Verifica qual é a sala vizinha nessa direção
            nova_sala = self.sala_atual.vizinho[direcao]


            # Se a sala existir, fazemos a transição
            if nova_sala:
                # Verifica se é a sala final e se o jogador tem as 3 chaves
                if nova_sala == salas[(2, -2)] and self.player.inventario.contagem_chave < 3:
                    self.aviso_porta_timer = 180 
                    return  # Bloqueia a passagem

                self.troca_sala(nova_sala)

                if direcao == 'N':
                    self.player.rect.x = 10 * TILESIZE
                    self.player.rect.y = 13 * TILESIZE
                    self.espera_porta = 20

                elif direcao == 'S':
                    self.player.rect.x = 10 * TILESIZE
                    self.player.rect.y = 1 * TILESIZE
                    self.espera_porta = 20

                elif direcao == 'E':
                    self.player.rect.x = 1 * TILESIZE
                    self.player.rect.y = 13 * TILESIZE
                    self.espera_porta = 20

                elif direcao == 'O':
                    self.player.rect.x = 19 * TILESIZE
                    self.player.rect.y = 13 * TILESIZE
                    self.espera_porta = 20


g = Game()
g.intro_screen()

while g.runnning:
    g.menu()

pygame.quit()
sys.exit()