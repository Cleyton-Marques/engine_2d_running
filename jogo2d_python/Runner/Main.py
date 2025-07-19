import pygame
import random
import os 

# Inicialização
pygame.init()

pygame.mixer.init()

pulo=pygame.mixer.Sound("Sons/jump.wav")

# Tamanho da janela
WIDTH, HEIGHT = 800, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quadrado Runner")

# Cores 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (220, 20, 60)

# Relógio e fonte
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


SPRITES_DIR = 'sprites'

try:
    # Imagem do Jogador
    player_image = pygame.image.load(os.path.join(SPRITES_DIR, 'protagonista.png')).convert_alpha()
    player_image = pygame.transform.scale(player_image, (70, 70)) 
except pygame.error as e:
    print(f"Erro ao carregar 'protagonista.png': {e}. Usando um quadrado azul como fallback.")
    player_image = pygame.Surface((70, 70)) # Fallback: superfície azul
    player_image.fill(BLUE)

try:
    # Imagem do Obstáculo
    obstacle_image = pygame.image.load(os.path.join(SPRITES_DIR, 'caixa3.png')).convert_alpha()
    obstacle_image = pygame.transform.scale(obstacle_image, (70, 70))
except pygame.error as e:
    print(f"Erro ao carregar 'caixa.png': {e}. Usando um quadrado vermelho como fallback.")
    obstacle_image = pygame.Surface((70, 70)) # Fallback: superfície vermelha
    obstacle_image.fill(RED)


inimigo_voador=pygame.image.load("sprites/fogo.png")
inimigo_voador = pygame.transform.scale(inimigo_voador, (70,70))


# Jogador
player_width, player_height = player_image.get_size()
player = pygame.Rect(100, HEIGHT - player_height -50  , player_width, player_height)
velocity_y = 0
gravity = 1
jump_force = -18
is_jumping = False

speed = 10
acceleration = 5
max_speed = 12
min_speed = 10

# Obstáculos
obstacles = []
obstacle_timer = 0
obstacle_interval = 1500    # em milissegundos



#background
background_image = pygame.image.load("sprites/background.png")

# Função para criar um obstáculo
def create_obstacle():

    obs_width, obs_height = obstacle_image.get_size()

    return pygame.Rect(WIDTH + random.randint(150, 400), HEIGHT - obs_height - 50, obs_width, obs_height)

# Pontuação
score = 0

# Loop principal
running = True
while running:
    dt = clock.tick(60) # Delta time para controlar a criação de obstáculos por tempo
    win.blit(background_image,(0,0))

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controles 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        speed = min(speed + acceleration, max_speed)
    else:
        speed = max(speed - acceleration, min_speed)

    # Pulo
    if keys[pygame.K_SPACE] and not is_jumping:
        pulo.play()

        velocity_y = jump_force
        is_jumping = True

    # Atualiza o jogador (pulo e gravidade)
    player.y += velocity_y
    velocity_y += gravity

    # Garante que o jogador não caia pelo chão
    if player.bottom >= HEIGHT - 50: 
        player.bottom = HEIGHT - 50 
        is_jumping = False
        velocity_y = 0 

    # Criação de obstáculos
    obstacle_timer += dt
    if obstacle_timer >= obstacle_interval:
        if random.choice([True, False]):
            obstacles.append(create_obstacle())
        obstacle_timer = 0


    # Movimenta, desenha e verifica colisão dos obstáculos
    for obstacle in obstacles[:]: 
        obstacle.x -= int(speed) 

        # --- DESENHA A IMAGEM DO OBSTÁCULO ---
        win.blit(obstacle_image, obstacle) 

        # Colisão
        if player.colliderect(obstacle):
            print("💥 GAME OVER! Pontuação:", score)
            running = False

        # Remove obstáculos que saíram da tela e aumenta a pontuação
        if obstacle.right < 0:
            obstacles.remove(obstacle)
            score += 1

    # --- DESENHA A IMAGEM DO JOGADOR ---
    win.blit(player_image, player) 

    # Linha do chão


    # Pontuação
    score_text = font.render(f"Pontos: {score}", True, BLACK)
    win.blit(score_text, (10, 10))
    
    # Atualiza a tela
    pygame.display.update()

# Finaliza o Pygame ao sair do loop principal
pygame.quit()