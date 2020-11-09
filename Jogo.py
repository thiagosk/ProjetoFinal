#Importando as bibliotecas
import pygame
import random
import math

pygame.init()

branco = (255,255,255)
preto = (0,0,0)
largura = 800
altura = 650

janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Space Frogerson')

nave_largura = 50
nave_altura = 38
nave_img = pygame.image.load('assets/img/playerShip1_orange.png').convert_alpha()
nave_img = pygame.transform.scale(nave_img, (nave_largura, nave_altura))

class nave(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 325
        self.vx = 0

    def update(self):
        self.rect.x += self.vx


todas_sprites = pygame.sprite.Group()
jogador = nave(nave_img)
todas_sprites.add(jogador)

controle= 0
while controle != 1:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  
            controle = 1
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                jogador.vx -= 8
            elif evento.key == pygame.K_d:
                jogador.vx += 8

    todas_sprites.update()
    janela.fill(preto)
    todas_sprites.draw(janela)

    pygame.display.update()

pygame.quit()