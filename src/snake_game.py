import pygame
import random
import sys

# --- Constantes do Jogo ---
# Cores
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Dimensões da tela e do "tijolo" da cobra
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BOX_SIZE = 20

# Velocidade da cobra (controla o quão rápido a cobra se move)
SNAKE_SPEED = 0.15 # Tempo em segundos entre cada movimento

class SnakeGame:
    """
    Classe principal para o jogo da cobrinha.
    Gerencia a lógica do jogo, renderização e entrada do usuário.
    """
    def __init__(self):
        """
        Inicializa o Pygame, a janela do jogo, a cobra, a comida e as variáveis do jogo.
        """
        pygame.init() # Inicializa todos os módulos do Pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Cria a janela do jogo
        pygame.display.set_caption("Snake Game") # Define o título da janela

        self.clock = pygame.time.Clock() # Cria um objeto Clock para controlar a taxa de quadros
        self.last_move_time = pygame.time.get_ticks() # Registra o tempo do último movimento da cobra

        self.box_size = BOX_SIZE
        self.snake_speed = SNAKE_SPEED
        self.max_length = 5 # Comprimento inicial da cobra

        # Inicializa a cobra com um único segmento no centro da tela
        # A cobra é uma lista de retângulos (pygame.Rect)
        initial_x = (SCREEN_WIDTH // 2 // self.box_size) * self.box_size
        initial_y = (SCREEN_HEIGHT // 2 // self.box_size) * self.box_size
        self.snake = [pygame.Rect(initial_x, initial_y, self.box_size, self.box_size)]

        # Direção inicial da cobra (movendo para a direita)
        self.direction = (self.box_size, 0) # (x, y) - (20, 0) para direita, (-20, 0) para esquerda, etc.

        self.food = None # A comida será um retângulo (pygame.Rect)
        self.spawn_food() # Gera a primeira comida

        self.game_over = False # Flag para controlar o estado do jogo

    def spawn_food(self):
        """
        Gera uma nova posição aleatória para a comida na tela.
        A posição é sempre um múltiplo do tamanho do "tijolo" (BOX_SIZE)
        para se alinhar com a grade do jogo.
        """
        while True:
            # Gera coordenadas aleatórias dentro dos limites da tela, alinhadas à grade
            x = random.randrange(0, SCREEN_WIDTH // self.box_size) * self.box_size
            y = random.randrange(0, SCREEN_HEIGHT // self.box_size) * self.box_size
            self.food = pygame.Rect(x, y, self.box_size, self.box_size)

            # Garante que a comida não apareça dentro do corpo da cobra
            if not any(segment.colliderect(self.food) for segment in self.snake):
                break

    def update(self):
        """
        Atualiza a lógica do jogo: move a cobra e verifica colisões.
        """
        if self.game_over:
            return

        # Controla a velocidade da cobra usando o tempo
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_move_time) / 1000.0 > self.snake_speed:
            self.move_snake()
            self.check_collision()
            self.last_move_time = current_time

    def move_snake(self):
        """
        Move a cobra: adiciona uma nova cabeça na direção atual
        e remove a cauda se a cobra não comeu.
        """
        # Cria a nova cabeça da cobra na direção atual
        current_head = self.snake[0]
        new_head_x = current_head.x + self.direction[0]
        new_head_y = current_head.y + self.direction[1]
        new_head = pygame.Rect(new_head_x, new_head_y, self.box_size, self.box_size)

        # Adiciona a nova cabeça ao início da lista da cobra
        self.snake.insert(0, new_head)

        # Se a cobra comeu a comida
        if new_head.colliderect(self.food):
            self.spawn_food() # Gera nova comida
            self.max_length += 1 # Aumenta o comprimento máximo da cobra
        elif len(self.snake) > self.max_length:
            self.snake.pop() # Remove a cauda se a cobra não atingiu o comprimento máximo

    def check_collision(self):
        """
        Verifica se a cobra colidiu com as bordas da tela ou com seu próprio corpo.
        """
        head = self.snake[0]

        # Colisão com as bordas da tela
        if (head.left < 0 or head.right > SCREEN_WIDTH or
                head.top < 0 or head.bottom > SCREEN_HEIGHT):
            self.game_over = True
            print("Game Over! Colisão com a borda.")
            return

        # Colisão com o próprio corpo
        # Começa a verificar do segundo segmento para evitar colisão com a própria cabeça
        for segment in self.snake[1:]:
            if head.colliderect(segment):
                self.game_over = True
                print("Game Over! Colisão com o próprio corpo.")
                return

    def handle_input(self):
        """
        Processa os eventos de entrada do usuário (teclado, fechar janela).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Se o botão de fechar a janela for clicado
                self.game_over = True # Define game_over como True para sair do loop principal
                pygame.quit() # Desinicializa o Pygame
                sys.exit() # Sai do programa
            elif event.type == pygame.KEYDOWN: # Se uma tecla for pressionada
                # Muda a direção da cobra, evitando que ela vire 180 graus (ex: de direita para esquerda)
                if event.key == pygame.K_UP and self.direction != (0, self.box_size):
                    self.direction = (0, -self.box_size)
                elif event.key == pygame.K_DOWN and self.direction != (0, -self.box_size):
                    self.direction = (0, self.box_size)
                elif event.key == pygame.K_LEFT and self.direction != (self.box_size, 0):
                    self.direction = (-self.box_size, 0)
                elif event.key == pygame.K_RIGHT and self.direction != (-self.box_size, 0):
                    self.direction = (self.box_size, 0)

    def render(self):
        """
        Desenha todos os elementos do jogo na tela.
        """
        self.screen.fill(BLACK) # Preenche o fundo da tela com preto

        # Desenha a cobra
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN, segment) # Desenha um retângulo verde para cada segmento

        # Desenha a comida
        if self.food:
            pygame.draw.rect(self.screen, RED, self.food) # Desenha um retângulo vermelho para a comida

        pygame.display.flip() # Atualiza a tela (mostra o que foi desenhado)

    def run(self):
        """
        O loop principal do jogo.
        """
        while not self.game_over:
            self.handle_input() # Lida com a entrada do usuário
            self.update()       # Atualiza a lógica do jogo
            self.render()       # Desenha os elementos na tela
            self.clock.tick(60) # Limita a taxa de quadros a 60 FPS (quadros por segundo)

        # Se o jogo terminar, desinicializa o Pygame e fecha a janela
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = SnakeGame() # Cria uma instância do jogo
    game.run()         # Inicia o loop principal do jogo
