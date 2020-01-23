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
from Coin import Coin
from OpenGL.GL import *
from OpenGL.GLU import *


class App(object):
    def __init__(self, width=800, height=600):
        self.title = 'My first OpenGL game'
        self.start_clicked = False
        self.fps = 60
        self.width = width
        self.height = height
        self.set_startValues()

    def set_startValues(self):
        self.random_dt = 0
        self.random_dt_coin = 0
        self.blocks = []
        self.coins = []
        self.light = Light(GL_LIGHT0, (0, 15, -25, 1))
        self.player = Sphere(1, position=(0, 0, 0),
                             color=(255 / 255, 20 / 255, 147 / 255, 0))
        self.ground = Cube(position=(0, -1, -20),
                           size=(16, 1, 60),
                           color=(253 / 255, 222 / 255, 238 / 255, 1))

    def start(self):
        pygame.init()
        self.pygame_init()
        self.main_loop()

    def pygame_init(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.draw_menu()

    def openGL_init(self):
        self.score = -1
        self.wallet = []
        print(self.start_clicked)
        self.start_clicked = True
        pygame.display.set_mode((self.width, self.height), OPENGL | DOUBLEBUF)
        pygame.display.set_caption(self.title)
        self.set_startValues()
        self.light.enable()
        glEnable(GL_DEPTH_TEST)
        glClearColor(.1, .1, .1, 1)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, self.width / self.height, 1, 100)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_CULL_FACE)
        print('im init opengl')

    def main_loop(self):
        self.clock = pygame.time.Clock()
        self.isJump = False  # прыгает ли игрок
        self.jumpCount = 4
        self.y0 = self.player.position[1]
        self.fly = 0
        self.draw_menu()
        while True:
            for event in pygame.event.get():
                if not self.start_clicked and event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    self.onClick(mouse_position)
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == 13: # если нажали на enter
                    self.start_game()

            if self.start_clicked:
                #print('display!!')
                self.display()
                dt = self.clock.tick(self.fps)
                for block in self.blocks:
                    block.update(dt)
                for coin in self.coins:
                    coin[0].update(dt)
                self.clear_past_blocks()
                self.add_random_block(dt)
                self.clear_past_coins()
                self.add_random_coin(dt)
                self.check_collisions()
                self.process_input(dt)
    def start_game(self):
        print('opengl init')
        self.score = -1
        self.wallet = []
        self.start_clicked = True
        self.openGL_init()

    def draw_menu(self):
        try:
            score = self.score
        except:
            score = -1
        print('hello i draw menu')
        font = pygame.font.Font(None, 72)
        logo = font.render("MATe_ball!", 1, (100, 255, 100))
        self.screen.blit(logo, (self.width // 2 - 120, 50))
        text = font.render("Play!", 1, (100, 255, 100))

        if score > -3:
            textScore = font.render(f"score: {score}", 1, (100, 255, 100))
            textScore_x = self.width // 2 - 100
            textScore_y = self.height // 2 - text.get_height() // 2 - 100
            self.screen.blit(textScore, (textScore_x, textScore_y))
            text_y = self.height // 2 - text.get_height() // 2
        else:
            text_y = self.height // 2 + text.get_height() // 2
        text_x = self.width // 2 - text.get_width() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        pygame.draw.rect(self.screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                    text_w + 20, text_h + 20), 1)
        self.buttons = {'play': [text_x - 10, text_y - 10, text_w + 20, text_h + 20]}
        self.screen.blit(text, (text_x, text_y))
        pygame.display.flip()

    def onClick(self, mousePos):
        mousePos_X = mousePos[0]
        mousePos_Y = mousePos[1]
        try:
            for key in self.buttons.keys():
                cords = self.buttons[key]
                # если нажали на кнопку
                if (mousePos_X > cords[0]) and (mousePos_X < cords[0] + cords[2]) and \
                        (mousePos_Y > cords[1]) and (mousePos_Y < cords[1] + cords[3]):
                    if key == 'play':
                        print('click')
                        self.start_game()
        except:
            print('click "play" ')

    def check_collisions(self):  # проиграл или собрал монетку
        blocks = filter(lambda x: 0 < x.position[2] < 1,
                        self.blocks)
        coins = filter(lambda x: 0 < x[0].position[2] < 1,
                       self.coins)
        x = self.player.position[0]
        y = self.player.position[1]
        r = self.player.radius
        for block in blocks:
            x1 = block.position[0]
            y1 = block.position[1]
            s = block.size / 2
            is_left = x1 - s < x - r < x1 + s  # левая половинка задела
            is_right = x1 - s < x + r < x1 + s  # правая половинка задела
            is_upper = y1 < y
            if (is_left or is_right) and not is_upper:
                print("Game over!")
                self.start_clicked = False
                self.pygame_init()
        for coin in coins:
            x1 = coin[0].position[0]
            y1 = coin[0].position[1]
            z1 = coin[0].position[1]
            hash = coin[1]
            if abs(x - x1) < 5 and abs(y - y1) < 5:
                self.wallet.append((x1, y1, z1, hash) )
                print(x1, y1, z1, hash)
                #print(self.wallet)
                self.score = len(set(self.wallet))
                print(self.score)

    def add_random_block(self, dt):
        self.random_dt += dt
        if self.random_dt >= 800:
            r = random.random()
            if r < 0.1:
                self.random_dt = 0
                self.generate_block(r)

    def add_random_coin(self, dt):
        self.random_dt_coin += dt
        if self.random_dt_coin >= 800:
            r = random.random()
            if r < 0.05:
                self.random_dt_coin = 0
                self.generate_coin()

    def generate_block(self, r):
        size = 7 if r < 0.03 else 5
        offset = random.choice([-4, 0, 4])
        self.blocks.append(Block((offset, 0, -40), size))

    def generate_coin(self):
        offset = random.choice(range(-4, 5, 1))
        x, y, z = (offset, 0, -40)
        if not self.blocks:  # если блоков нет, генерим монету
            self.coins.append([Coin((x, y, z)),  random.random()])
            return                #print(self.wallet)

        lastBlock_X = self.blocks[-1].position[0]
        lastBlock_Y = self.blocks[-1].position[1]
        # если монетка где-то около блока, ее не будет
        if (lastBlock_X - 4 <= x <= lastBlock_X + 4):
            self.coins.append([Coin((lastBlock_X, y + 2.5, z)), random.random()])
        else:
            self.coins.append([Coin((x, y, z)), random.random()])

    def clear_past_blocks(self):
        blocks = filter(lambda x: x.position[2] > 5,
                        self.blocks)
        for block in blocks:
            self.blocks.remove(block)
            del block

    def clear_past_coins(self):
        coin0 = [coin[0] for coin in self.coins]
        coins = filter(lambda x: x[0].position[2] > 5,
                       self.coins)
        for coins in coins:
            self.coins.remove(coins)
            del coins

    def draw(self, my_text='MATe_ball', cords=[], color=(100, 255, 100)):
        font = pygame.font.Font(None, 50)
        text = font.render(my_text, 1, color)
        text_x, text_y = cords
        text_w = text.get_width()
        text_h = text.get_height()
        # screen.blit(text, (text_x, text_y))
        pygame.draw.rect(self.screen, color, (text_x - 10, text_y - 10,
                                              text_w + 20, text_h + 20), 1)

    def drawText(self, position, textString):
        font = pygame.font.Font(None, 64)
        textSurface = font.render(textString, True, (255, 255, 255, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glRasterPos3d(*position)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 10, 10,
                  0, 0, -5,
                  0, 1, 0)
        self.light.render()
        for block in self.blocks:
            block.render()
        for coin in self.coins:
            coin[0].render2()
        self.player.render()
        self.ground.render()
        pygame.display.flip()

    def process_input(self, dt):
        pressed = pygame.key.get_pressed()
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
        if pressed[K_SPACE] or self.isJump:
            if self.jumpCount > -4:
                self.isJump = True
                y += self.jumpCount * abs(self.jumpCount) / 10
                y = round(y, 2)
                self.jumpCount -= 0.5
            elif self.jumpCount < -4:
                self.jumpCount = 4
                self.isJump = False
                y = self.y0
            elif self.jumpCount == -4:
                self.fly += 1
                self.isJump = True
                if self.fly > 7:
                    self.fly = 0
                    self.jumpCount = -5
        self.player.position = (x, y, z)


if __name__ == '__main__':
    app = App()
    app.start()
