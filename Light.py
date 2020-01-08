from OpenGL.GL import *
from OpenGL.GLU import *


class Light(object):
    # описывает ИСТОЧНИК света
    enabled = False
    colors = [(1., 1., 1., 1.),
              (1., 0.5, 0.5, 1.),
              (0.5, 1., 0.5, 1.),
              (0.5, 0.5, 1., 1.)]

    def __init__(self, light_id, position):
        self.light_id = light_id
        self.position = position
        self.current_color = 0

    def render(self):
        light_id = self.light_id
        color = Light.colors[self.current_color]

        # координаты местоположения лампы
        glLightfv(light_id, GL_POSITION, self.position)
        glLightfv(light_id, GL_DIFFUSE, color)  # рассеянный свет, далее задается его параметры рассеивания
        glLightfv(light_id, GL_CONSTANT_ATTENUATION, 0.1)  # интенсивность константа
        glLightfv(light_id, GL_LINEAR_ATTENUATION, 0.05)  # интенсивность линейный множитель

    def switch_color(self):
        self.current_color += 1
        self.current_color %= len(Light.colors)

    def enable(self):  # включение источника
        if not Light.enabled:
            glEnable(GL_LIGHTING)
            Light.enabled = True
        glEnable(self.light_id)
