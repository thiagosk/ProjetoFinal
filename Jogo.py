import pygame
import random

#inicializa o jogo
pygame.init()

#cria o tamanho da tela de display
largura = 1200
altura = 800
screen = pygame.display.set_mode((largura, altura))

#cria imagens a tamanhos desejaveis
nave_img = pygame.image.load('assets/img/playerShip1_orange.png').convert_alpha()
nave_img = pygame.transform.scale(nave_img, (30, 30))

bala_img = pygame.image.load('assets/img/regularExplosion00.png').convert_alpha()
bala_img = pygame.transform.scale(bala_img, (30, 30))

l_meteoro = 50
a_meteoro = 50
meteoro_img = pygame.image.load('assets/img/meteorBrown_med1.png').convert_alpha()
meteoro_img = pygame.transform.scale(meteoro_img, (l_meteoro, a_meteoro))


class Jogador(pygame.sprite.Sprite):
    def __init__(self, img):

        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.angle = 0

    def update(self, img):

        # Cria um vetor na nave conforme a imagem da nave e o rotaciona conforme o angulo mexido pelo jogador
        self.direcao_jogador = pygame.Vector2(1,0).rotate(-self.angle)

        # Rotaciona a imagem da nave conforme o angulo mexido pelo jogador
        self.image = pygame.transform.rotate(img, self.angle)

        # Posição da nave 
        self.rect = self.image.get_rect()
        self.rect.center = (largura/2, altura/2)


class Balas(pygame.sprite.Sprite):
    def __init__(self, direcao_jogador, img): 

        pygame.sprite.Sprite.__init__(self)

        self.image = img

        # Cria um vetor na bala conforme a imagem da nave e o rotaciona conforme o angulo mexido pelo jogador
        self.direcao_bala = direcao_jogador

        # Posição inicial da bala
        self.rect = self.image.get_rect()
        self.rect.center = (largura/2, altura/2)

        # Vetor criado na posicao inicial da bala
        self.vetor = pygame.Vector2(self.rect.center)
        
    def update(self):
        # Vetor da bala seguir com o sentido da nave
        self.vetor += self.direcao_bala

        # Atualiza a posicao da bala
        self.rect.center = self.vetor
        
        # Apaga a bala se sair da tela
        self.vetor.x = self.vetor[0]
        self.vetor.y = self.vetor[1]
        if self.vetor.x > largura or self.vetor.x < 0:
            self.kill()
        elif self.vetor.y > altura or self.vetor.y < 0:
            self.kill()


class Meteoros(pygame.sprite.Sprite):
    def __init__(self, img):

        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()

        #posicao inicial do meteoro
        #sorteio de um numero para ver qual lado o meteoro ira surgir
        self.numero = random.randint(1,4)
        if self.numero == 1:
            self.rect.x = random.randint(0, largura - l_meteoro)
            self.rect.y = random.randint(altura, altura + a_meteoro)
        elif self.numero == 2:
            self.rect.x = random.randint(0, largura - l_meteoro)
            self.rect.y = random.randint(-51, - a_meteoro)
        elif self.numero == 3:
            self.rect.x = random.randint(-l_meteoro,0)
            self.rect.y = random.randint(0, altura)
        elif self.numero == 4:
            self.rect.x = random.randint(largura,largura+l_meteoro)
            self.rect.y = random.randint(0,altura)

        #velocidade do meteoro
        if self.numero == 1 or self.numero == 2:
            self.speedx = random.randint(-1, 1)
            self.speedy = random.randint(-1, 1)
        elif self.numero == 3:
            self.speedx = random.randint(0, 2)
            self.speedy = random.randint(-1, +1)
        elif self.numero == 4:
            self.speedx = random.randint(-2, 0)
            self.speedy = random.randint(-1, +1)

    def update(self):
        #atualiza a posicao do meteoro
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        #se o meteoro sair da tela um novo meteoro aparece
        if self.rect.y > altura or self.rect.x < 0 or self.rect.x > largura or self.rect.y < -52:
            if self.numero == 1:
                self.rect.x = random.randint(0, largura - l_meteoro)
                self.rect.y = random.randint(altura, altura + a_meteoro)
                self.speedx = random.randint(-1, 1)
                self.speedy = random.randint(-1, 1)
            elif self.numero == 2:
                self.rect.x = random.randint(0, largura - l_meteoro)
                self.rect.y = random.randint(-51, - a_meteoro)
                self.speedx = random.randint(-1, 1)
                self.speedy = random.randint(-1, 1)
            elif self.numero == 3:
                self.rect.x = random.randint(-l_meteoro,0)
                self.rect.y = random.randint(0, altura )
                self.speedx = random.randint(0, 2)
                self.speedy = random.randint(-1, +1)
            elif self.numero == 4:
                self.rect.x = random.randint(largura,largura+l_meteoro)
                self.rect.y = random.randint(0,altura)
                self.speedx = random.randint(-2, 0)
                self.speedy = random.randint(-1, +1)


#cria sprites para facilitar a execucao final
sprites = pygame.sprite.Group()
todos_meteoros = pygame.sprite.Group()
todas_balas = pygame.sprite.Group()

#adiciona o jogador nas sprites
jogador = Jogador(nave_img)
sprites.add(jogador) 

#criando os meteoros e os adicionando no seu grupo
for i in range(20):
    todos_meteoros.add(Meteoros(meteoro_img))

#velocidade do jogo
clock = pygame.time.Clock()
FPS = 50

#loop do jogo
controle = True
while controle:
    clock.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            controle = False
        if evento.type == pygame.KEYDOWN:
            #cria bala
            if evento.key == pygame.K_SPACE: 
                #adiciona no seu grupo as balas
                todas_balas.add(Balas(jogador.direcao_jogador, bala_img)) 

    #enquanto a tecla estiver apertada o jogador gira
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
        jogador.angle += 4
    if pressed[pygame.K_d]:
        jogador.angle -= 4
           
    #atualiza o jogo
    sprites.update(nave_img)
    todas_balas.update()
    todos_meteoros.update()

    #se a bala colidir com o meteoro, ambos desaparecem
    hits = pygame.sprite.groupcollide(todos_meteoros, todas_balas, True, True)

    #quando um meteoro desaparece, um outro surge
    for i in hits: 
        todos_meteoros.add(Meteoros(meteoro_img))

    #cor de fundo 
    screen.fill((0, 0, 0))

    #mostra as imagens na tela
    sprites.draw(screen)
    todas_balas.draw(screen)
    todos_meteoros.draw(screen)

    #mostra o proximo frame
    pygame.display.update()

# Finaliza o jogo
pygame.quit()