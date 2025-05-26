import pygame
from pygame.locals import *
from sys import exit
from random import randint

#inicialização do jogo
pygame.init()

#musica de fundo
pygame.mixer.music.set_volume(0.1)
musica_de_fundo = pygame.mixer.music.load('Crash Bandicoot 1 Theme.mp3')
pygame.mixer.music.play(-1)

#barulho da colisão
barulho_colisao = pygame.mixer.Sound('smw_coin.wav')

#posição quadrado azul
largura = 640
altura = 480
x_cobra = int(largura/2)
y_cobra = int(altura / 2)

velocidade = 10
x_controle = 20
y_controle = 0

#posição quadrado verde
x_maca = int(randint(40, 600))
y_maca = int(randint(50, 430))

#pontuação
pontos = 0

#texto
fonte = pygame.font.SysFont('8-Bit-Madness', 40, True, False)

#especificações e proporções
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("jogo")
relogio = pygame.time.Clock()

morreu = False

#aumento do tamanho da cobra
def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        pygame.draw.rect(tela, (0,255,0), (XeY[0], XeY[1], 30, 30))
lista_cobra = []
comprimento_inicial = 5

def reiniciar_jogo():
    global pontos, comprimento_inicial, x_cobra, y_cobra, x_maca, y_maca, lista_cobra, lista_cabeca, morreu
    pontos = 0
    comprimento_inicial = 5
    x_cobra = int(largura / 2)
    y_cobra = int(altura / 2)
    x_maca = int(randint(40, 600))
    y_maca = int(randint(50, 430))
    lista_cobra = []
    lista_cabeca = []
    morreu = False



#intervalo infinito para gerar o jogo
while True:
    relogio.tick(30)
    tela.fill((0,20,0))
    mensagem = f'Pontos: {pontos}'
    texto_formatado = fonte.render(mensagem, False, (120,120,120))
    #fechar o jogo
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        #movimentação retilinea cobra
        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle = -velocidade
                    y_controle = 0
            if event.key == K_d:
                if x_controle == -velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0
            if event.key == K_w:
                if y_controle == velocidade:
                    pass
                else:
                    y_controle = -velocidade
                    x_controle = 0
            if event.key == K_s:
                if y_controle == -velocidade:
                    pass
                else:
                    y_controle = velocidade
                    x_controle = 0

    x_cobra = x_cobra + x_controle
    y_cobra = y_cobra + y_controle

    #especificações quadrado azul e verde
    cobra = pygame.draw.rect(tela, (0, 255, 0), (x_cobra, y_cobra, 30, 30))
    maca = pygame.draw.rect(tela, (255,0,0), (x_maca, y_maca, 20, 20))

    #condição de colisão
    if cobra.colliderect(maca):
        x_maca = randint(40, 600)
        y_maca = randint(50, 430)
        pontos += 1
        barulho_colisao.play()
        comprimento_inicial += 1

    #aumentar tamanho da cobra
    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)
    lista_cobra.append(lista_cabeca)

    if lista_cobra.count(lista_cabeca) > 1:
        fonte2 = pygame.font.SysFont('8-Bit-Madness', 30, True, False)
        mensagem = 'Game Over! Pressione a tecla "R" para jogar novamente'
        texto_formatado = fonte2.render(mensagem, False,  (200,200,200))
        ret_texto = texto_formatado.get_rect()

        morreu = True
        while morreu:
            tela.fill((50,50,50))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()
            ret_texto.center = (largura//2, altura//2)
            tela.blit(texto_formatado, (ret_texto))
            pygame.display.update()

    #ao colidir com a parede passa para o outro lado
    if x_cobra > largura:
        x_cobra = 0
    if x_cobra < 0:
        x_cobra = largura
    if y_cobra > altura:
        y_cobra = 0
    if y_cobra < 0:
        y_cobra = altura

    #limitando tamanho da cobra
    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)

    #mostrando texto
    tela.blit(texto_formatado, (450, 40))

    #deixar o jogo atualizando a cada loop do while true
    pygame.display.update()
