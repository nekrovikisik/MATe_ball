from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import (sin, cos, pi)


class Coin(object):
    radius = 1
    height = 1
    color = (212 / 255, 175 / 255, 55 / 255, 0)
    speed = 0.01

    def __init__(self, position):
        self.position = position
        self.color = (212 / 255, 175 / 255, 55 / 255)
        self.radius = 1
        self.height = 0.6
        self.quadratic = gluNewQuadric()

    def render2(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ZERO)
        glPushMatrix()
        glTranslatef(*self.position)
        cylinder = gluNewQuadric()
        gluQuadricDrawStyle(cylinder, GLU_FILL)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.color)
        gluCylinder(cylinder, self.radius, self.radius, self.height, 30, 30)
        gluQuadricNormals(cylinder, GLU_SMOOTH)

        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.color)
        gluCylinder(cylinder, self.radius, self.radius, self.height, 40, 40)
        gluDeleteQuadric(cylinder)
        glPopMatrix()

        posx, posy = self.position[0], self.position[1]
        sides = 32
        radius = 1
        glBegin(GL_POLYGON)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.color)
        for i in range(100):
            cosine = radius * cos(i * 2 * pi / sides) + posx
            sine = radius * sin(i * 2 * pi / sides) + posy
            glVertex3f(cosine, sine, self.position[2])
        glEnd()

    def render(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ZERO)
        glPushMatrix()
        glTranslatef(*self.position)
        cylinder = gluNewQuadric()
        gluQuadricDrawStyle(cylinder, GLU_FILL)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.color)
        gluCylinder(cylinder, self.radius, self.radius, self.height, 30, 30)
        gluQuadricNormals(cylinder, GLU_SMOOTH)

        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.color)
        gluCylinder(cylinder, self.radius, self.radius, self.height, 40, 40)
        gluDeleteQuadric(cylinder)
        glPopMatrix()

    def update(self, dt):
        x, y, z = self.position
        z += Coin.speed * dt
        self.position = x, y, z
