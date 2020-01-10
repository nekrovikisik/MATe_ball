import os, sys
import pygame
from pygame.locals import *
import random
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)
from Light import Light
from Sphere import Sphere
from Cube import Cube
from Block import Block
from OpenGL.GL import *
from OpenGL.GLU import *


class App(object):
    def __init__(self, width=800, height=600):
        self.title = 'My first OpenGL game'
        self.fps = 60
        self.width = width
        self.height = height
        self.game_over = False
        self.random_dt = 0
        self.blocks = []
        self.light = Light(GL_LIGHT0, (0, 15, -25, 1))
        self.player = Sphere(1, position=(0, 0, 0),
                             color=(255/255, 20/255, 147/255, 0))
        self.ground = Cube(position=(0, -1, -20),
                           size=(16, 1, 60),
                           color=(253/255, 222/255, 238/255, 1))

    def start(self):
        pygame.init()
        pygame.display.set_mode((self.width, self.height),
                                OPENGL | DOUBLEBUF)
        pygame.display.set_caption(self.title)
        self.light.enable()
        glEnable(GL_DEPTH_TEST)
        glClearColor(.1, .1, .1, 1)
        glMatrixMode(GL_PROJECTION)
        aspect = self.width / self.height
        gluPerspective(45, aspect, 1, 100)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_CULL_FACE)
        self.main_loop()

    def main_loop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if not self.game_over:
                self.display()
                dt = clock.tick(self.fps)
                for block in self.blocks:
                    block.update(dt)
                self.clear_past_blocks()
                self.add_random_block(dt)
                self.check_collisions()
                self.process_input(dt)
                print(self.player.position)

    def check_collisions(self): # проиграл ли
        blocks = filter(lambda x: 0 < x.position[2] < 1,
                        self.blocks)
        x = self.player.position[0]
        y = self.player.position[1]
        r = self.player.radius
        for block in blocks:
            x1 = block.position[0]
            y1 = block.position[1]
            s = block.size / 2
            is_left = x1 - s < x - r < x1 + s # левая половинка задела
            is_right = x1 - s < x + r < x1 + s # правая половинка задела
            is_upper = y1 < y
            if (is_left or is_right) and not is_upper:
                print(is_upper)
                print(y1)
                self.game_over = True
                print("Game over!")

    def add_random_block(self, dt):
        self.random_dt += dt
        if self.random_dt >= 800:
            r = random.random()
            if r < 0.1:
                self.random_dt = 0
                self.generate_block(r)

    def generate_block(self, r):
        size = 7 if r < 0.03 else 5
        offset = random.choice([-4, 0, 4])
        self.blocks.append(Block((offset, 0, -40), size))

    def clear_past_blocks(self):
        blocks = filter(lambda x: x.position[2] > 5,
                        self.blocks)
        for block in blocks:
            self.blocks.remove(block)
            del block

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 10, 10,
                  0, 0, -5,
                  0, 1, 0)
        self.light.render()
        for block in self.blocks:
            block.render()
        self.player.render()
        self.ground.render()
        pygame.display.flip()

    def process_input(self, dt):
        pressed = pygame.key.get_pressed()
        pressed = pygame.key.get_focused()
        x, y, z = self.player.position
        if pressed[K_LEFT]:
            x -= 0.01 * dt
            x = max(min(x, 7), -7)
        if pressed[K_RIGHT]:
            x += 0.01 * dt
            x = max(min(x, 7), -7)
        if pressed[K_RIGHT]:
            x += 0.01 * dt
            x = max(min(x, 7), -7)
        if pressed[K_SPACE]:
            y0 = y
            y += 0.01 * dt
            y = max(min(y, 7), -7)
            y = y0
        self.player.position = (x, y, z)


if __name__ == '__main__':
    app = App()
    app.start()
