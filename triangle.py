import math
import pygame as pg
from OpenGL.GL import *

class Triangle:

    # Equilateral triangle points
    points = [
        {
            'x': -0.25,
            'y': 0.1445,
            'color': [1.0, 0.0, 0.0]
        },
        {
            'x': 0.25,
            'y': 0.1445,
            'color': [0.0, 1.0, 0.0]
        },
        {
            'x': 0.0,
            'y': -0.2885,
            'color': [0.0, 0.0, 1.0]
        }
    ]

    def __init__(self):
        self.is_valid_triangle(self.points)

        pg.init()
        pg.display.set_caption("Pygame OpenGL")
        pg.display.set_mode((800, 600), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        glClearColor(0.1, 0.2, 0.1, 1.0)
        self.mainLoop()

    def mainLoop(self):

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            glClear(GL_COLOR_BUFFER_BIT)
            self.draw_triangle(0, 0, 0) #triangulo equilatero normal
            self.draw_triangle(0.50, 0.30, 0) #triangulo transladado
            self.draw_triangle(0.50, -0.40, 90.0) #triangulo rotacionado
            pg.display.flip()
            self.clock.tick(60)
        self.quit()

    def draw_triangle(self, dx, dy, r):
        center_x = 0.0 + dx #coordenada x do centro de rotação
        center_y = 0.0 + dy #coordenada y do centro de rotação

        glBegin(GL_TRIANGLES)
        for point in self.points:
            point_x = point['x'] + dx
            point_y = point['y'] + dy

            # Calcula as coordenadas em relação ao centro de rotação
            x_from_center = point_x - center_x
            y_from_center = point_y - center_y

            # Aplica a rotação manualmente
            x_rotated = x_from_center * math.cos(math.radians(r)) - y_from_center * math.sin(math.radians(r))
            y_rotated = x_from_center * math.sin(math.radians(r)) + y_from_center * math.cos(math.radians(r))

            # Adiciona as coordenadas do centro de rotação de volta
            x_rotated += center_x
            y_rotated += center_y

            glVertex2f(x_rotated, y_rotated)
            glColor3f(point['color'][0], point['color'][1], point['color'][2])
        glEnd()

    def is_valid_triangle(self, points):
        vertice_ab = round(self.calculate_distance(points[0], points[1]), 3)
        vertice_bc = round(self.calculate_distance(points[1], points[2]), 3)
        vertice_ca = round(self.calculate_distance(points[2], points[0]), 3)
        print(f'vertice_ab: {vertice_ab}')
        print(f'vertice_bc: {vertice_bc}')
        print(f'vertice_ca: {vertice_ca}')

        if vertice_ab + vertice_bc <= vertice_ca:
            print("Invalid triangle")
            self.quit()
        if vertice_ab == vertice_bc == vertice_ca:
            print("Equilateral triangle")
        elif vertice_ab == vertice_bc or vertice_bc == vertice_ca or vertice_ca == vertice_ab:
            print("Isosceles triangle")
        else:
            print("Scalene triangle")

    def calculate_distance(self, point_1, point_2):
        return ((point_1['x'] - point_2['x']) ** 2 + (point_1['y'] - point_2['y']) ** 2) ** 0.5

    def quit(self):
        pg.quit()

if __name__ == "__main__":
    myTriangle = Triangle()