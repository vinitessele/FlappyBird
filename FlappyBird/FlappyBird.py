import pygame #Biblioteca de criação de jogos
import os #Biblioteca integrar codigo com os arquivos(imgs) do computador
import random #Biblioteca de geração de números aleatórios
import neat #Biblioteca da Inteligência Artificial

ai_jogando = True #Quando for True é a IA e quando for False é o usuario jogando
geracao = 0 #Geração inicial

TELA_LARGURA = 500 #Definindo o tamanho da largura da tela
TELA_ALTURA =  800 #Definindo o tamanho da altura da tela

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load('D:\\Aulas Práticas 2024-2\\projetos\\Projeto_FlappyBird_Py-main\\imgs\\pipe.png')) #Imagem do cano
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load('D:\\Aulas Práticas 2024-2\\projetos\\Projeto_FlappyBird_Py-main\\imgs\\base.png')) #Imagem do chão
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load('D:\\Aulas Práticas 2024-2\\projetos\\Projeto_FlappyBird_Py-main\\imgs\\bg.png')) #Imagem do fundo
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load('D:\\Aulas Práticas 2024-2\\projetos\\Projeto_FlappyBird_Py-main\\imgs\\bird1.png')), #Imagem passaro 1
    pygame.transform.scale2x(pygame.image.load('D:\\Aulas Práticas 2024-2\\projetos\\Projeto_FlappyBird_Py-main\\imgs\\bird2.png')), #Imagem passaro 2
    pygame.transform.scale2x(pygame.image.load('D:\\Aulas Práticas 2024-2\\projetos\\Projeto_FlappyBird_Py-main\\imgs\\bird3.png')), #Imagem passaro 3
]

pygame.font.init() #Definindo a fonte e tamanho das letras
FONTE_PONTOS = pygame.font.SysFont('arial', 40)

#Passáro:
class Passaro:
    IMGS = IMAGENS_PASSARO #Inserindo a constante na variavel
    #Animações da rotação:
    ROTACAO_MAXIMA = 25 #Rotação maxima do passaro
    VELOCIDADE_ROTACAO = 20 #Velocidade da rotação do passaro
    TEMPO_ANIMACAO = 6 #Tempo da animação do passaro

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0 #Angulo do passaro
        self.velocidade = 0 #Velocidade do passaro para cima e para baixo
        self.altura = self.y #Definindo a altura do passaro que será a posição dele no eixo y

        #Definindo parametos auxiliares
        self.tempo = 0 #Tempo do movimento/pulo do passaro
        self.contagem_imagem = 0 #Qual a imagem do passaro está sendo utilizada no momento(bird1;bird2;bird3)
        self.imagem = self.IMGS[0] #Primeira imagem da lista

    def pular(self): #Definindo a função de pular
        self.velocidade = -10.5 #Definindo a velocidade para ele poder subir
        self.tempo = 0 #Zerando o atributo do tempo
        self.altura = self.y

    def mover(self): #Definindo a função de se mover
    #Calcular deslocamento
        self.tempo +=1 #A cada --tempo muito curto-- essa função irá rodar
        deslocamento = 1.9 * (self.tempo**2) + self.velocidade * self.tempo #Formula: S = so +  vo . t + at² /2. (sorvetão)

    #Restringir deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0: 
            deslocamento -= 2  #Quando o passarinho pular ele terá um "ganho" de pulo
        self.y += deslocamento               

    #Angulo do passaro    
    
        if deslocamento < 0 or self.y < (self.altura + 50): #Se a posição y do passaro ainda é abaixo da posição dele o passaro ficará inclinado (jogo de animação)
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA #Se ele nao esta todo virado para cima, ele deve voltar todo para cima
        else:
            if self.angulo > -90: 
                self.angulo -= self.VELOCIDADE_ROTACAO #Rotacionando o passaro para baixo

    def desenhar(self, tela):
    #Definindo qual imagem do passáro será utilizado:
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO: #Se a contagem da imagem dele for menor que a primeira animação, então é a primeira imagem que está aparecendo
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]


    #Se o passaro tiver caindo a asa não irá bater:
        if self.angulo <= 80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

    #Desenhar a imagem:

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo) #Rotacionando a imagem do passaro com o angulo desejado
        #Como se desenhasse um retangulo em volta da imagem
        #Colocando o retangulo no centro:
        posicao_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=posicao_centro_imagem) 
        #Desenhando na tela
        tela.blit(imagem_rotacionada, retangulo.topleft)

