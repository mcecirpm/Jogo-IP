import pygame
import os

from classes.config import *


class Player(pygame.sprite.Sprite):
    _imagem = None
    def __init__(self, game, x, y, status, homming):

        self.game = game
        self._layer = PLAYER_LAYER
        self.group = self.game.all_sprites

        # Objeto pai
        pygame.sprite.Sprite.__init__(self, self.group)

        self.x = TILESIZE * x
        self.y = TILESIZE * y

        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        if Player._imagem is None: 
            diretorio_atual = os.path.dirname(__file__) 
            caminho = os.path.join(diretorio_atual, '..', 'assetes', 'sprites', 'jogador_alternativo_sem_fundo.png') 
            Player._imagem = pygame.image.load(caminho).convert_alpha()
            
        self.image = pygame.transform.scale(Player._imagem, (TILESIZE, TILESIZE))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.inventario = Inventario(self)

        self.shoot_cooldown = 0

        # Dicionário com as estatísticas do personagem
        self.status = status

        self.has_homing = homming

        # Exemplo de quantidade máxima de vidas e de tempo de duração da "partida", pode ser modificado se decidirmos algo novo
        self.hp_max = self.status["hp_max"]
        self.hp = self.hp_max
        self.vida_extra = self.status['vida_extra']

        self.tempo = 180  # 5 minutos em segundos

        # Efeito do Curupira
        self.velocidade_multiplicador = 1
        self.atordoado = False
        self.tempo_atordoado = 0

    def moviment(self):
        # a velocidade do jogador é multiplicada pelo efeito do Curupira, que deixa o jogador mais lento
        speed = self.status['speed'] * 4 * self.velocidade_multiplicador

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change -= speed
        if keys[pygame.K_d]:
            self.x_change += speed
        if keys[pygame.K_w]:
            self.y_change -= speed
        if keys[pygame.K_s]:
            self.y_change += speed

    def attack(self):
        keys = pygame.key.get_pressed()

        if self.shoot_cooldown == 0:
            hx = self.rect.centerx
            hy = self.rect.centery
            shoot = False

            damage = self.status['dano'] * self.status['multi_atq']
            speed_proj = self.status['atq_speed'] * 4
            alcance = self.status['alcance']

            if keys[pygame.K_UP]:
                Projectile(self.game, hx, hy, 'face_up',
                           damage, speed_proj, alcance)
                shoot = True
            elif keys[pygame.K_DOWN]:
                Projectile(self.game, hx, hy, 'face_down',
                           damage, speed_proj, alcance)
                shoot = True
            elif keys[pygame.K_LEFT]:
                Projectile(self.game, hx, hy, 'face_left',
                           damage, speed_proj, alcance)
                shoot = True
            elif keys[pygame.K_RIGHT]:
                Projectile(self.game, hx, hy, 'face_right',
                           damage, speed_proj, alcance)
                shoot = True

            if shoot:
                self.shoot_cooldown = round(self.shoot_cooldown_cal(), 1) + 1

    def shoot_cooldown_cal(self):
        self.teto_freq = 2.307
        frequencia = self.status['frequencia']

        if frequencia > self.teto_freq:
            return 7
        elif frequencia <= self.teto_freq and frequencia >= 0:
            return 21 - 7 * (1.31 * frequencia) ** (1/2)
        elif frequencia < 0 and frequencia < -0.467:
            return 21 - 7 * (1.31 * frequencia) ** (1/2) - 7 * (frequencia)
        else:
            return 21 - 7 * (frequencia)

    def update(self):
        if self.atordoado:
            self.tempo_atordoado -= 1
            if self.tempo_atordoado <= 0:
                self.atordoado = False
                self.velocidade_multiplicador = 1

        self.moviment()
        self.attack()
        self.coletar_itens()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        self.rect.x += self.x_change
        self.collide_walls('x')
        self.collide_porta_bloqueada('x')

        self.rect.y += self.y_change
        self.collide_walls('y')
        self.collide_porta_bloqueada('y')

        self.x_change = 0
        self.y_change = 0

    def aplicar_atordoamento(self):
        if self.atordoado:  # se o jogador já estiver atordoado, não aplica o efeito novamente
            return
        self.atordoado = True  # jogador atordoado
        self.velocidade_multiplicador = 0.5  # deixa a velocidade do jogador pela metade
        # o jogador fica atordoado por 5 segundos, depois volta a velocidade normal
        self.tempo_atordoado = FPS * 5

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

    def coletar_itens(self):
        hits = pygame.sprite.spritecollide(self, self.game.pickup, True)

        for hit in hits:
            if hit.tipo == 'vida':
                self.hp = min(self.status['hp_max'], self.hp + 10)
                self.inventario.registrar_vida()
            elif hit.tipo == 'tempo':
                self.tempo += 15
                self.inventario.registrar_tempo()
            elif hit.tipo == 'chave':
                self.inventario.contagem_chave += 1
                pos_chave = (self.game.sala_atual.x,
                             self.game.sala_atual.y, hit.grid_x, hit.grid_y)
                self.game.chaves_coletadas.add(pos_chave)

    def collide_porta_bloqueada(self, direction):
        from classes.labirinto import salas

        sala_atual = self.game.sala_atual
        proxima_sala_final = salas[(2, -2)]

        hits_porta = pygame.sprite.spritecollide(self, self.game.doors, False)

        for porta in hits_porta:
            vizinho = sala_atual.vizinho[porta.direcao]

            if vizinho == proxima_sala_final and self.inventario.contagem_chave < 3:
                if direction == "x":
                    if self.x_change > 0:
                        self.rect.x = porta.rect.left - self.rect.width
                    elif self.x_change < 0:
                        self.rect.x = porta.rect.right
                elif direction == "y":
                    if self.y_change > 0:
                        self.rect.y = porta.rect.top - self.rect.height
                    elif self.y_change < 0:
                        self.rect.y = porta.rect.bottom


