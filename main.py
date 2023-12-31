import pygame as pg
from triangle import Triangle
from circle import Circle
from OpenGL.GL import *

largura_janela = 800
altura_janela = 600

class App:

    def __init__(self):
        pg.init()
        pg.display.set_caption("Pygame OpenGL")
        pg.display.set_mode((largura_janela, altura_janela), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        glClearColor(0.1, 0.2, 0.1, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, largura_janela, 0, altura_janela, -1, 1)
        self.circle = Circle()
        self.triangle = Triangle()  # Crie uma instância de Triangle
        self.mainLoop()

    def mainLoop(self):

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            glClear(GL_COLOR_BUFFER_BIT)
            self.draw()
            pg.display.flip()
            self.clock.tick(60)
        self.quit()
        
    def quit(self):
        pg.quit()

    def draw(self):
        # Desenhe o triângulo chamando o método draw_triangle()
        self.triangle.draw_triangle()

        # Desenhe o círculo chamando o método draw_circle()
        # self.circle.draw_circle()

if __name__ == "__main__":
    myApp = App()
