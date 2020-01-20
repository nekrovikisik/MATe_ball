import os, sys
from OpenGL.GL import *
from OpenGL.GLU import *

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)
from Cube import Cube

class Block(Cube):

    #color = (100 / 255, 153 / 255, 153 / 255, 0)
    color = (100 / 255, 153 / 255, 153 / 255, 0)
    speed = 0.01

    def __init__(self, position, size):
        super().__init__(position, (size, 1, 1), Block.color)
        self.size = size

    def update(self, dt):
        x, y, z = self.position
        z += Block.speed * dt
        self.position = x, y, z