class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, facing, damage, speed_proj, alcance):
        self.game = game
        self._layer = PROJ_LAYER
        self.group = self.game.all_sprites, self.game.projectiles

        # Objeto neto
        pygame.sprite.Sprite.__init__(self, self.group)

        self.width = 25
        self.heigth = 25

        self.image = pygame.Surface([self.width, self.heigth])
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.facing = facing
        self.damage = damage
        self.speed_proj = speed_proj

        self.distance_traveled = 0
        self.max_distance = TILESIZE * alcance

    def update(self):
        if self.facing == "face_up":
            self.rect.y -= self.speed_proj
            self.distance_traveled += self.speed_proj
        elif self.facing == "face_down":
            self.rect.y += self.speed_proj
            self.distance_traveled += self.speed_proj
        elif self.facing == "face_left":
            self.rect.x -= self.speed_proj
            self.distance_traveled += self.speed_proj
        elif self.facing == "face_right":
            self.rect.x += self.speed_proj
            self.distance_traveled += self.speed_proj

        if self.distance_traveled >= self.max_distance:
            self.kill()

        if pygame.sprite.spritecollide(self, self.game.walls, False):
            self.kill()

        if pygame.sprite.spritecollide(self, self.game.doors, False):
            self.kill()

        hits_enemy = pygame.sprite.spritecollide(
            self, self.game.guardioes, False)

        for hit in hits_enemy:
            if self.rect.colliderect(hit.hitbox):
                hit.take_damage(self.damage)
                self.kill()
                break


class Inventario:
    def __init__(self, player):
        self.player = player
        self.coisas = []  # Armazena os dicionários dos itens coletados
        self.contagem_vida = 0
        self.contagem_tempo = 0
        self.contagem_chave = 0

    def adicionar_chave(self, tipo_chave):
        self.coisas.append({
            "nome": f"Chave ({tipo_chave})",
            "tipo": "chave",
            "subtipo": tipo_chave
        })

    def registrar_vida(self):
        self.contagem_vida += 1

    def registrar_tempo(self):
        self.contagem_tempo += 1
