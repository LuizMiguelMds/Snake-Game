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


#função que cria e aumenta a cobra
class snake:
    
    def __init__(self):
        self.body_size = body_parts
        self.coordinates = []
        self.squares = []

        for i in range(0, body_parts):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill = snake_color, tag = "snake")
            self.squares.append(square)
            
#Função que cria a comida da cobra
class Food:
    
    def __init__(self):
        #gerador de coordenadas da cobra
        x = random.randint(0, int(game_width / space_size) - 1) * space_size
        y = random.randint(0, int(game_height / space_size) - 1) * space_size

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + space_size, y  + space_size, fill = food_color, tags = "food")

#Função para prosseguir para o proiximo turno
def next_turn(snake):
    global food, score  # Declara food antes de usá-lo

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

    # Verifica se a cobra comeu a comida
    if x == food.coordinates[0] and y == food.coordinates[1]:  
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")  # Remove a comida antiga
        food = Food()  # Cria uma nova comida
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_colisions(snake):
        gameover()

    else:
        window.after(speed, next_turn, snake)


#Função para mudar de direção
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

#função de checagem de colisões
def check_colisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= game_width:
        return True
    elif y < 0 or y >= game_height:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("game over")
            return True

    return False    



#função para encerrar o game
def gameover():
    
    canvas.delete(all)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,font = ('consolas', 70), text = "GAME OVER", fill = "red", tag = "gameover")

# Criação da janela principal
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

# Variáveis do jogo
score = 0
direction = 'down'

#criação da barra do score
label = tk.Label(window, text = "Score:{}".format(score), font = ('consolas', 40))
label.pack()

#criação do canvas/ambiente em que a cobra vai andar
canvas = tk.Canvas(window, bg = background_color, height = game_height, width = game_width)
canvas.pack()

#Atualiza a janela para garantir que as dimensões sejam calculadas corretamente
window.update()

#Dimensões da janela e da tela
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calcula a posição central da janela
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

# Define a geometria da janela (centralizada)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))


snake = snake()
food = Food()

next_turn(snake)

#inicia o loop principal
window.mainloop()
