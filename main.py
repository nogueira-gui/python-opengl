import pygame as pg
from OpenGL.GL import *

class App:

    points = [
        {
            'x': 0,
            'y': 0.5,
            'color': [1.0, 0.0, 0.0]
        },
        {
            'x': -0.433,
            'y': -0.25,
            'color': [0.0, 1.0, 0.0]
        },
        {
            'x': 0.433,
            'y': -0.25,
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
            self.draw_triangle()
            pg.display.flip()
            self.clock.tick(60)
        self.quit()

    def draw_triangle(self):
        glBegin(GL_TRIANGLES)
        for point in self.points:
            glVertex2f(point['x'], point['y'])
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
    myApp = App()