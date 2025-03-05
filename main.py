import tkinter as tk
from tkinter import font as tkfont
import random


game_width = 1000
game_height = 700
speed = 100
space_size = 50
body_parts = 3
# Cores
snake_color = "#00FF00"
food_color = "#FF0000"
background_color = "#000000"
BACKGROUND_COLOR = "#1E1E1E"  # Cor de fundo escura
TITLE_COLOR = "#00FF00"       # Verde para o título
BUTTON_COLOR = "#333333"      # Cor dos botões
BUTTON_HOVER_COLOR = "#555555"  # Cor dos botões ao passar o mouse
TEXT_COLOR = "#FFFFFF"        # Cor do texto

# Função que cria e aumenta a cobra
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

# Função que cria a comida da cobra
class Food:
    def __init__(self, canvas, space_size, game_width, game_height, snake_coordinates):
        # Considera a altura da label subtraindo um espaço adicional
        label_buffer = 100  # Ajuste este valor conforme necessário
        
        while True:
            # Limita a geração de x entre 0 e game_width
            x = random.randint(0, int(game_width / space_size) - 1) * space_size
            
            # Limita a geração de y considerando a label
            y = random.randint(
                int(label_buffer / space_size), 
                int((game_height - label_buffer) / space_size) - 1
            ) * space_size
            
            # Verifica se a nova posição não coincide com a cobra
            if [x, y] not in snake_coordinates:
                self.coordinates = [x, y]
                canvas.create_oval(x, y, x + space_size, y + space_size, fill=food_color, tags="food")
                break

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

    if x < 0 or x >= game_width:
        return True
    elif y < 0 or y >= game_height:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

# Função para encerrar o jogo
def game_over():
    canvas.delete("all")
    canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50,
        font=('consolas', 70), text="GAME OVER!", fill="red", tag="gameover"
    )
    canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 50,
        font=('consolas', 30), text="Pressione Enter para voltar ao menu",
        fill="white", tag="gameover"
    )
    window.bind('<Return>', lambda event: return_to_menu())  # Captura a tecla "Enter"

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


# Função para mostrar o menu
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
    start_button = create_button(menu_frame, "Iniciar", start_game)
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

# Função para exibir recordes (a ser implementada)
def records():
    pass

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
        
        records.sort(key=lambda x: int(x.split(": ")[1]), reverse=True)
        
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


# Criação da janela principal
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)
window.configure(bg=BACKGROUND_COLOR)

# Variáveis do jogo
score = 0
direction = 'down'

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