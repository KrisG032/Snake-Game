import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

# center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# initialize game
snake = [Tile(5 * TILE_SIZE, 5 * TILE_SIZE)]  # snake body
food = Tile(random.randint(0, ROWS - 1) * TILE_SIZE, random.randint(0, COLS - 1) * TILE_SIZE)

dx = TILE_SIZE
dy = 0
score = 0
game_over = False

def move():
    global snake, food, dx, dy, score, game_over

    if game_over:
        return

    # изчисляваме новата позиция на главата
    new_head_x = (snake[0].x + dx) % WINDOW_WIDTH
    new_head_y = (snake[0].y + dy) % WINDOW_HEIGHT
    new_head = Tile(new_head_x, new_head_y)
    
    # проверка за сблъсък със себе си
    for part in snake:
        if part.x == new_head.x and part.y == new_head.y:
            end_game()
            return

    # добавяме новата глава
    snake.insert(0, new_head)
    
    # проверка за ядене на храна
    if new_head.x == food.x and new_head.y == food.y:
        score += 1
        update_title()
        food.x = random.randint(0, ROWS - 1) * TILE_SIZE
        food.y = random.randint(0, COLS - 1) * TILE_SIZE
    else:
        snake.pop()

    window.after(100, move)

def draw():
    global game_over
    canvas.delete("all")
    # рисуваме змията
    for i, part in enumerate(snake):
        color = "yellow" if i == 0 else "yellow"
        canvas.create_rectangle(part.x, part.y, part.x + TILE_SIZE, part.y + TILE_SIZE, fill=color)
    # рисуваме храната
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")

    if not game_over:
        window.after(100, draw)
    else:
        canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, fill="white", font=("Arial", 30), text="GAME OVER")

def update_title():
    window.title(f"Snake — Score: {score}")

def end_game():
    global game_over
    game_over = True
    draw()

# управление
def go_up(event):
    global dx, dy
    if dy == 0:
        dx, dy = 0, -TILE_SIZE
def go_down(event):
    global dx, dy
    if dy == 0:
        dx, dy = 0, TILE_SIZE
def go_left(event):
    global dx, dy
    if dx == 0:
        dx, dy = -TILE_SIZE, 0
def go_right(event):
    global dx, dy
    if dx == 0:
        dx, dy = TILE_SIZE, 0

window.bind("<Up>", go_up)
window.bind("<Down>", go_down)
window.bind("<Left>", go_left)
window.bind("<Right>", go_right)

update_title()
draw()
move()
window.mainloop()
