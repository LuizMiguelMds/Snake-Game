import tkinter as tk
import random

game_width = 1000
game_height = 700
speed = 100
space_size = 50
body_parts = 3
snake_color = "#00FF00"
food_color = "#FF0000"
background_color = "#000000"

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
    def __init__(self):
        x = random.randint(0, int(game_width / space_size) - 1) * space_size
        y = random.randint(0, int(game_height / space_size) - 1) * space_size

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + space_size, y + space_size, fill=food_color, tags="food")

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
        food = Food()
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
    menu_frame.pack_forget()  # Esconde o menu
    label.config(text="Score: 0")  # Configura o texto antes de empacotar
    label.pack()  # Primeiro empacota a label
    canvas.pack()  # Depois empacota o canvas
    score = 0
    direction = 'down'
    snake = Snake()
    food = Food()
    next_turn(snake)


# Função para mostrar o menu
def show_menu():
    canvas.pack_forget()  # Esconde o canvas do jogo
    label.pack_forget()  # Esconde a label do score
    menu_frame.pack()  # Mostra o menu inicial

# Função para sair do jogo
def exit_game():
    window.quit()

# Função para exibir recordes (a ser implementada)
def records():
    pass

# Criação da janela principal
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

# Variáveis do jogo
score = 0
direction = 'down'

# Criação da barra do score
label = tk.Label(window, text="Score: 0", font=('consolas', 40), bg='black', fg='white')


# Criação do canvas/ambiente em que a cobra vai andar
canvas = tk.Canvas(window, bg=background_color, height=game_height, width=game_width)

# Criação do menu inicial
menu_frame = tk.Frame(window)

start_button = tk.Button(menu_frame, text="Iniciar", font=('consolas', 40), command=start_game)
start_button.pack()

records_button = tk.Button(menu_frame, text="Recordes", font=('consolas', 40), command=records)
records_button.pack()

exit_button = tk.Button(menu_frame, text="Sair", font=('consolas', 40), command=exit_game)
exit_button.pack()

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