#Inserindo o collider no passáro
    def get_mask(self):      
        return pygame.mask.from_surface(self.imagem)

#Cano:
class Cano:
    DISTANCIA = 170 #Distancia de um cano para o outro
    VELOCIDADE = 8 #Velocidade de movimento do cano

    def __init__(self,x):
        self.x = x #Posição do eixo x
        self.altura = 0 #Altura do cano
        self.pos_topo = 0 #Posição do topo
        self.pos_base = 0 #Posição da base
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True) #Virando a imagem do cano para baixo (img_cano, x, y)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False #Se o passaro já passou pelo cano
        self.definir_altura() #Função que irá gerar a altura do cano

    #Definindo a altura do cano
    def definir_altura(self):
        self.altura = random.randrange(50, 450) #Definindo qual será a altura/posição que o cano ficará na tela
        self.pos_topo = self.altura - self.CANO_TOPO.get_height() #Altura - Tamanho do cano
        self.pos_base= self.altura + self.DISTANCIA #Altura + a distancia

    #Movendo o cano
    def mover(self):
        self.x -= self.VELOCIDADE 

    #Desenhando o cano na tela
    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    #Criando o collider do cano
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask() #Colisor
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO) #Criando a mask das imgs
        base_mask = pygame.mask.from_surface(self.CANO_BASE) #Criando a mask das imgs
        
        #Pegando a distancia da mask do passaro para a distancia da mask do topo
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        #Pegando a distancia da mask do passaro para a distancia da mask da base
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        #Verificando se há colisão na mask do passaro e nas masks dos canos
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)
        
        if base_ponto or topo_ponto:
            return True #Se encostou no topo ou base, retorna verdadeiro que colidiu
        else:
            return False

#Chão:       
class Chao:
    VELOCIDADE = 8 #Velocidade do chão
    LARGURA = IMAGEM_CHAO.get_width() #Largura do chão
    IMAGEM = IMAGEM_CHAO #Imagem do chão

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA 
    
    #Mover o chão na tela
    def mover(self):
        self.x1 -= self.VELOCIDADE #chão 1
        self.x2 -= self.VELOCIDADE #chão 2
        
        if self.x1 + self.LARGURA < 0: #Chão 1 saiu da tela
            self.x1 = self.x2 + self.LARGURA 

        if self.x2 + self.LARGURA < 0: #Chão 2 saiu da tela
            self.x2 = self.x1 + self.LARGURA 
    
    #Desenhando o chão:
    def desenhar(self, tela):
        tela.blit(self.IMAGEM,(self.x1, self.y))
        tela.blit(self.IMAGEM,(self.x2, self.y))

#Tela
def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0,0)) #Desenhando o fundo da tela

    for passaro in passaros: #Desenhando os passaros na tela
        passaro.desenhar(tela)

    for cano in canos: #Desenhando os canos na tela
        cano.desenhar(tela)

    #Desenhando o texto dos pontos na tela, posição e cor
    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255,255,255)) 

    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

    if ai_jogando:
        texto = FONTE_PONTOS.render(f"Geração: {geracao}", 1, (255,255,255)) 
        tela.blit(texto, (10,10))

    chao.desenhar(tela)

    #Atualizando a tela do jogo
    pygame.display.update()

#Executando o jogo:
def main(genomas, config): #fitness function
    global geracao
    geracao += 1 #Aumenta +1 a geração toda vez que a executar a função main (ia)

    if ai_jogando: #As listas se interligam
        redes = []
        lista_genomas = []
        passaros = []
        for _, genoma in genomas: #Para cada genoma > criar rede neural > criar passaro
            rede = neat.nn.FeedForwardNetwork.create(genoma, config) #rede neural
            redes.append(rede)
            genoma.fitness = 0 #Pontuação do passaro (interna)
            lista_genomas.append(genoma)
            passaros.append(Passaro(230, 350))

    else:
        passaros = [Passaro(230, 350)] #Definindo a posição y e x do passaro

    chao = Chao(730) #Definindo a posição do chão

    canos = [Cano(700)] #Definindo a posição x do cano

    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA)) #Criando a tela
    
    pontos = 0 #Parametreo pontuação inicia em zero

    relogio = pygame.time.Clock() #Tempo em que atualiza as infos do jogo


