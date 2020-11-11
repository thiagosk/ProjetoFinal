# importa bibliotecas
import pygame
import random
import math

# inicializa o jogo
pygame.init()

# variaveis de cor
branco = (255,255,255)
preto = (0,0,0)

# variaveis de dimensoes
largura = 800
altura = 650
nave_largura = 50
nave_altura = 38

# variaveis gerais
g = 2
v = 25
chao_altura = altura - 50
# Cria janela, nome e icone
janela = pygame.display.set_mode((largura, altura))

pygame.display.set_caption('Space Frogerson')

icone = pygame.image.load("assets/img/playerShip1_orange.png")
pygame.display.set_icon(icone)

# Cria imagem a dimensoes desejaveis
nave_img = pygame.image.load('assets/img/playerShip1_orange.png').convert_alpha()
nave_img = pygame.transform.scale(nave_img, (nave_largura, nave_altura))

bala_img = pygame.image.load('assets/img/laserRed16.png').convert_alpha()

# Estados do jogador
parado = 0
pulando = 1
caindo = 2

class nave(pygame.sprite.Sprite):
    def __init__(self, img, todas_sprites, todas_balas, bala_img):
        pygame.sprite.Sprite.__init__(self)

        self.state = parado

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = chao_altura - nave_altura
        self.rect.top = 0
        self.vx = 0
        self.vy = 0
        self.todas_sprites = todas_sprites
        self.todas_balas = todas_balas
        self.bala_img = bala_img

    def update(self):
        self.vy += g
        if self.vy > 0:
            self.state = caindo
        self.rect.y += self.vy
        if self.rect.bottom > chao_altura:
            self.rect.bottom = chao_altura
            self.vy = 0
            self.state = parado

        self.rect.x += self.vx

        # Mantém o jogador na tela
        if self.rect.right > largura:
            self.rect.right = largura
        elif self.rect.left < 0:
            self.rect.left = 0
       
    def pula(self):
        if self.state == parado:
            self.vy -= v
            self.state = pulando
        
    def atira(self):
        nova_bala = bala(self.bala_img, self.rect.top, self.rect.x)
        self.todas_sprites.add(nova_bala)
        self.todas_balas.add(nova_bala)

class bala(pygame.sprite.Sprite):
    def __init__(self, img, bottom, centerx):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.vy = -10

    def update(self):
        self.rect.y += self.vy

        if self.rect.bottom < 0:
            self.kill()


todas_sprites = pygame.sprite.Group()
todas_balas = pygame.sprite.Group()

jogador = nave(nave_img, todas_sprites, todas_balas, bala_img)
todas_sprites.add(jogador)

# ajustar velocidade
clock = pygame.time.Clock()
FPS = 60

# Looping do jogo
controle= 0
while controle == 0:
    clock.tick(FPS)
 
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  
            controle = 1
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                jogador.vx -= 10
            elif evento.key == pygame.K_d:
                jogador.vx += 10
            elif evento.key == pygame.K_SPACE:
                jogador.pula()
            elif evento.key == pygame.K_p:
                jogador.atira()
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_a:
                jogador.vx += 10
            elif evento.key == pygame.K_d:
                jogador.vx -= 10

    todas_sprites.update()
    janela.fill(preto)
    todas_sprites.draw(janela)

    pygame.display.update()

# Finalizando o jogo
pygame.quit()