import pygame
import random
import math
import json

from classes.config import *


class BolaDeFogo(pygame.sprite.Sprite):  # classe para os projeteis da mula sem cabeça

    def __init__(self, game, x, y, dx, dy):

        self.game = game

        self._layer = PROJ_LAYER
        self.group = self.game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.group)

        # quadrado laranja da bola de fogo
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 120, 0))

        self.rect = self.image.get_rect()
        self.rect.centerx = x  # onde a bola de fogo nasce
        self.rect.centery = y

        self.dx = dx  # direção do projétil, normalizada
        self.dy = dy

        self.speed = 5  # coloquei a velocidade 5, mas pode ser ajustada para ficar melhor

    def update(self):

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        if self.rect.colliderect(self.game.player.rect):
            self.game.player.hp = max(0, self.game.player.hp - 3)  # dá dano ao jogador
            self.kill()  # destrói o projétil ao colidir com o jogador

        if pygame.sprite.spritecollide(self, self.game.walls, False):
            self.kill()

# Inimigo perseguidor


class MulaSemCabeca(pygame.sprite.Sprite):  # classe para a mula sem cabeça
    def __init__(self, game, x, y):

        self.game = game

        self._layer = PLAYER_LAYER
        self.group = self.game.all_sprites, self.game.enemies

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        # aparencia do quadrado laranja representando a mula sem cabeça
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((255, 100, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # posição inicial da mula sem cabeça para que ela possa voltar para lá caso o jogador se afaste
        self.pos_inicial_x = self.x
        self.pos_inicial_y = self.y

        self.hitbox = self.rect.copy()
        self.speed = 2
        self.cooldown_tiro = 0

        self.hp = 9 # a mula tem 9 vidas
        self.invencivel_timer = 0 # p ñ morrer com 1 clique

        self.perseguindo = False # flag para saber se a mula sem cabeça está perseguindo o jogador

    # a mula sem cabeça não recebe dano, então esse método é só um placeholder para evitar erros caso o jogador tente atacar ela
    def take_damage(self, damage):
        if self.invencivel_timer == 0:
            self.hp -= damage
            self.invencivel_timer = 15 #fica invencivel por alguns frames

            if self.hp <= 0:
                self.kill()  # a mula sem cabeça morre se a vida chegar a zero

    def visao_limpa(self, player):
        mula_centro = self.rect.center
        jogador_centro = player.rect.center

        tolerancia = TILESIZE // 2  # tolerância para considerar que a linha de visão está limpa

        no_mesmo_eixo_x = abs(mula_centro[1] - jogador_centro[1]) < tolerancia
        no_mesmo_eixo_y = abs(mula_centro[0] - jogador_centro[0]) < tolerancia

        if not no_mesmo_eixo_x and not no_mesmo_eixo_y:
            return False
        
        if no_mesmo_eixo_x:
            x1 = min(mula_centro[0], jogador_centro[0])
            x2 = max(mula_centro[0], jogador_centro[0])
            raio_de_visao_rect = pygame.Rect(x1, mula_centro[1] - 2, x2 - x1, 4)  # cria um retângulo horizontal de 4 pixels de altura
        else:
            y1 = min(mula_centro[1], jogador_centro[1])
            y2 = max(mula_centro[1], jogador_centro[1])
            raio_de_visao_rect = pygame.Rect(mula_centro[0] - 2, y1, 4, y2 - y1)  # cria um retângulo vertical de 4 pixels de largura

        for parede in self.game.walls: # verifica se há alguma parede entre a mula sem cabeça e o jogador
            if raio_de_visao_rect.colliderect(parede.rect):
                return False  # há uma parede entre a mula sem cabeça e o jogador

        return True  # a visão está limpa

    def update(self):
        if self.invencivel_timer > 0: #diminui o timer de invencinilidade se tomou dano há pouco
            self.invencivel_timer -= 1
            if self.invencivel_timer == 0:
                self.image.fill((255, 100, 0))  # volta a cor original da mula sem cabeça

        player = self.game.player
        if player is None:
            return

        # diferença de posições entre a mula sem cabeça e o jogador
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        distancia = math.sqrt(dx**2 + dy**2)

        raio_de_visao = 180 # raio de visão da mula sem cabeça em 180 pixels
        distancia_minima = 45

        x_distancia = 0
        y_distancia = 0

        if not self.perseguindo:
            if distancia <= raio_de_visao and self.visao_limpa(player):
                self.perseguindo = True

        if self.perseguindo:
            if distancia > distancia_minima:
                if self.rect.centerx < player.rect.centerx:
                    x_distancia += self.speed
                elif self.rect.centerx > player.rect.centerx:
                    x_distancia -= self.speed

                if self.rect.centery < player.rect.centery:
                    y_distancia += self.speed
                elif self.rect.centery > player.rect.centery:
                    y_distancia -= self.speed
            else:
                x_distancia = 0
                y_distancia = 0

        self.rect.x += x_distancia
        colidiu_x = self.collide_walls('x', x_distancia)
        self.rect.y += y_distancia
        colidiu_y = self.collide_walls('y', y_distancia)

        if self.perseguindo and distancia > distancia_minima and (colidiu_x or colidiu_y):
            if colidiu_x and not colidiu_y:
                self.rect.y += self.speed if dy > 0 else -self.speed
                self.collide_walls('y', self.speed if dy > 0 else -self.speed)
            elif colidiu_y and not colidiu_x:
                self.rect.x += self.speed if dx > 0 else -self.speed
                self.collide_walls('x', self.speed if dx > 0 else -self.speed)

        self.hitbox = self.rect.copy()

        # A mula sem cabeça atira projéteis em direção ao jogador se ele estiver dentro de um certo alcance
        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1

        if self.cooldown_tiro == 0 and self.perseguindo:
            if distancia < raio_de_visao:
                dx_tiro = player.rect.centerx - self.rect.centerx
                dy_tiro = player.rect.centery - self.rect.centery
                distancia_tiro = (dx_tiro**2 + dy_tiro**2)**0.5

                if distancia_tiro > 0:
                    dx_tiro /= distancia_tiro  # normalização do vetor direção
                    dy_tiro /= distancia_tiro

                    BolaDeFogo(
                        self.game,
                        self.rect.centerx,
                        self.rect.centery,
                        dx_tiro,
                        dy_tiro
                    )

                    self.cooldown_tiro = 120  # espera um tempo de +- 2 segundos antes de atirar novamente, limitando a quantidade de projéteis na tela e dando uma chance para o jogador se esquivar

    def collide_walls(self, direcao, distancia):
        bateu_parede = pygame.sprite.spritecollide(self, self.game.walls, False)
        if bateu_parede:
            if direcao == 'x':
                if distancia > 0:  # movendo para a direita
                    self.rect.x = bateu_parede[0].rect.left - self.rect.width
                if distancia < 0:  # movendo para a esquerda
                    self.rect.x = bateu_parede[0].rect.right
            if direcao == 'y':
                if distancia > 0:  # movendo para baixo
                    self.rect.y = bateu_parede[0].rect.top - self.rect.height
                if distancia < 0:  # movendo para cima
                    self.rect.y = bateu_parede[0].rect.bottom

            return True
        return False

# Criando a Iara:
class Poder(pygame.sprite.Sprite):

    def __init__(self, game, x, y):

        self.game = game

        # Ajeitar a imagem do ataque
        self._layer = PROJ_LAYER
        self.group = self.game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.group)

        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Ajeitar as distancias para ficar proporcional o quanto anda
        player = self.game.player
        distancia = ((self.rect.centerx - player.rect.centerx) **2 + (self.rect.centery - player.rect.centery)**2)**0.5
        if distancia == 0:
            self.dx = 0
            self.dy = 0
        else:
            self.dx = (player.rect.centerx - self.rect.centerx)/distancia
            self.dy = (player.rect.centery - self.rect.centery)/distancia

        # Uma velocidade qualquer, podemos mudar depois qualquer coisa
        self.speed = 7

    def update(self):

        # Ele anda um pouco dependendo da velocidade
        self.rect.centerx += self.dx * self.speed
        self.rect.centery += self.dy * self.speed

        # Verifica se houve colisão ou com o jogador(para diminuir o tempo) ou com a parede (para desaparecer)
        if self.rect.colliderect(self.game.player.rect):
            # Diminui a princípio em 10 segundos, mas a gente pode mudar
            self.game.player.tempo -= 10
            self.kill()

        if pygame.sprite.spritecollide(self, self.game.walls, False):
            self.kill()

class Iara(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game

        # Ajeitar a imagem e as informações principais da iara
        self.x = x*TILESIZE
        self.y = y*TILESIZE

        self._layer = PLAYER_LAYER
        self.group = self.game.all_sprites, self.game.enemies

        pygame.sprite.Sprite.__init__(self, self.group)

        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect()
        self.rect.centerx = self.x + TILESIZE // 2
        self.rect.centery = self.y + TILESIZE // 2

        # Começamos com zero para poder atacar logo
        self.cooldown_tiro = 0

        self.hitbox = self.rect.copy()

    def take_damage(self, damage):  # Só para não dar erro
        pass

    def update(self):
        player = self.game.player

        # Calculando a distância para ajeitar o alcance:
        distancia = ((self.rect.centerx - player.rect.centerx) **2 + (self.rect.centery - player.rect.centery)**2)**0.5

        # Primeiro vamos verificar se o jogador tá perto o suficiente
        if distancia < 128:  # Chutei um número qualquer para testar
            if self.cooldown_tiro == 0:  # para esperar um pouco antes de atacar
                Poder(self.game, self.rect.centerx, self.rect.centery)
                self.cooldown_tiro = 60  # Botei 1 segundo, mas podemos trocar depois
        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1


class Curupira(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.group = self.game.all_sprites, self.game.enemies

        pygame.sprite.Sprite.__init__(self, self.group)

        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((0, 180, 0))  # quadrado verde
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        self.hitbox = self.rect.copy()

    def take_damage(self, damage):  # Só para não dar erro
        pass

    def update(self):
        # saber se o jogador encostou no curupira
        if self.rect.colliderect(self.game.player.rect):
            # aplica o efeito de atordoamento no jogador
            self.game.player.aplicar_atordoamento()
            self.kill()  # o curupira desaparece apos aplicar o efeito

class Poder_curupira(pygame.sprite.Sprite): #Classe para os projéteis do inimigo final, inspiradas no curupira
    def __init__(self, game, x, y):

        self.game = game

        # Ajeitar a imagem do ataque
        self._layer = PROJ_LAYER
        self.group = self.game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.group)

        self.image = pygame.Surface((16, 16))
        self.image.fill((0, 180, 0))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Ajeitar as distancias para ficar proporcional o quanto anda
        player = self.game.player
        distancia = ((self.rect.centerx - player.rect.centerx) **2 + (self.rect.centery - player.rect.centery)**2)**0.5
        if distancia == 0:
            self.dx = 0
            self.dy = 0
        else:
            self.dx = (player.rect.centerx - self.rect.centerx)/distancia
            self.dy = (player.rect.centery - self.rect.centery)/distancia

        # Uma velocidade qualquer, podemos mudar depois qualquer coisa
        self.speed = 10

    def update(self):
        # Ele anda um pouco dependendo da velocidade
        self.rect.centerx += self.dx * self.speed
        self.rect.centery += self.dy * self.speed

        # Verifica se houve colisão ou com o jogador ou com a parede (para desaparecer)
        if self.rect.colliderect(self.game.player.rect):
            # Aplica o atordoamento do curupira
            self.game.player.aplicar_atordoamento()
            self.kill()

        if pygame.sprite.spritecollide(self, self.game.walls, False):
            self.kill()

class Cacador(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game

        self._layer = PLAYER_LAYER
        self.group = self.game.all_sprites, self.game.enemies

        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = x * TILESIZE  
        self.y = y * TILESIZE 

        #Colocando a aparencia dele como um quadrado vermelho
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        
        self.hitbox = self.rect.copy()
        self.speed = 2
        self.cooldown_tiro = 0

        self.hp = 27 #o caçador tem 15 de vida
        self.invencivel_timer = 0 



    def take_damage(self, damage):
        if self.invencivel_timer == 0:
            self.hp -= damage
            self.invencivel_timer = 15 #fica invencivel por alguns frames

            if self.hp <= 0:
                self.game.playing = False
                self.kill()  #Morre se a vida chegar a zero


    def update(self):
        if self.invencivel_timer > 0: #diminui o timer de invencinilidade se tomou dano há pouco
            self.invencivel_timer -= 1


        player = self.game.player
        if player is None:
            return

        # diferença de posições entre o caçador e o jogador
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        distancia = math.sqrt(dx**2 + dy**2)

        raio_de_visao = 180
        distancia_minima = 45

        x_distancia = 0
        y_distancia = 0


        if distancia <= raio_de_visao:
            if distancia > distancia_minima:
                if self.rect.centerx < player.rect.centerx:
                    x_distancia += self.speed
                elif self.rect.centerx > player.rect.centerx:
                    x_distancia -= self.speed

                if self.rect.centery < player.rect.centery:
                    y_distancia += self.speed
                elif self.rect.centery > player.rect.centery:
                    y_distancia -= self.speed
            else:
                x_distancia = 0
                y_distancia = 0

        self.rect.x += x_distancia
        colidiu_x = self.collide_walls('x', x_distancia)
        self.rect.y += y_distancia
        colidiu_y = self.collide_walls('y', y_distancia)

        if colidiu_x or colidiu_y:
            if colidiu_x and not colidiu_y:
                self.rect.y += self.speed if dy > 0 else -self.speed
                self.collide_walls('y', self.speed if dy > 0 else -self.speed)
            elif colidiu_y and not colidiu_x:
                self.rect.x += self.speed if dx > 0 else -self.speed
                self.collide_walls('x', self.speed if dx > 0 else -self.speed)

        self.hitbox = self.rect.copy()

        # O caçador atira se tiver no alcance dele:
        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1

        if self.cooldown_tiro == 0:
            if distancia < raio_de_visao:
                dx_tiro = player.rect.centerx - self.rect.centerx
                dy_tiro = player.rect.centery - self.rect.centery
                distancia_tiro = (dx_tiro**2 + dy_tiro**2)**0.5

                if distancia_tiro > 0:
                    dx_tiro /= distancia_tiro  # normalização do vetor direção
                    dy_tiro /= distancia_tiro

                    lista_poderes = [BolaDeFogo, Poder_curupira, Poder]
                    sorteado = random.choice(lista_poderes)

                    if sorteado == BolaDeFogo:
                        BolaDeFogo(
                            self.game,
                            self.rect.centerx,
                            self.rect.centery,
                            dx_tiro,
                            dy_tiro
                        )
                    elif sorteado == Poder_curupira:
                        Poder_curupira(self.game, self.rect.centerx, self.rect.centery)
                    else:
                        Poder(self.game, self.rect.centerx, self.rect.centery)

                    self.cooldown_tiro = 60  # espera um tempo de +- 1 segundo

    def collide_walls(self, direcao, distancia):
        bateu_parede = pygame.sprite.spritecollide(self, self.game.walls, False)
        if bateu_parede:
            if direcao == 'x':
                if distancia > 0:  # movendo para a direita
                    self.rect.x = bateu_parede[0].rect.left - self.rect.width
                if distancia < 0:  # movendo para a esquerda
                    self.rect.x = bateu_parede[0].rect.right
            if direcao == 'y':
                if distancia > 0:  # movendo para baixo
                    self.rect.y = bateu_parede[0].rect.top - self.rect.height
                if distancia < 0:  # movendo para cima
                    self.rect.y = bateu_parede[0].rect.bottom

            return True
        return False
