import math
import cv2
import pygame as pg
from OpenGL.GL import *

largura_janela = 800
altura_janela = 600

class Face:

    def __init__(self):
        pg.init()
        pg.display.set_caption("Pygame OpenGL")
        pg.display.set_mode((largura_janela, altura_janela), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        glClearColor(0.1, 0.2, 0.1, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, largura_janela, 0, altura_janela, -1, 1)

        # Inicialize o detector de faces do OpenCV
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.mainLoop()

    def mainLoop(self):

        # Defina o índice da câmera que você deseja usar
        camera_index = 1  # Use 0 para a primeira câmera, 1 para a segunda, etc.

        # Inicialize a captura de vídeo com a câmera especificada
        cap = cv2.VideoCapture(camera_index)

        # Verifique se a câmera foi aberta com sucesso
        if not cap.isOpened():
            print("Não foi possível abrir a câmera.")
        else:
            print(f"Câmera {camera_index} aberta com sucesso.")

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            # Capturar um quadro do feed de vídeo
            ret, frame = cap.read()

            # Detectar faces no quadro
            faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Se uma face for detectada, atualize a posição do círculo com base na posição da face
            if len(faces) > 0:
                x, y, w, h = faces[0]  # Supomos que a primeira face detectada é a principal
                print(f"x: {x}, y: {y}, w: {w}, h: {h}")
                x_centro = x + w // 2
                y_centro = y + h // 2
                #inverte x_centro and y_centro
                x_centro = largura_janela - x_centro
                y_centro = altura_janela - y_centro
            else:
                x_centro = largura_janela // 2
                y_centro = altura_janela // 2

            glClear(GL_COLOR_BUFFER_BIT)
            self.draw_circle(x_centro, y_centro)
            pg.display.flip()
            self.clock.tick(60)
        self.quit()

    def draw_circle(self, x, y):
        raio = 50

        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1.0, 0.0, 0.0)  # Cor vermelha
        glVertex2f(x, y)  # Vértice central

        num_segments = 100  # Número de segmentos para a forma do círculo
        for i in range(num_segments + 1):
            theta = 2.0 * 3.1415926 * float(i) / float(num_segments)
            x_pos = raio * math.cos(theta)
            y_pos = raio * math.sin(theta)
            glVertex2f(x + x_pos, y + y_pos)

        glEnd()

    def quit(self):
        pg.quit()

if __name__ == "__main__":
    myFace = Face()
