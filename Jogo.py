import pygame

#inicializa o jogo
pygame.init()

#cria o tamanho da tela de display
screen = pygame.display.set_mode((500, 500))

#cria imagens a tamanhos desejaveis
nave_img = pygame.image.load('assets/img/playerShip1_orange.png').convert_alpha()
nave_img = pygame.transform.scale(nave_img, (30, 30))

bala_img = pygame.image.load('assets/img/regularExplosion00.png').convert_alpha()
bala_img = pygame.transform.scale(bala_img, (30, 30))


class Jogador(pygame.sprite.Sprite):
    def __init__(self, img):

        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.angle = 0

    def update(self, img):

        #cria um vetor na nave conforme a imagem da nave e o rotaciona conforme o angulo mexido pelo jogador
        self.direcao_jogador = pygame.Vector2(1,0).rotate(-self.angle)

        #rotaciona a imagem da nave conforme o angulo mexido pelo jogador
        self.image = pygame.transform.rotate(img, self.angle)

        #posicao da nave 
        self.rect = self.image.get_rect()
        self.rect.center = (250,250)

class Balas(pygame.sprite.Sprite):
    def __init__(self, direcao_jogador, img): 

        pygame.sprite.Sprite.__init__(self)

        self.image = img

        #cria um vetor na bala conforme a imagem da nave e o rotaciona conforme o angulo mexido pelo jogador
        self.direcao_bala = direcao_jogador

        #posicao inicial da bala
        self.rect = self.image.get_rect()
        self.rect.center = (250,250)

        #vetor criado na posicao inicial da bala
        self.vetor = pygame.Vector2(self.rect.center)
        
    def update(self, img):
        #vetor da bala seguir com o sentido da nave
        self.vetor += self.direcao_bala

        #atualiza a posicao da bala
        self.rect.center = self.vetor
        
        #apaga a bala se sair da tela
        self.vetor.x = self.vetor[0]
        self.vetor.y = self.vetor[1]
        if self.vetor.x > 500 or self.vetor.x < 0:
            self.kill()
        elif self.vetor.y > 500 or self.vetor.y < 0:
            self.kill()

#cria sprites para facilitar a execucao final
sprites = pygame.sprite.Group()

#adiciona o jogador nas sprites
jogador = Jogador(nave_img)
sprites.add(jogador)

#velocidade do jogo
clock = pygame.time.Clock()
FPS = 30

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
                #adiciona nas sprites as balas
                sprites.add(Balas(jogador.direcao_jogador, bala_img)) 

    #enquanto a tecla estiver apertada o jogador gira
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
        jogador.angle += 10
    if pressed[pygame.K_d]:
        jogador.angle -= 10
           
    #atualiza o jogo
    sprites.update(nave_img)

    #cor de fundo 
    screen.fill((0, 0, 0))

    #mostra as imagens na tela
    sprites.draw(screen)

    #mostra o proximo frame
    pygame.display.update()

#finaliza o jogo
pygame.quit()