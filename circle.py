import math
import pygame as pg
from OpenGL.GL import *

largura_janela = 800
altura_janela = 600

class Circle:

    def __init__(self):

        pg.init()
        pg.display.set_caption("Pygame OpenGL")
        pg.display.set_mode((largura_janela, altura_janela), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        glClearColor(0.1, 0.2, 0.1, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, largura_janela, 0, altura_janela, -1, 1)
        self.mainLoop()

    def mainLoop(self):

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            glClear(GL_COLOR_BUFFER_BIT)
            self.draw_circle()
            pg.display.flip()
            self.clock.tick(60)
        self.quit()

    def draw_circle(self):
        raio = 50
        x_centro = largura_janela // 2
        y_centro = altura_janela // 2

        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1.0, 0.0, 0.0)  # Cor vermelha
        glVertex2f(x_centro, y_centro)  # Vértice central

        num_segments = 100  # Número de segmentos para a forma do círculo
        for i in range(num_segments + 1):
            theta = 2.0 * 3.1415926 * float(i) / float(num_segments)
            x = raio * math.cos(theta)
            y = raio * math.sin(theta)
            glVertex2f(x + x_centro, y + y_centro)

        glEnd()


    
    def quit(self):
        pg.quit()

if __name__ == "__main__":
    myCircle = Circle()