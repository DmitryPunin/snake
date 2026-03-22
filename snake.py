from tkinter import *
from tkinter import ttk
import time
import random



class game:
    def __init__(self,cells_x,cells_y):
        self.field = [['' for _ in range(cells_y)] for _ in range(cells_x)]
        self.snake = snake((cells_x//2,cells_y//2))
        self.direction = 'up'
        self.snake_direction = 'up'
        self.has_fruit = False
        self.pos_fruit = None
        self.stopped = False
        self.showing_start_menu = True
        self.color = None
        self.won = False


    def update(self):

        if not self.stopped:

            self.snake.move(self.direction)
            self.snake_direction = self.direction
            head = self.snake.head
            if head[1] < 0 or head[1] >= cells_y or head[0] < 0 or head[0] >= cells_x or self.snake.head_in_body():
                self.stopped = True
                self.field = [['' for _ in range(cells_y)] for _ in range(cells_x)]
                return
            snake_point = self.field[head[0]][head[1]]
            if snake_point == '.':
                self.field[head[0]][head[1]] = ''
                self.snake.grow()
                self.has_fruit = False
                self.pos_fruit = None
            elif snake_point == ',':
                self.field[head[0]][head[1]] = ''
                for _ in range(3):
                    self.snake.grow()
                self.has_fruit = False
                self.pos_fruit = None
            if not self.has_fruit:
                self.spawn_fruit()
        else:
            pass


    def spawn_fruit(self):
        x = random.randint(0,cells_x-1)
        y = random.randint(0,cells_y-1)
        if random.randint(1, 6) == 1:
            self.field[x][y] = ','
        else:
            self.field[x][y] = '.'
            self.color = random.choice(['red', 'green', 'blue'])
        self.has_fruit = True
        self.pos_fruit = (x, y)




class snake:
    def __init__(self,start_point):
        self.head = start_point
        self.body = [(start_point[0],start_point[1]+1)]
    def head_in_body(self):
        for b in self.body:
            if b == self.head:
                return True
        return False
    def grow(self):
        last = self.body[-1]
        if len(self.body) > 1 :
            prev_last = self.body[-2]
        else:
            prev_last = self.head
        x_diff = last[0] - prev_last[0]
        y_diff = last[1] - prev_last[1]
        x = x_diff + last[0]
        y = y_diff - last[1]
        self.body.append((x,y))
    def move(self,direction):
        speed = [0,0]
        if direction == 'down':
            speed[1] = 1
        elif direction =='up':
            speed[1] = -1
        elif direction == 'left':
            speed[0] = -1
        elif direction == 'right':
            speed[0] = 1
        prev_pos = self.head
        self.head = (self.head[0] + speed[0], self.head[1] + speed[1])
        if speed[0] != 0 or speed[1] != 0:
            for i in range(len(self.body)):
                b = self.body[i]
                self.body[i] = prev_pos
                prev_pos = b










width = 500
height = 500
W = Tk()
W.geometry('800x800')
style = ttk.Style()
style.theme_use('alt')
style.configure('red.TButton',background='red',foreground='WHITE')
style.map('red.TButton',background=[('pressed','#FB000D'),('active','#FB000D')])

style.configure('orange.TButton',background='orange',foreground='WHITE')
style.map('orange.TButton',background=[('pressed','orange'),('active','orange')])

style.configure('green.TButton',background='green',foreground='WHITE')
style.map('green.TButton',background=[('pressed','green'),('active','green')])
c = Canvas(bg='white',width=width,height=height)
c.pack(anchor=CENTER,expand=1)
def show_start_menu():
    c.delete('all')
    c.create_text(width / 2, height / 2, text='Выберите уровень сложности, чтобы начать игру.', font='Arial 15',
                  fill='black')
    g.field = [['' for _ in range(cells_y)] for _ in range(cells_x)]
def show_start_menu_againt(e):
    show_start_menu()


def init():
    global g, cells_x, pad_x, cells_y, pad_y,game_elements
    c.delete('all')
    c.bind('a', move_left)
    c.bind('w', move_up)
    c.bind('s', move_down)
    c.bind('d', move_right)
    c.focus_set()
    game_elements = []
    cells_x = (width // size) + 1
    pad_x = width / cells_x
    for i in range(cells_x):
        c.create_line(i * pad_x, 0, i * pad_x, height, width=1)
    cells_y = (height // size) + 1
    pad_y = height / cells_y
    for i in range(cells_y):
        c.create_line(0, i * pad_y, width, i * pad_y, width=1)
    g = game(cells_x, cells_y)
    g.stopped = False
    g.showing_start_menu = False
    for id in after_ids:
        W.after_cancel(id)
    after_ids.clear()
    update()

def easy_lvl():
    global size,update_ms

    size = 50
    update_ms = 650
    init()

def middle_lvl():
    global size, update_ms
    size = 35
    update_ms = 500
    init()
def hard_lvl():
    global size, update_ms
    size = 25
    update_ms = 200
    init()


easy_button = ttk.Button(text='Легко',command=easy_lvl,style='green.TButton')
easy_button.place(x=150,y=75,width=100)

middle_button = ttk.Button(text='Средний',command=middle_lvl,style='orange.TButton')
middle_button.place(x=350,y=75,width=100)

hard_button = ttk.Button(text='Сложно',command=hard_lvl,style='red.TButton')
hard_button.place(x=550,y=75,width=100)

update_ms = 1000
size = 20
cells_x = (width // size) + 1
pad_x = width / cells_x
for i in range(cells_x):
    c.create_line(i * pad_x, 0, i * pad_x, height, width=1)
cells_y = (height // size) + 1
pad_y = height / cells_y
for i in range(cells_y):
    c.create_line(0, i * pad_y, width, i * pad_y, width=1)
g = game(cells_x, cells_y)
after_ids = []
game_elements = []
def update():
    global g, cells_x, pad_x, cells_y, pad_y,game_elements
    for element in game_elements:
        c.delete(element)
    game_elements.clear()
    for i in range (cells_x):
        for j in range(cells_y):
            if g.field [i] [j] == '.':
                dot = c.create_oval(i * pad_x, j * pad_y, (i + 1) * pad_x, (j + 1) * pad_y, fill=g.color)
                game_elements.append(dot)
            elif g.field[i][j] == ',':
                rainbow_color = random.choice(['red', 'green', 'blue', 'yellow','orange','purple'])
                dot = c.create_oval(i * pad_x, j * pad_y, (i + 1) * pad_x, (j + 1) * pad_y,fill=rainbow_color)
                game_elements.append(dot)
    if g.stopped == False:
        ul = [g.snake.head[0] * pad_x, g.snake.head[1] * pad_y]
        dr = [(g.snake.head[0]+1) * pad_x, (g.snake.head[1]+1) * pad_y]
        if g.snake_direction == 'up' or g.snake_direction == 'down':
            ul[0] += 5
            dr[0] -= 5
        elif g.snake_direction == 'left' or g.snake_direction == 'right':
            ul[1] += 5
            dr[1] -= 5
        snake_head = c.create_oval(*ul,*dr,fill='#3BDA00')
        game_elements.append(snake_head)

        h_c = [(ul[0]+dr[0])/2,(ul[1]+dr[1])/2]
        speed = [0, 0]



        if g.snake_direction == 'down':
            speed[1] = size / 5
        elif g.snake_direction == 'up':
            speed[1] = -size / 5
        elif g.snake_direction == 'left':
            speed[0] = -size / 5
        elif g.snake_direction == 'right':
            speed[0] = size / 5
        snake_eye1 = c.create_oval(h_c[0]+speed[0]-size/10,h_c[1] + speed[1] - size/10,h_c[0]+speed[0]+size/10,h_c[1] + speed[1] + size/10,fill='black')
        game_elements.append(snake_eye1)
        for b in g.snake.body:
            ul = [b[0] * pad_x, b[1] * pad_y]
            dr = [(b[0] + 1) * pad_x, (b[1] + 1) * pad_y]
            snake_body = c.create_oval(*ul,*dr,fill='#269926')
            game_elements.append(snake_body)
        g.update()
        id= W.after(update_ms, update)
        after_ids.append(id)


    else:
            c.delete('all')
            c.create_text(width / 2, height / 2 - size * 3, text='Вы проиграли!', font='Arial 40', fill='black')
            c.create_text(width / 2, height / 2, text=f'Ваш счет:{len(g.snake.body)}', font='Arial 40', fill='black')
            c.create_text(width/2,height/2+size*3,text='Нажмите Q для выхода',font='Arial 20',fill='black')
            g.field = [['' for _ in range(cells_y)] for _ in range(cells_x)]

    if g.showing_start_menu == True:
        show_start_menu()



update()




def move_up(e):
    if g.snake_direction != 'down':
        g.direction = 'up'
def move_left(e):
    if g.snake_direction != 'right':
        g.direction = 'left'
def move_down(e):
    if g.snake_direction != 'up':
        g.direction = 'down'
def move_right(e):
    if g.snake_direction !='left':
        g.direction = 'right'

c.bind('a',move_left)
c.bind('w',move_up)
c.bind('s',move_down)
c.bind('d',move_right)
c.bind('q',show_start_menu_againt)
c.focus_set()
if g.won == True:
    c.create_text(width/2,height/2-size*4,text='Вы победили!',font='Arial 40',fill='black')
    c.create_text(width/2,height/2,text=f'Ваш счет:{len(g.snake.body)}',font='Arial 40',fill='black')
    g.field = [['' for _ in range(cells_y)] for _ in range(cells_x)]
    c.delete('all')
if len(g.snake.body) == cells_x * cells_y:
    g.won = True


W.mainloop()
