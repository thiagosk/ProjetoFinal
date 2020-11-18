import pygame
import random

#inicializa o jogo
pygame.init()

#cria o tamanho da tela de display
largura = 1500
altura = 750
screen = pygame.display.set_mode((largura, altura))

#cria imagens a tamanhos desejaveis
nave_img = pygame.image.load('assets/img/playerShip1_orange.png').convert_alpha()
nave_img = pygame.transform.scale(nave_img, (30, 30))

bala_img = pygame.image.load('assets/img/regularExplosion00.png').convert_alpha()
bala_img = pygame.transform.scale(bala_img, (20, 20))

l_meteoro = 30
a_meteoro = 30
meteoro_img = pygame.image.load('assets/img/meteorBrown_med1.png').convert_alpha()
meteoro_img = pygame.transform.scale(meteoro_img, (l_meteoro, a_meteoro))

score_font = pygame.font.Font('assets/font/PressStart2P.ttf', 30)

background = pygame.image.load('assets/img/starfield.png').convert()
background = pygame.transform.scale(background, (largura, altura))

explosion_anim = []
for i in range(9):
    # Os arquivos de animação são numerados de 00 a 08
    filename = 'assets/img/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img = pygame.transform.scale(img, (32, 32))
    explosion_anim.append(img)


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

        self.rect.center = (self.rect.x,self.rect.y)

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
        if self.speedx == 0:
            self.speedx = 1
        if self.speedy == 0:
            self.speedy = 1

    def update(self):
        #atualiza a posicao do meteoro
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        #se o meteoro sair da tela um novo meteoro aparece
        if self.rect.y > altura or self.rect.x < -l_meteoro or self.rect.x > largura or self.rect.y < -52:
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
                self.rect.y = random.randint(0, altura)
                self.speedx = random.randint(0, 2)
                self.speedy = random.randint(-1, +1)
            elif self.numero == 4:
                self.rect.x = random.randint(largura,largura+l_meteoro)
                self.rect.y = random.randint(0,altura)
                self.speedx = random.randint(-2, 0)
                self.speedy = random.randint(-1, +1)

            self.rect.center = (self.rect.x,self.rect.y)

        if self.speedx == 0:
            self.speedx = 1
        if self.speedy == 0:
            self.speedy = 1


class Explosion(pygame.sprite.Sprite):

    def __init__(self, center, img):

        pygame.sprite.Sprite.__init__(self)

        self.explosion_anim = img

        self.frame = 0  
        self.image = self.explosion_anim[self.frame]  
        self.rect = self.image.get_rect()
        self.rect.center = center  

        self.last_update = pygame.time.get_ticks()

        self.frame_ticks = 50

    def update(self,img):
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update

        if elapsed_ticks > self.frame_ticks:
            self.last_update = now

            self.frame += 1

            if self.frame == len(self.explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


#cria sprites para facilitar a execucao final
sprites = pygame.sprite.Group()
todos_meteoros = pygame.sprite.Group()
todas_balas = pygame.sprite.Group()

#adiciona o jogador nas sprites
jogador = Jogador(nave_img)
sprites.add(jogador) 

#criando os meteoros e os adicionando no seu grupo
for i in range(10):
    todos_meteoros.add(Meteoros(meteoro_img))

#velocidade do jogo
clock = pygame.time.Clock()
FPS = 30

#valor inicial do score
score = 0

#numero de balas totais
balass = 10

#contagem do tempo
t_max = 30
start_ticks=pygame.time.get_ticks()

#loop do jogo
controle = True
while controle:
    clock.tick(FPS)

    #contagem do tempo
    seconds=int((pygame.time.get_ticks()-start_ticks)/1000)
    if seconds>=t_max: 
        controle = False

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            controle = False
        if evento.type == pygame.KEYDOWN:
            #cria bala e limita a quantidade de tiros
            if evento.key == pygame.K_SPACE and balass != 0 :
                balas = Balas(jogador.direcao_jogador, bala_img)
                todas_balas.add(balas)
                balass -= 1

    #Game over se as balas acabarem e nao estiverem mais na tela
    if balass == 0:
        if len(todas_balas) == 0:
            controle = False

    #enquanto a tecla estiver apertada o jogador gira
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
        jogador.angle += 4
    if pressed[pygame.K_d]:
        jogador.angle -= 4
           

    #se a bala colidir com o meteoro, ambos desaparecem
    hits = pygame.sprite.groupcollide(todos_meteoros, todas_balas, True, True)

    #quando um meteoro desaparece, um outro surge
    for i in hits: 
        meteoros = Meteoros(meteoro_img)
        todos_meteoros.add(meteoros)

        #atualiza o score
        score+=100

        #chama a animaçao de colisao
        explosao = Explosion(i.rect.center, explosion_anim)
        sprites.add(explosao)

    #atualiza o jogo
    sprites.update(nave_img)
    todas_balas.update()
    todos_meteoros.update()

    #cor de fundo 
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    #mostra as imagens na tela
    sprites.draw(screen)
    todas_balas.draw(screen)
    todos_meteoros.draw(screen)

    #mostra o score
    texto = score_font.render("{:04d}".format(score), True, (255, 255, 0))
    text_rect = texto.get_rect()
    text_rect.midtop = (largura / 2,  10)
    screen.blit(texto, text_rect)

    #mostra quantidade de balas
    texto = score_font.render("Balas: {:02d}".format(balass), True, (0, 255, 255))
    text_rect = texto.get_rect() 
    text_rect.midtop = (largura - 200, altura-100)
    screen.blit(texto, text_rect)

    #mostra o tempo
    texto = score_font.render("Tempo:{0:02d}/{1}".format(seconds,t_max), True, (100, 255, 100))
    text_rect = texto.get_rect()
    text_rect.midtop = (200,  100)
    screen.blit(texto, text_rect)

    #mostra o proximo frame
    pygame.display.update()

# Finaliza o jogo
pygame.quit()