# importar libs
import pygame
import time
import random

velocidade_cobra = 15

# tamanho da janela
altura = 720
largura = 480

# cores
preto = pygame.Color(0, 0, 0)  # fundo
branco = pygame.Color(255, 255, 255)  # fonte
vermelho = pygame.Color(255, 0, 0)  # fruta
verde = pygame.Color(0, 255, 0)  # cobra

# iniciar pygame
pygame.init()

# iniciar janela
pygame.display.set_caption("Jogo da Cobrinha")  # nome da janela
janela_jogo = pygame.display.set_mode((altura, largura))

# controle do FPS (frames por segundo)
fps = pygame.time.Clock()

# define a posição inicial da cobra
posicao_cobra = [100, 50]

# define os primeiros 4 blocos iniciais do corpo da cobra
corpo_cobra = [[100, 50], [90, 50], [80, 50], [70, 50]]

# posição da fruta
posicao_fruta = [
    random.randrange(1, (altura // 10)) * 10,
    random.randrange(1, (largura // 10)) * 10,
]

spawn_fruta = True

# define a direção em que a cobra começa a se movimentar
direcao = "RIGHT"  # cobra começa a se movimentar para direita
mudar_para = direcao

# valor inicial da pontuação
score = 0


# função da pontuação
def mostrar_score(choice, color, font, size):
    # fonte do texto da pontuação
    score_fonte = pygame.font.SysFont(font, size)
    # mostra o texto da pontuação durante a partida
    score_render = score_fonte.render("Score: " + str(score), True, color)
    # cria retangulo para o texto
    score_retangulo = score_render.get_rect()
    janela_jogo.blit(score_render, score_retangulo)


# função do fim do jogo
def fimdejogo():
    # fonte do utilizada na tela de fim de jogo
    minha_fonte = pygame.font.SysFont("times new roman", 50)

    fimdejogo_render = minha_fonte.render(
        "Sua pontuação é : " + str(score), True, branco
    )

    fimdejogo_retangulo = fimdejogo_render.get_rect()

    # posição do texto
    fimdejogo_retangulo.midtop = (altura / 2, largura / 4)

    janela_jogo.blit(fimdejogo_render, fimdejogo_retangulo)
    pygame.display.flip()

    # após 4 seg o programa fecha
    time.sleep(2)

    # sai do pygame
    pygame.quit()

    # sai do programa
    quit()


# função principal
while True:
    # controles do jogo
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                mudar_para = "UP"
            if event.key == pygame.K_DOWN:
                mudar_para = "DOWN"
            if event.key == pygame.K_LEFT:
                mudar_para = "LEFT"
            if event.key == pygame.K_RIGHT:
                mudar_para = "RIGHT"

    # caso duas teclas sejam pressionadas ao mesmo tempo
    # isso deve previnir que a cobra ande para duas direções
    # ao mesmo tempo
    if mudar_para == "UP" and direcao != "DOWN":
        direcao = "UP"
    if mudar_para == "DOWN" and direcao != "UP":
        direcao = "DOWN"
    if mudar_para == "LEFT" and direcao != "RIGHT":
        direcao = "LEFT"
    if mudar_para == "RIGHT" and direcao != "LEFT":
        direcao = "RIGHT"

    # move a cobra
    if direcao == "UP":
        posicao_cobra[1] -= 10
    if direcao == "DOWN":
        posicao_cobra[1] += 10
    if direcao == "LEFT":
        posicao_cobra[0] -= 10
    if direcao == "RIGHT":
        posicao_cobra[0] += 10

    # mecanismo da cobra crescer caso a fruta e a cobra
    # colidam a pontuação aumenta em 10 pontos
    corpo_cobra.insert(0, list(posicao_cobra))
    if posicao_cobra[0] == posicao_fruta[0] and posicao_cobra[1] == posicao_fruta[1]:
        score += 10
        spawn_fruta = False
    else:
        corpo_cobra.pop()

    if not spawn_fruta:
        posicao_fruta = [
            random.randrange(1, (altura // 10)) * 10,
            random.randrange(1, (largura // 10)) * 10,
        ]

    spawn_fruta = True
    janela_jogo.fill(preto)

    for pos in corpo_cobra:
        pygame.draw.rect(janela_jogo, verde, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(
        janela_jogo, vermelho, pygame.Rect(posicao_fruta[0], posicao_fruta[1], 10, 10)
    )

    # condições de fim de jogo
    if posicao_cobra[0] < 0 or posicao_cobra[0] > altura - 10:
        fimdejogo()
    if posicao_cobra[1] < 0 or posicao_cobra[1] > largura - 10:
        fimdejogo()

    # ao tocar a cobra
    for block in corpo_cobra[1:]:
        if posicao_cobra[0] == block[0] and posicao_cobra[1] == block[1]:
            fimdejogo()

    # a pontuação sempre fica visivel na tela
    mostrar_score(1, branco, "times new roman", 20)

    # atualiza a tela de jogo
    pygame.display.update()

    # FPS & atualização de quadros
    fps.tick(velocidade_cobra)
