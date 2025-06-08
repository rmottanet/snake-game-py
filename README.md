# lab-snake-game-py

Este documento fornece uma visão técnica aprofundada do projeto "Snake Game", implementado em Python utilizando a biblioteca Pygame. Destina-se a desenvolvedores e entusiastas que buscam entender a arquitetura, o funcionamento e os componentes do jogo.

### 1. Visão Geral do Projeto

O Snake Game é uma recriação do clássico jogo arcade onde o jogador controla uma cobra que se move em uma grade. O objetivo é consumir itens de "comida" que aparecem aleatoriamente na tela, fazendo com que a cobra aumente de comprimento. O jogo termina se a cobra colidir com as bordas da tela ou com seu próprio corpo. Este projeto serve como um exemplo prático de desenvolvimento de jogos 2D com Pygame, demonstrando conceitos fundamentais como:

* Manipulação de gráficos e janelas.
* Processamento de eventos de entrada (teclado).
* Lógica de atualização de estado do jogo.
* Detecção de colisões.
* Controle de tempo e velocidade.

### 2. Estrutura do Código

O projeto consiste em um único arquivo, `snake_game.py`, que encapsula toda a lógica e a interface do jogo dentro de uma classe principal.

#### `snake_game.py`

Este arquivo contém a definição da classe `SnakeGame`, que gerencia o ciclo de vida completo do jogo.

```python
# snake_game.py
import pygame
import random
import sys

# Constantes de configuração do jogo
# ... (definições de cores, dimensões e velocidade)

class SnakeGame:
    def __init__(self):
        # Inicialização do Pygame, janela e variáveis de estado
        # ...

    def spawn_food(self):
        # Lógica para gerar a comida em posições aleatórias na grade
        # ...

    def update(self):
        # Atualiza o estado do jogo (movimento da cobra, colisões) baseado no tempo
        # ...

    def move_snake(self):
        # Calcula a nova posição da cabeça e atualiza o corpo da cobra
        # ...

    def check_collision(self):
        # Verifica colisões da cobra com as bordas da tela ou com o próprio corpo
        # ...

    def handle_input(self):
        # Processa eventos de entrada do usuário (teclado, fechar janela)
        # ...

    def render(self):
        # Desenha todos os elementos do jogo na tela
        # ...

    def run(self):
        # Loop principal do jogo
        # ...

if __name__ == '__main__':
    # Cria e executa a instância do jogo
    # ...
```

---

### 3. Detalhamento Técnico dos Componentes

#### 3.1. Variáveis de Configuração Global

As **constantes** definidas no início do arquivo `snake_game.py` parametrizam o comportamento visual e lógico do jogo:

* **Cores (`GREEN`, `RED`, `BLACK`)**: Tuplas RGB que definem as cores dos elementos gráficos.
* **Dimensões da Tela (`SCREEN_WIDTH`, `SCREEN_HEIGHT`)**: Resolução da janela de exibição em pixels.
* **Tamanho do Bloco (`BOX_SIZE`)**: Dimensão em pixels de cada segmento da cobra e da comida, garantindo um alinhamento preciso em uma grade virtual.
* **Velocidade da Cobra (`SNAKE_SPEED`)**: Intervalo de tempo (em segundos) entre cada movimento da cobra, controlando a dificuldade do jogo.

#### 3.2. Classe `SnakeGame`

##### a. `__init__(self)`

O construtor da classe é responsável pela **inicialização do ambiente Pygame**, a configuração da **janela de exibição** (`self.screen`) e a definição dos **estados iniciais** do jogo. A cobra é representada por uma `list` de objetos `pygame.Rect`, onde `self.snake[0]` é a cabeça. A direção do movimento (`self.direction`) é um vetor `(dx, dy)` que indica o deslocamento por `BOX_SIZE`.

##### b. `spawn_food(self)`

