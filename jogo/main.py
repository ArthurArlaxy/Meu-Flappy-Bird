import pygame, os, random
from time import sleep


TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
TELA_INICIAL = pygame.image.load(os.path.join('imgs', 'Telainicial.png'))
IMAGENS_PASSARO1 = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'frame-1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'frame-2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'frame-3.png')))
]
IMAGENS_PASSARO2 = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]
IMAGEM_PASSAROS = []
IMAGEM_PASSAROS.append(IMAGENS_PASSARO1[:])
IMAGEM_PASSAROS.append(IMAGENS_PASSARO2[:])

pygame.font.init()
flappy_font = os.path.join('font', 'PressStart2P-Regular.ttf' ) # Fonte importada do Google
flappy_point = os.path.join('font', 'flappy-bird-font.ttf' ) # Fonte importada estilo Flappy Bird
FONTE_POINTS = pygame.font.Font(flappy_point, 50)
FONTE_GAME = pygame.font.Font(flappy_font, 18)



class Passaro:
    IMGS = IMAGEM_PASSAROS[0]
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 1.5

        self.y += deslocamento

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def tela_inicial(tela):
    tela.blit(TELA_INICIAL, (0, 0))

    pygame.display.update()

    esperando = True
    while esperando:
        pygame.time.wait(10)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    esperando = False
                elif evento.key == pygame.K_n:
                    pygame.quit()
                    quit()


def desenhar_tela(tela, passaro, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    if passaro:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_POINTS.render(f"{pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def game_over(tela, pontos):
    # Texto de Game Over com pontuação
    game_over_texto = FONTE_GAME.render('GAME OVER', 1, (255, 255, 255))
    pontuacao_texto = FONTE_GAME.render(f'Pontuacao final: {pontos}', 1, (255, 255, 255))
    reiniciar_texto = FONTE_GAME.render(f"'Y' para Reiniciar",1, (255, 255, 255))
    
    tela.blit(game_over_texto, (TELA_LARGURA / 2 - game_over_texto.get_width() / 2, TELA_ALTURA / 2 - game_over_texto.get_height() / 2 - 30))
    tela.blit(pontuacao_texto, (TELA_LARGURA / 2 - pontuacao_texto.get_width() / 2, TELA_ALTURA / 2 - pontuacao_texto.get_height() / 2 + 10))
    tela.blit(reiniciar_texto, (TELA_LARGURA / 2 - reiniciar_texto.get_width() / 2, TELA_ALTURA / 2 - reiniciar_texto.get_height() / 2 + 50))

    pygame.display.update()

    #While que espera por um tempo e aguarda a tecla "Y" para reiniciar
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_y:
                    esperando = False  # Sai do loop para reiniciar o jogo
                elif evento.key == pygame.K_n:
                    pygame.quit()  # Fecha o jogo se pressionar "N"
                    quit()

def main():
    passaro = Passaro(230, 350)
    chao = Chao(700)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    tela_inicial(tela)
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    passaro.pular()

        passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            if cano.colidir(passaro):
                rodando = False  # Fim do jogo se houver colisão
            if not cano.passou and passaro.x > cano.x:
                cano.passou = True
                adicionar_cano = True
            cano.mover()
        if cano.x + cano.CANO_TOPO.get_width() < 0:
            remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        if passaro.y + passaro.imagem.get_height() > chao.y or passaro.y < 0:
            rodando = False  # Fim do jogo se o pássaro tocar o chão ou sair da tela


        desenhar_tela(tela, passaro, canos, chao, pontos)

        if not rodando:
            game_over(tela, pontos)  # Passa para a tela de Game Over
            passaro = Passaro(230, 350)# Reseta o pássaro
            canos = [Cano(700)]#Reseta canos
            pontos = 0#Reseta pontos
            rodando = True#Reinicia o jogo

if __name__ == '__main__':
    main()