#Inicializando o jogo:
    #(Enquanto o jogo estiver rodando ele será verdadeiro)
    rodando = True
    while rodando:

        relogio.tick(30) #Qtd de frames por segundo (fps)

        #Interação do usuário com o jogo
        #Eventos são as teclas de interação com o jogo
        for evento in pygame.event.get():
            if evento.type == pygame.quit:
                rodando = False
                pygame.quit()

            if not ai_jogando: #A tecla só será selecionada se nao for a ia jogando
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()
        
        indice_cano = 0 
        #descobrindo qual o cano olhar
        if len(passaros) > 0:
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].CANO_TOPO.get_width()): #(Se a posição x do passaro + a posição x do cano + a largura do cano)
                indice_cano = 1 
        else: #O jogo acaba
            rodando = False
            break 

        #Mover as coisas
        for i, passaro in enumerate(passaros):
            passaro.mover()
            #aumentar um pouquinho a fitness do passaro
            lista_genomas[i].fitness += 0.1
            output = redes[i].activate((passaro.y, 
                                        abs(passaro.y - canos[indice_cano].altura), 
                                        abs(passaro.y - canos[indice_cano].pos_base)))
            
            #-1 e 1 -> se o output for > 0.5 então o passaro pula
            if output[0] > 0.5:
                passaro.pular()
            

        chao.mover()

        adicionar_cano = False #Se o passaro passou do cano, retornara true
        remover_canos = []

        for cano in canos:
            for i, passaro in enumerate(passaros): #Pegando a posição do passaro dentro da lista
                if cano.colidir(passaro): #Se o passaro colidir com o cano, ele some
                    passaros.pop(i)
                    if ai_jogando:
                        lista_genomas[i].fitness -=1 #Penalizando a IA se enconstar no cano (-1 ponto)
                        lista_genomas.pop(i) #Tirar o passaro da lista de genomas
                        redes.pop(i) #Tirar o passaro da lista de redes

                #Checando se o passaro passou do cano: 
                if not cano.passou and passaro.x > cano.x: 
                    cano.passou = True
                    adicionar_cano = True

            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano) #Adicionando o cano que saiu da tela em uma lista de canos que precisam ser removidos

        #Adicionando novos canos na tela:
        if adicionar_cano:
            pontos += 1 
            canos.append(Cano(600)) #adicionando o cano

            for genoma in lista_genomas:
                genoma.fitness += 5 #Adicionando pontos a ia quando ela passa por um cano


        for cano in remover_canos: #Removendo os canos da lista de canos (que precisam ser removidos)
            canos.remove(cano)

        #Colisão do passáro com o céu e/ou com o chão:
        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

                if ai_jogando: #"penalizando" a ia retirando os passaros
                    lista_genomas.pop(i)
                    redes.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos) #Desenhando o jogo

def rodar(caminho_config): #Puxando as configurações da rede neural do arquivo de configs:

    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                caminho_config)
    
    populacao = neat.Population(config) #Criando a população dos passaros
    populacao.add_reporter(neat.StdOutReporter(True)) #Reportando as estatisticas da ia jogando
    populacao.add_reporter(neat.StatisticsReporter())

    if ai_jogando: #Definindo se é a IA que está jogando
        populacao.run(main, 50)
    else:
        main(None, None)

#Rodando o jogo:
if __name__ == '__main__':

    caminho = os.path.dirname(__file__) #local do arquivo do codigo.py
    
    caminho_config = os.path.join(caminho, 'Configuracao da Inteligencia Artificial [Projeto Flappy Bird].txt') #juntando o local com o config.txt

    rodar(caminho_config)
