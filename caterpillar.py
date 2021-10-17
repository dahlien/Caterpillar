import pyglet
import random
from pathlib import Path

BODY = 64
BODY_PARTS = Path('tiles')
NORTH = (0, 1)
SOUTH = (0, -1)
WEST = (-1, 0)
EAST = (1, 0)

class State:
    def __init__(self):
        self.body_length = [(0, 0), (1, 0)]
        self.direction = NORTH
        self.snake_alive = True
        self.queued_directions = []
        self.width = 10
        self.height = 10
        self.food = []
        self.add_food()
        self.add_food()

    def move(self):
        if self.queued_directions:
            new_direction = self.queued_directions[0]
            del self.queued_directions[0]
            old_x, old_y = self.direction
            new_x, new_y = new_direction
            if (old_x, old_y) != (-new_x, -new_y):
                self.direction = new_direction

        if not self.snake_alive:
            return

        old_x, old_y = self.body_length[-1]
        dir_x, dir_y = self.direction
        new_x = old_x + dir_x
        new_y = old_y + dir_y

        new_head = new_x, new_y

        if new_x < 0 or new_y < 0 or new_x >= self.width or new_y >= self.height:
            exit('GAME OVER')

        if new_head in self.body_length:
            self.snake_alive = False

        self.body_length.append(new_head)
        if new_head in self.food:
            self.food.remove(new_head)
            self.add_food()
        else:
            del self.body_length[0]

    def add_food(self):
        for try_number in range(100):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            position = x, y
            if (position not in self.body_length) and (position not in self.food):
                self.food.append(position)
                return

window = pyglet.window.Window(width=11*BODY, height=11*BODY)
background = pyglet.image.load('grass_with_border.png')
grass_with_border = pyglet.sprite.Sprite(background)
red_image = pyglet.image.load('apple.png')
snake_tiles = {}
for path in BODY_PARTS.glob('*.png'):
    snake_tiles[path.stem] = pyglet.image.load(path)

state = State()
state.width = window.width // BODY
state.height = window.height // BODY

def on_draw():
    window.clear()
    grass_with_border.draw()

    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    for x, y in state.body_length:
        snake_tiles['tail-head'].blit(x * BODY, y * BODY,
                         width=BODY, height=BODY)
    for x, y in state.food:
        red_image.blit(x * BODY, y * BODY,
                         width=BODY, height=BODY)

def on_key_press(key_code, modifier):
    if key_code == pyglet.window.key.LEFT:
        state.direction = WEST
    if key_code == pyglet.window.key.RIGHT:
        state.direction = EAST
    if key_code == pyglet.window.key.DOWN:
        state.direction = SOUTH
    if key_code == pyglet.window.key.UP:
        state.direction = NORTH

def move(dt):
    state.move()

pyglet.clock.schedule_interval(move, 1/6)

window.push_handlers(on_draw, on_key_press)

pyglet.app.run()
