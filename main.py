import tkinter as tk
from tkinter import simpledialog
import random

# Configurações iniciais do jogo
game_width = 1000
game_height = 700
speed = 100  # Velocidade padrão (Médio)
space_size = 50
body_parts = 3
snake_color = "#00FF00"  # Verde (padrão)
food_color = "#FF0000"   # Vermelho
background_color = "#000000"  # Preto (padrão)

# Cores do menu
BACKGROUND_COLOR = "#1E1E1E"  # Cor de fundo escura
TITLE_COLOR = "#00FF00"       # Verde para o título
BUTTON_COLOR = "#333333"      # Cor dos botões
BUTTON_HOVER_COLOR = "#555555"  # Cor dos botões ao passar o mouse
TEXT_COLOR = "#FFFFFF"        # Cor do texto

# Objeto da cobra
class Snake:
    def __init__(self):
        self.body_size = body_parts
        self.coordinates = []
        self.squares = []

        for i in range(0, body_parts):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, canvas, space_size, game_width, game_height, snake_coordinates):
        max_x = int(game_width / space_size) - 1
        max_y = int((game_height - 50) / space_size) - 1  # Subtrai 50 pixels para a label
        
        attempts = 0
        max_attempts = 100
        
        while attempts < max_attempts:
            x = random.randint(0, max_x) * space_size
            y = random.randint(0, max_y) * space_size
            
            print(f"Attempting food generation: x={x}, y={y}")
            print(f"Canvas limits - Width: {game_width}, Height: {game_height}")
            print(f"Max X: {max_x}, Max Y: {max_y}")
            print(f"Snake coordinates: {snake_coordinates}")
            
            if ([x, y] not in snake_coordinates and 
                0 <= x < game_width and 
                0 <= y < (game_height - 50)):  # Ajusta limite superior para considerar a label
                self.coordinates = [x, y]
                print(f"Food successfully generated at: x={x}, y={y}")
                canvas.create_oval(
                    x, y, 
                    x + space_size, y + space_size, 
                    fill=food_color, 
                    tags="food"
                )
                return
            
            attempts += 1
        
        # Fallback: se não conseguir gerar comida, usa uma posição padrão
        x = (max_x // 2) * space_size
        y = (max_y // 2) * space_size
        self.coordinates = [x, y]
        print(f"Fallback food generation at: x={x}, y={y}")
        canvas.create_oval(
            x, y, 
            x + space_size, y + space_size, 
            fill=food_color, 
            tags="food"
        )

# Função para prosseguir para o próximo turno
def next_turn(snake):
    global food, score
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= space_size
    elif direction == "down":
        y += space_size
    elif direction == "left":
        x -= space_size
    elif direction == "right":
        x += space_size
    
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill=snake_color)
    snake.squares.insert(0, square)
    
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food(canvas, space_size, game_width, game_height, snake.coordinates)
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    if check_collisions(snake):
        game_over()
    else:
        window.after(speed, next_turn, snake)

# Função para mudar de direção
def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

# Função de checagem de colisões
def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Verifica colisões com as bordas
    if x < 0:  # Borda esquerda
        return True
    elif x >= game_width:  # Borda direita (sem subtrair space_size)
        return True
    elif y < 0:  # Borda superior
        return True
    elif y >= game_height:  # Borda inferior
        return True

    # Verifica colisão com o próprio corpo
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete("all")
    canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50,
        font=('consolas', 70), text="GAME OVER!", fill="red", tag="gameover"
    )
    canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2,
        font=('consolas', 40), text=f"Score: {score}", fill="white", tag="gameover"
    )
    canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 50,
        font=('consolas', 30), text="Pressione Enter para continuar",
        fill="white", tag="gameover"
    )
    
    # Remove qualquer binding anterior
    window.unbind('<Return>')
    
    # Cria um novo binding para salvar a pontuação
    window.bind('<Return>', lambda event: save_score_and_return_delayed(score))

def save_score_and_return_delayed(final_score):
    # Usa after para garantir que a interface esteja responsiva
    window.after(100, lambda: save_score(final_score))
    return_to_menu()

# Função para retornar ao menu
def return_to_menu():
    canvas.delete("all")
    show_menu()
    window.unbind('<Return>')  # Remove o evento de "Enter" após retornar ao menu

# Função para iniciar o jogo
def start_game():
    global snake, food, score, direction
    menu_frame.pack_forget()
    label.config(text="Score: 0")
    label.pack()
    canvas.pack()
    score = 0
    direction = 'down'
    snake = Snake()
    food = Food(canvas, space_size, game_width, game_height, snake.coordinates)
    next_turn(snake)

# Função para mostrar o menu de dificuldade
def show_difficulty_menu():
    # Limpa o menu_frame antes de adicionar novos widgets
    for widget in menu_frame.winfo_children():
        widget.destroy()

    # Título do menu de dificuldade
    title_label = tk.Label(
        menu_frame,
        text="Selecione a Dificuldade",
        font=('consolas', 50, 'bold'),
        fg=TITLE_COLOR,
        bg=BACKGROUND_COLOR
    )
    title_label.pack(pady=50)

    # Botão "Fácil"
    easy_button = create_button(menu_frame, "Fácil", lambda: set_difficulty("Fácil"))
    easy_button.pack(pady=20)

    # Botão "Médio"
    medium_button = create_button(menu_frame, "Médio", lambda: set_difficulty("Médio"))
    medium_button.pack(pady=20)

    # Botão "Difícil"
    hard_button = create_button(menu_frame, "Difícil", lambda: set_difficulty("Difícil"))
    hard_button.pack(pady=20)

    # Botão "Voltar ao Menu"
    back_button = create_button(menu_frame, "Voltar ao Menu", show_menu)
    back_button.pack(pady=20)

    # Garante que o menu_frame esteja visível
    menu_frame.pack(expand=True, fill="both")

