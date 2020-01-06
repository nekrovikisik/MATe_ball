from OpenGL.GL import *
from OpenGL.GLU import *

class Sphere(object):
    slices = 40
    stacks = 40

    def __init__(self, radius, position, color):
        self.radius = radius
        self.position = position
        self.color = color
        self.quadratic = gluNewQuadric()

    def render(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color)
        gluSphere(self.quadratic, self.radius, Sphere.slices, Sphere.stacks)
        glPopMatrix()