Este método gera a **posição da comida** (`self.food`) aleatoriamente dentro da grade do jogo. Uma validação crucial é implementada para garantir que a comida **não seja posicionada sobre nenhum segmento da cobra**, evitando situações de jogo impossíveis ou indesejadas. A verificação é feita utilizando o método `colliderect()` de `pygame.Rect`.

##### c. `update(self)`

O método `update` gerencia a **lógica temporal** do jogo. Ele utiliza `pygame.time.get_ticks()` e `self.last_move_time` para controlar a **velocidade de movimento da cobra** de forma independente da taxa de quadros (FPS). A cobra se move apenas quando o tempo decorrido excede `self.snake_speed`.

##### d. `move_snake(self)`

Esta função implementa o **movimento da cobra**. Uma nova "cabeça" (`pygame.Rect`) é calculada com base na direção atual e adicionada ao início da lista `self.snake` usando `insert(0, ...)`.
* Se a nova cabeça colidir com a comida (`new_head.colliderect(self.food)`), a comida é regenerada e o comprimento máximo da cobra (`self.max_length`) é incrementado.
* Caso contrário, o último segmento da cobra é removido (`self.snake.pop()`), simulando o deslocamento.

##### e. `check_collision(self)`

Este método verifica as **condições de fim de jogo**:
* **Colisão com as bordas**: A cabeça da cobra é verificada em relação aos limites `SCREEN_WIDTH` e `SCREEN_HEIGHT`.
* **Colisão com o próprio corpo**: Itera sobre os segmentos da cobra (excluindo a própria cabeça) para detectar sobreposições usando `colliderect()`.
Em caso de qualquer colisão, a flag `self.game_over` é definida como `True`, sinalizando o encerramento do jogo.

##### f. `handle_input(self)`

Responsável pelo **processamento de eventos de entrada** do usuário. Utiliza `pygame.event.get()` para capturar eventos como o fechamento da janela (`pygame.QUIT`) e o pressionamento de teclas (`pygame.KEYDOWN`). As teclas de seta (UP, DOWN, LEFT, RIGHT) são mapeadas para alterar a `self.direction` da cobra, com uma lógica para **impedir que a cobra inverta 180 graus** instantaneamente.

##### g. `render(self)`

Este método cuida da **renderização gráfica**. A tela é limpa a cada quadro (`self.screen.fill(BLACK)`). Em seguida, cada segmento da cobra e o objeto da comida são desenhados usando `pygame.draw.rect()`. A função `pygame.display.flip()` é utilizada para atualizar a exibição da tela, mostrando os elementos desenhados.

##### h. `run(self)`

O `run` é o **loop principal do jogo**. Ele executa continuamente enquanto `self.game_over` for `False`, chamando em sequência `handle_input()`, `update()` e `render()`. A linha `self.clock.tick(60)` impõe um limite máximo de 60 quadros por segundo (FPS), garantindo uma experiência de jogo suave e consistente em diferentes ambientes de hardware. Ao sair do loop (jogo encerrado), `pygame.quit()` e `sys.exit()` são chamados para uma finalização limpa do programa.

---

### 4. Requisitos e Execução

Para configurar e executar o projeto, siga os passos abaixo:

#### 4.1. Pré-requisitos

* **Python 3.x**: Certifique-se de ter uma versão compatível do Python instalada.
* **Pygame**: A biblioteca Pygame é a única dependência externa.

#### 4.2. Instalação de Dependências

Instale o Pygame via `pip`, o gerenciador de pacotes do Python:

```bash
pip install pygame
```

#### 4.3. Como Executar

1.  **Clone o repositório** ou baixe o arquivo `snake_game.py`.
2.  **Navegue até o diretório** onde o arquivo está salvo via terminal ou prompt de comando.
3.  **Execute o script** Python:

    ```bash
    python snake_game.py
    ```

Após a execução, uma janela contendo o jogo será exibida, e você poderá controlá-lo usando as **setas do teclado**.

---