# Função para definir a dificuldade
def set_difficulty(difficulty):
    global speed, snake_color, background_color, current_difficulty

    if difficulty == "Fácil":
        speed = 150
        snake_color = "#90EE90"
        background_color = "#ADD8E6"
        current_difficulty = "Fácil"
    elif difficulty == "Médio":
        speed = 100
        snake_color = "#00FF00"
        background_color = "#000000"
        current_difficulty = "Médio"
    elif difficulty == "Difícil":
        speed = 50
        snake_color = "#00008B"
        background_color = "#FFFF00"
        current_difficulty = "Difícil"

    # Atualiza as cores do canvas
    canvas.config(bg=background_color)
    start_game()

# Função para mostrar o menu inicial
def show_menu():
    # Esconde o canvas e a label do score
    canvas.pack_forget()
    label.pack_forget()

    # Limpa o menu_frame antes de adicionar novos widgets
    for widget in menu_frame.winfo_children():
        widget.destroy()

    # Título do jogo
    title_label = tk.Label(
        menu_frame,
        text="Snake Game",
        font=('consolas', 50, 'bold'),
        fg=TITLE_COLOR,
        bg=BACKGROUND_COLOR
    )
    title_label.pack(pady=50)

    # Botão "Iniciar"
    start_button = create_button(menu_frame, "Iniciar", show_difficulty_menu)
    start_button.pack(pady=20)

    # Botão "Recordes"
    records_button = create_button(menu_frame, "Recordes", records)
    records_button.pack(pady=20)

    # Botão "Sair"
    exit_button = create_button(menu_frame, "Sair", exit_game)
    exit_button.pack(pady=20)

    # Mostra o menu_frame
    menu_frame.pack(expand=True, fill="both")

# Função para sair do jogo
def exit_game():
    window.quit()

# Função para criar botões estilizados
def create_button(parent, text, command):
    button = tk.Button(
        parent,
        text=text,
        font=('consolas', 20),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        activebackground=BUTTON_HOVER_COLOR,
        activeforeground=TEXT_COLOR,
        relief="flat",
        borderwidth=0,
        command=command
    )
    button.bind("<Enter>", lambda e: button.config(bg=BUTTON_HOVER_COLOR))
    button.bind("<Leave>", lambda e: button.config(bg=BUTTON_COLOR))
    return button

# Função para salvar a pontuação
def save_score(score):
    player_name = simpledialog.askstring("Recorde", "Digite seu nome:", parent=window)
    if player_name:
        with open("records.txt", "a") as file:
            file.write(f"{player_name}: {score}\n")

# Função para exibir os recordes
def show_records():
    try:
        with open("records.txt", "r") as file:
            records = file.readlines()
        
        # Ordena os recordes por pontuação (número antes do parênteses)
        records.sort(key=lambda x: int(x.split(":")[1].split("(")[0].strip()), reverse=True)
        
        for widget in menu_frame.winfo_children():
            widget.destroy()
        
        title_label = tk.Label(
            menu_frame,
            text="Recordes",
            font=('consolas', 50, 'bold'),
            fg=TITLE_COLOR,
            bg=BACKGROUND_COLOR
        )
        title_label.pack(pady=20)

        for record in records[:10]:
            record_label = tk.Label(
                menu_frame,
                text=record.strip(),
                font=('consolas', 20),
                fg=TEXT_COLOR,
                bg=BACKGROUND_COLOR
            )
            record_label.pack(pady=5)

        back_button = create_button(menu_frame, "Voltar ao Menu", show_menu)
        back_button.pack(pady=20)

    except FileNotFoundError:
        no_records_label = tk.Label(
            menu_frame,
            text="Nenhum recorde encontrado!",
            font=('consolas', 30),
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR
        )
        no_records_label.pack(pady=50)

        back_button = create_button(menu_frame, "Voltar ao Menu", show_menu)
        back_button.pack(pady=20)

# Função para exibir o menu de recordes
def records():
    show_records()

# Função para salvar a pontuação
def save_score(score):
    player_name = simpledialog.askstring("Recorde", "Digite seu nome:", parent=window)
    if player_name:
        with open("records.txt", "a") as file:
            # Salva nome, pontuação e dificuldade
            file.write(f"{player_name}: {score} (Dificuldade: {current_difficulty})\n")

# Criação da janela principal
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)
window.configure(bg=BACKGROUND_COLOR)

# Variáveis do jogo
score = 0
direction = 'down'
current_difficulty = "Médio"

# Criação da barra do score
label = tk.Label(window, text="Score: 0", font=('consolas', 40), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)

# Criação do canvas/ambiente em que a cobra vai andar
canvas = tk.Canvas(window, bg=background_color, height=game_height, width=game_width)

# Criação do menu inicial
menu_frame = tk.Frame(window, bg=BACKGROUND_COLOR)

# Mostra o menu inicial ao iniciar o programa
show_menu()

# Configura o tamanho da janela para acomodar o canvas e o label
window.update()
window_width = game_width
window_height = game_height + label.winfo_height()  # Adiciona a altura do label ao tamanho da janela
window.geometry(f"{window_width}x{window_height}")

# Centraliza a janela na tela
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Vincula as teclas de direção
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Inicia o loop principal
window.mainloop()