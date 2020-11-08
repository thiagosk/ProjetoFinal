#Importando as bibliotecas
import pygame
import random

pygame.init()

largura = 480
altura = 600
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Space Frogersor')

controle= True

while controle:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  
            controle = False

    janela.fill((255,255,255))
    pygame.display.update()

pygame.quit()