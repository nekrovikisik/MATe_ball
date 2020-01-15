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
        glPushMatrix()
        slices = 30
        for i in range(slices):
            theta = (i) * 2.0 * pi
            nextTheta = (i + 1) * 2.0 * pi
            glBegin(GL_TRIANGLE_STRIP)
            glVertex3f(0.0, self.height, 0.0)
            glVertex3f(self.radius * cos(theta), self.height, self.radius * sin(theta))
            glVertex3f (self.radius * cos(nextTheta), self.height, self.radius * sin(nextTheta))
            glVertex3f (self.radius * cos(nextTheta), -self.height, self.radius * sin(nextTheta))
            glVertex3f(self.radius * cos(theta), -self.height, self.radius * sin(theta))
            glVertex3f(0.0, -self.height, 0.0)
            glEnd()


    def render(self):
        #glTranslatef(-0.75, -0.5, 0.0)
        #glRotatef(270.0, 1.0, 0.0, 0.0)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,  [0.2, 1.0, 0.2, 1.0])

        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ZERO)
        glPushMatrix()
        # try:
        glTranslatef(*self.position)
        # glColorMaterial(GL_AMBIENT_AND_DIFFUSE, self.color)
        cylinder = gluNewQuadric()
        gluQuadricDrawStyle(cylinder, GLU_FILL)
        gluQuadricNormals(cylinder, GLU_SMOOTH)

        #glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.color)
        gluCylinder(cylinder, self.radius, self.radius, self.height, 40, 40)
        gluDeleteQuadric(cylinder)
        #glutSwapBuffers()
        glPopMatrix()

    def update(self, dt):
        x, y, z = self.position
        z += Coin.speed * dt
        self.position = x, y, z
        print('Coin ', x, y, z)
