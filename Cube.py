from OpenGL.GL import *
from OpenGL.GLU import *

class Cube(object):
    sides = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
             (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))

    def __init__(self, position, size, color):
        self.position = position
        self.color = color
        x, y, z = map(lambda i: i / 2, size)
        self.vertices = (
            (x, -y, -z), (x, y, -z),
            (-x, y, -z), (-x, -y, -z),
            (x, -y, z), (x, y, z),
            (-x, -y, z), (-x, y, z))

    def render(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glBegin(GL_QUADS)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color)
        for side in Cube.sides:
            for v in side:
                glVertex3fv(self.vertices[v])
        glEnd()
        glPopMatrix()
