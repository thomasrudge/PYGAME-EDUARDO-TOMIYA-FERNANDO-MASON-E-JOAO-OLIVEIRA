import pygame
import random
from config import FPS, WIDTH, HEIGHT, BLACK
from assets import carrega_arquivos

# Função para verificar colisão entre ponto (clique do mouse) e retângulo (imagem)
def colisao_ponto_retangulo(px, py, rx, ry, rw, rh):
    return rx <= px <= rx + rw and ry <= py <= ry + rh

# Função para sortear uma nova imagem (Cachorro ou Mop), posição e velocidade
def sorteia_imagem(sheepDog_images, mop_images):
    eh_cachorro = random.choice([True, False])
    imagem = random.choice(sheepDog_images if eh_cachorro else mop_images)
    x = random.randint(0, WIDTH - imagem.get_width())
    y = random.randint(-100, -1)
    velocidade = random.randint(1, 5)
    return {'imagem': imagem, 'eh_cachorro': eh_cachorro, 'x': x, 'y': y, 'velocidade': velocidade}

# Função principal do jogo
def game_screen(window):
    clock = pygame.time.Clock()

    # Carrega as imagens de Cachorro e Mop
    dicionario_de_arquivos = carrega_arquivos()
    sheepDog_images = dicionario_de_arquivos['sheepDog']
    mop_images = dicionario_de_arquivos['Mop']

    # Estados do jogo e inicialização da contagem de vidas
    DONE = 0
    PLAYING = 1
    state = PLAYING
    vidas = 3

    # Lista para armazenar imagens sorteadas
    imagens_sorteadas = []

    # Sorteia as primeiras 5 imagens
    for _ in range(5):
        imagem_sort = sorteia_imagem(sheepDog_images, mop_images)
        imagens_sorteadas.append(imagem_sort)

    # Loop principal do jogo
    while state != DONE:
        clock.tick(FPS)

        # Tratamento de eventos (fechar janela, clique do mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = DONE
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for img in imagens_sorteadas[:]:
                    if colisao_ponto_retangulo(mx, my, img['x'], img['y'], img['imagem'].get_width(), img['imagem'].get_height()):
                        if not img['eh_cachorro']:  # Se o jogador clicar em um Mop, perde uma vida
                            vidas -= 1
                        imagens_sorteadas.remove(img)  # Remove a imagem clicada
                        for _ in range(2):  # Adiciona duas novas imagens
                            nova_imagem = sorteia_imagem(sheepDog_images, mop_images)
                            imagens_sorteadas.append(nova_imagem)
                        break

        # Preenche a tela e desenha as imagens sorteadas
        window.fill(BLACK)
        for img in imagens_sorteadas:
            img['y'] += img['velocidade']  # Move a imagem para baixo
            window.blit(img['imagem'], (img['x'], img['y']))

        # Atualiza a tela
        pygame.display.update()

        # Verifica se o jogador ainda tem vidas
        if vidas <= 0:
            state = DONE  # Encerra o jogo se o jogador ficar sem vidas

    return state
