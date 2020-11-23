import pygame
import random
import time

#inicializa o jogo e o som
pygame.init()
pygame.mixer.init()

#cria o tamanho da tela de display
largura = 750
altura = 750
screen = pygame.display.set_mode((largura, altura))

#nome da tela
pygame.display.set_caption('navinhaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

#icone da tela
nave_img = pygame.image.load('assets/img/ufo.png').convert_alpha()
nave_img = pygame.transform.scale(nave_img, (30, 30))
pygame.display.set_icon(nave_img)

#cria imagens a tamanhos desejaveis
nave_img = pygame.image.load('assets/img/ufo.png').convert_alpha()
nave_img = pygame.transform.scale(nave_img, (30, 30))
nave_img2 = pygame.transform.scale(nave_img, (120, 120))

bala_img = pygame.image.load('assets/img/rec.png').convert_alpha()
bala_img = pygame.transform.scale(bala_img, (20, 20))

l_meteoro = 30
a_meteoro = 30
meteoro_img = pygame.image.load('assets/img/asteroid.png').convert_alpha()
meteoro_img = pygame.transform.scale(meteoro_img, (l_meteoro, a_meteoro))

thiagao_img = pygame.image.load('assets/img/thiagao.png').convert_alpha()
thiagao_img = pygame.transform.scale(thiagao_img, (200,300))

luisao_img = pygame.image.load('assets/img/luisao.png').convert_alpha()
luisao_img = pygame.transform.scale(luisao_img, (200, 300))

pedrao_img = pygame.image.load('assets/img/pedro.png').convert_alpha()
pedrao_img = pygame.transform.scale(pedrao_img, (200, 300))

score_font = pygame.font.Font('assets/font/kindergarten.ttf', 30)
score_font2 = pygame.font.Font('assets/font/kindergarten.ttf', 50)
score_font3 = pygame.font.Font('assets/font/kindergarten.ttf', 80)
score_font4 = pygame.font.Font('assets/font/kindergarten.ttf', 60)
score_font6 = pygame.font.Font('assets/font/kindergarten.ttf', 100)
score_font7 = pygame.font.Font('assets/font/kindergarten.ttf', 21)
score_font8 = pygame.font.Font('assets/font/kindergarten.ttf', 25)

fundo = pygame.image.load('assets/img/starfield.png').convert()
fundo = pygame.transform.scale(fundo, (largura, altura))

fundo2 = pygame.image.load('assets/img/starfield.png').convert()
fundo2 = pygame.transform.scale(fundo2, (largura, altura))

fundo4 = pygame.image.load('assets/img/starfield.png').convert()
fundo4 = pygame.transform.scale(fundo4, (largura, altura))

#cria animacoes
explosion_anim = []
for i in range(5):
    filename = 'assets/img/explosion{}.png'.format(i)
    img = pygame.image.load(filename).convert_alpha()
    img = pygame.transform.scale(img, (32, 32))
    explosion_anim.append(img)

#cria sons
pygame.mixer.music.load('assets/snd/som4.flac')
botao_sound = pygame.mixer.Sound('assets/snd/som1.wav')
destroy_sound = pygame.mixer.Sound('assets/snd/som3.wav')
pew_sound = pygame.mixer.Sound('assets/snd/som2.wav')
pygame.mixer.music.set_volume(0.05)
botao_sound.set_volume(0.1)
destroy_sound.set_volume(0.1)
pew_sound.set_volume(0.1)


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

        #se o meteoro sair da tela, um novo meteoro aparece
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

        #para o meteoro nunca ficar parado
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
for i in range(5):
    todos_meteoros.add(Meteoros(meteoro_img))

#velocidade do jogo
clock = pygame.time.Clock()

#condicao para entrar na tela inicial
estado = "inicio"

#guarda score max
max_p = 0

pygame.mixer.music.play(loops=-1)

#tela inicial
while estado == "inicio":
    FPS = 30

    #cria botao
    button1 = pygame.Rect(320, 300, 120, 60)
    button2 = pygame.Rect(277, 430, 210, 50)
    button4 = pygame.Rect(280, 580, 220, 50)

    #tempo inicial
    tempo = 0  # Tempo desde o começo do jogo

    #balas iniciais
    balass = 10

    clock.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
        if evento.type == pygame.MOUSEBUTTONDOWN:
                #posicao do mouse
                mouse_posicao = evento.pos

                #se o mouse clicar no botao
                if button1.collidepoint(mouse_posicao):
                    botao_sound.play()



                    #score inicial
                    score = 0

                    estado = "jogando"

                    gameover = 0

                    m = 1
                    #contagem do tempo
                    start_ticks = pygame.time.get_ticks()  # Ticks desde o último frame

                    #loop principal
                    while estado == "jogando" and gameover != 2:
                        clock.tick(FPS)
                        #contagem do tempo
                        tempo += (pygame.time.get_ticks() - start_ticks) * m
                        seconds = 35 - int(tempo / (1000))
                        start_ticks=pygame.time.get_ticks()

                        #se o tempo acaba, Game Over
                        if seconds <= 0:

                            # condicao para nao ter dois gameovers
                            gameover = 1

                            tempo = 0
                            seconds = 3

                            #tela de game over por 3-4 segundos dps volta para a tela inicial (loop final)
                            while seconds >= 0 and gameover == 1:
                                #contagem do tempo
                                tempo += pygame.time.get_ticks() - start_ticks
                                seconds = 3 - int(tempo / (1000))
                                start_ticks=pygame.time.get_ticks()

                                #cor da tela
                                screen.fill((0, 0, 0))
                                screen.blit(fundo2, (0, 0))

                                #escreve GameOver
                                texto = score_font6.render("Game over", True, (100, 255, 100))
                                text_rect = texto.get_rect()
                                text_rect = (160,  100)
                                screen.blit(texto, text_rect)

                                #escreve a pontuacao
                                texto = score_font2.render("Pontuacao:", True, (200, 255, 100))
                                text_rect = texto.get_rect()
                                text_rect = (270,  300)
                                screen.blit(texto, text_rect)

                                texto = score_font2.render("{0}".format(score), True, (200, 255, 100))
                                text_rect = texto.get_rect()
                                text_rect = (350,  365)
                                screen.blit(texto, text_rect)

                                #substitui o score max
                                if score > max_p:
                                    max_p = score

                                for evento in pygame.event.get():
                                    if evento.type == pygame.QUIT:
                                        pygame.quit()

                                pygame.display.update()

                            #reset nos meteoros
                            todos_meteoros.empty()
                            for i in range(5):
                                todos_meteoros.add(Meteoros(meteoro_img))

                            #reset nas balas
                            todas_balas.empty()

                            #volta para a tela inicial
                            estado = "inicio"

                        for evento in pygame.event.get():
                            if evento.type == pygame.QUIT:
                                pygame.quit()
                            if evento.type == pygame.KEYDOWN:
                                #cria bala e limita a quantidade de tiros
                                if evento.key == pygame.K_SPACE and balass != 0:
                                    pew_sound.play()
                                    balas = Balas(jogador.direcao_jogador, bala_img)
                                    todas_balas.add(balas)
                                    balass -= 1

                                #se as balas tiverem acabado, mas o jogo nao, o jogador pode alterar a velocidade do jogo para acabar mais rapido
                                if evento.key == pygame.K_r and balass == 0:
                                    FPS = 60
                                    m = 2


                        #Game over se as balas acabarem e nao estiverem mais na tela
                        if balass == 0 and gameover != 1:
                            if len(todas_balas) == 0:

                                #tela de game over por 2-3 segundos dps volta para a tela inicial
                                start_ticks = pygame.time.get_ticks()
                                seconds = tempo

                                #condicao para nao ter dois gameovers
                                gameover = 2
                                tempo = 0
                                seconds = 3

                                #loop final
                                while seconds >= 0 and gameover == 2:
                                    #contagem do tempo
                                    tempo += pygame.time.get_ticks() - start_ticks
                                    seconds = 3 - int(tempo / (1000))
                                    start_ticks=pygame.time.get_ticks()

                                    #cor da tela
                                    screen.fill((0, 0, 0))
                                    screen.blit(fundo2, (0, 0))

                                    #escreve GameOver
                                    texto = score_font6.render("Game over", True, (100, 255, 100))
                                    text_rect = texto.get_rect()
                                    text_rect = (160,  100)
                                    screen.blit(texto, text_rect)

                                    #escreve a pontuacao
                                    texto = score_font2.render("Pontuacao:", True, (200, 255, 100))
                                    text_rect = texto.get_rect()
                                    text_rect = (270,  300)
                                    screen.blit(texto, text_rect)

                                    texto = score_font2.render("{0}".format(score), True, (200, 255, 100))
                                    text_rect = texto.get_rect()
                                    text_rect = (350,  365)
                                    screen.blit(texto, text_rect)

                                    #substitui o score maximo
                                    if score > max_p:
                                        max_p = score

                                    for evento in pygame.event.get():
                                        if evento.type == pygame.QUIT:
                                            pygame.quit()

                                    pygame.display.update()

                                #reset nos meteoros
                                todos_meteoros.empty()
                                for i in range(5):
                                    todos_meteoros.add(Meteoros(meteoro_img))

                                #reset nas balas
                                todas_balas.empty()

                                #volta para a tela inicial
                                estado = "inicio"

                        #enquanto a tecla estiver apertada o jogador gira
                        pressed = pygame.key.get_pressed()
                        if pressed[pygame.K_a]:
                            jogador.angle += 8
                        if pressed[pygame.K_d]:
                            jogador.angle -= 8

                        #se a bala colidir com o meteoro, ambos desaparecem
                        hits = pygame.sprite.groupcollide(todos_meteoros, todas_balas, True, True)

                        #quando um meteoro desaparece, um outro surge
                        for i in hits:
                            meteoros = Meteoros(meteoro_img)
                            todos_meteoros.add(meteoros)

                            #atualiza o score
                            score+=100

                            destroy_sound.play()

                            #chama a animaçao de colisao
                            explosao = Explosion(i.rect.center, explosion_anim)
                            sprites.add(explosao)


                        #atualiza o jogo
                        sprites.update(nave_img)
                        todas_balas.update()
                        todos_meteoros.update()

                        #cor de fundo
                        screen.fill((0, 0, 0))
                        screen.blit(fundo, (0, 0))

                        #mostra as imagens na tela
                        sprites.draw(screen)
                        todas_balas.draw(screen)
                        todos_meteoros.draw(screen)

                        #mostra o score
                        texto = score_font2.render("{:04d}".format(score), True, (255, 255, 0))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (largura / 2,  50)
                        screen.blit(texto, text_rect)

                        #mostra quantidade de balas
                        texto = score_font.render("Balas:{:02d}".format(balass), True, (0, 255, 255))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (largura - 100, altura-50)
                        screen.blit(texto, text_rect)

                        #mostra o tempo
                        texto = score_font.render("Tempo:{0:02d}".format(seconds), True, (100, 255, 100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (100, 100)
                        screen.blit(texto, text_rect)

                        #mostra o proximo frame
                        pygame.display.update()

                #se clicar no botao de tutorial
                elif button2.collidepoint(mouse_posicao):
                    botao_sound.play()

                    estado = "tutorial"

                    while estado == "tutorial":

                        #imagem de fundo
                        screen.fill((0, 0, 0))
                        screen.blit(fundo2, (0, 0))

                        #escreve tutorial
                        texto = score_font3.render("Tutorial", True, (100, 255, 100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (400, 70)
                        screen.blit(texto, text_rect)

                        #escreve girar para a direita
                        texto = score_font.render("girar para a direita", True,  (255,100,100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (480, 300)
                        screen.blit(texto, text_rect)

                        #escreve girar para a esquerda
                        texto = score_font.render("girar para a esquerda", True, (255,100,100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (500, 400)
                        screen.blit(texto, text_rect)

                        #escreve atirar
                        texto = score_font.render("atirar", True,  (255,100,100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (390, 500)
                        screen.blit(texto, text_rect)

                        #escreve velocidade 2x
                        texto = score_font.render("velocidade 2x ", True,  (255,100,100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (450,600)
                        screen.blit(texto, text_rect)

                        #escreve (somente possivel quando voce estiver sem
                        texto = score_font7.render("(somente possivel quando estiver sem", True,(255,100,100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (530, 640)
                        screen.blit(texto, text_rect)

                        #escreve balas)
                        texto = score_font7.render("balas)", True, (255,100,100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (720, 660)
                        screen.blit(texto, text_rect)

                        #escreve A
                        texto = score_font3.render("A", True, (255,100,255))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (200, 380)
                        screen.blit(texto, text_rect)

                        #escreve D
                        texto = score_font3.render("D", True, (255,100,255))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (200, 280)
                        screen.blit(texto, text_rect)

                        #escreve SPACE
                        texto = score_font3.render("SPACE", True, (255,100,255))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (200, 480)
                        screen.blit(texto, text_rect)

                        #escreve R
                        texto = score_font3.render("R", True,(255,100,255))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (200,580)
                        screen.blit(texto, text_rect)

                        #escreve (somente possivel quando voce estiver sem balas)
                        texto = score_font7.render("Acerte o maximo de meteoros que conseguir em 35 segundos e com {0} balas!".format(balass), True, (255,50,100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (375, 200)
                        screen.blit(texto, text_rect)

                        #imagem do botao de volta
                        button3 = pygame.Rect(35, 50, 90,27)
                        pygame.draw.rect(screen, [40,100,10], button3)

                        #escreve voltar
                        texto = score_font.render("Voltar", True, (0, 255, 255))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (80, 50)
                        screen.blit(texto, text_rect)

                        pygame.display.update()

                        for evento in pygame.event.get():
                            if evento.type == pygame.QUIT:
                                pygame.quit()
                            if evento.type == pygame.MOUSEBUTTONDOWN:
                                    #posicao do mouse
                                    mouse_posicao = evento.pos

                                    if button3.collidepoint(mouse_posicao):
                                        botao_sound.play()

                                        #volta para a tela de inicio
                                        estado = "inicio"

                #se clicar no botao de tutorial
                elif button4.collidepoint(mouse_posicao):
                    botao_sound.play()

                    estado = "creditos"

                    while estado == "creditos":

                        #escreve creditos
                        texto = score_font3.render("Creditos", True, (100, 255, 100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (400, 70)
                        screen.blit(texto, text_rect)

                        #imagem do botao de voltar
                        button5 = pygame.Rect(35, 50, 90, 27)
                        pygame.draw.rect(screen, [255,255,0], button5)

                        #escreve voltar
                        texto = score_font.render("Voltar", True, (0, 255, 0))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (80, 50)
                        screen.blit(texto, text_rect)

                        #escreve Pedro
                        texto = score_font.render("Pedro", True, (255,100,100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (140, 220)
                        screen.blit(texto, text_rect)

                        #escreve Andrade
                        texto = score_font.render("Andrade", True,(255,100,100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (140,250)
                        screen.blit(texto, text_rect)

                        #escreve Luis
                        texto = score_font.render("Luis", True,(255,100,100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (380, 220)
                        screen.blit(texto, text_rect)

                        #escreve Bordignon
                        texto = score_font.render("Bordignon", True,(255,100,100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (380, 250)
                        screen.blit(texto, text_rect)

                        #escreve Thiago
                        texto = score_font.render("Thiago", True,(255,100,100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (600, 220)
                        screen.blit(texto, text_rect)

                        #escreve Shiguero
                        texto = score_font.render("Shiguero", True,(255,100,100))
                        text_rect = texto.get_rect()
                        text_rect.midtop = (600, 250)
                        screen.blit(texto, text_rect)

                        pygame.display.update()

                        for evento in pygame.event.get():
                            if evento.type == pygame.QUIT:
                                pygame.quit()
                            if evento.type == pygame.MOUSEBUTTONDOWN:
                                    #posicao do mouse
                                    mouse_posicao = evento.pos

                                    if button5.collidepoint(mouse_posicao):
                                        botao_sound.play()

                                        #volta para a tela de inicio
                                        estado = "inicio"

                        #imagem de fundo
                        screen.fill((0, 0, 0))
                        screen.blit(fundo2, (0, 0))

                        screen.blit(luisao_img, (280, 300))

                        screen.blit(thiagao_img, (510, 300))

                        screen.blit(pedrao_img, (50, 300))

        #cor da tela
        screen.fill((0, 0, 0))
        screen.blit(fundo4, (0, 0))

        #desenha retangulo do botao
        pygame.draw.rect(screen, [255,0,255], button1)
        pygame.draw.rect(screen, [255,0,255], button2)
        pygame.draw.rect(screen, [255,0,255], button4)

        #escreve navinhaaaaaaaaa
        texto = score_font3.render("navinhaaaaaaaaaaaaaa", True, (0,255,255))
        text_rect = texto.get_rect()
        text_rect = (130, 88)
        screen.blit(texto, text_rect)

        screen.blit(nave_img2, (10, 70))

        #escreve a pontuacao max
        texto = score_font.render("Maior pontuacao: {0}".format(max_p), True, (50, 255, 50))
        text_rect = texto.get_rect()
        text_rect = (30,  240)
        screen.blit(texto, text_rect)

        #mostra o PLAY do botao
        texto = score_font4.render("Play", True, (0, 0,0))
        text_rect = texto.get_rect()
        text_rect = (320, 300)
        screen.blit(texto, text_rect)

        #mostra o TUTORIAL do botao
        texto = score_font4.render("Tutorial", True, (0, 0, 0))
        text_rect = texto.get_rect()
        text_rect = (280, 430)
        screen.blit(texto, text_rect)

        #mostra o CREDITOS do botao
        texto = score_font4.render("Creditos", True, (0, 0, 0))
        text_rect = texto.get_rect()
        text_rect = (280, 580)
        screen.blit(texto, text_rect)

        pygame.display.update()

pygame.quit()
