import math
import cv2
import pygame as pg
from OpenGL.GL import *

largura_janela = 320
altura_janela = 240

class Face:

    def __init__(self):
        pg.init()
        pg.display.set_caption("Pygame OpenGL")
        pg.display.set_mode((largura_janela, altura_janela), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-largura_janela/2, largura_janela/2, -altura_janela/2, altura_janela/2, -1, 1)  # Defina o ponto de origem no centro

        # Inicialize o detector de faces do OpenCV
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Posições iniciais dos círculos
        self.eyes_distances = 65
        self.left_circle_x = -self.eyes_distances
        self.left_circle_y = 0
        self.right_circle_x = self.eyes_distances
        self.right_circle_y = 0
        self.circle_radius = 23.33  # Raio dos círculos menores

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

            # Se uma face for detectada, atualize a posição dos círculos com base na posição da face
            if len(faces) > 0:
                x, y, w, h = faces[0]  # Supomos que a primeira face detectada é a principal
                # print(f"x: {x}, y: {y}, w: {w}, h: {h}")
                x_centro = x + w // 2
                y_centro = y + h // 2
                # Inverte x_centro e y_centro
                x_centro = largura_janela - x_centro
                y_centro = altura_janela - y_centro
                # print(f"x_camera: {x} y_camera: {y} | x_centro: {x_centro}, y_centro: {y_centro}")
            else:
                x_centro = 0
                y_centro = 0

            # Interpolação suave das posições dos círculos
            smoothing_factor = 0.1
            self.left_circle_x = (1 - smoothing_factor) * self.left_circle_x + smoothing_factor * (x_centro - self.eyes_distances)
            self.left_circle_y = (1 - smoothing_factor) * self.left_circle_y + smoothing_factor * y_centro
            self.right_circle_x = (1 - smoothing_factor) * self.right_circle_x + smoothing_factor * (x_centro + self.eyes_distances)
            self.right_circle_y = (1 - smoothing_factor) * self.right_circle_y + smoothing_factor * y_centro

            #verifica se left_circle_x e right_circle_x estão fora do limite dos olhos
            print(f"left_circle_x: {self.left_circle_x} right_circle_x: {self.right_circle_x}")
            if (self.left_circle_x < -90):
                self.left_circle_x = -90
            if (self.right_circle_x < 35):
                self.right_circle_x = 35
            if (self.left_circle_x > -35):
                self.left_circle_x = -35
            if (self.right_circle_x > 95):
                self.right_circle_x = 95

            if (self.left_circle_y > 28):
                self.left_circle_y = 28
            if (self.right_circle_y > 28):
                self.right_circle_y = 28
            if (self.left_circle_y < -28):
                self.left_circle_y = -28
            if (self.right_circle_y < -28):
                self.right_circle_y = -28

            glClear(GL_COLOR_BUFFER_BIT)
            color_1 = [1.0, 1.0, 1.0]
            color_2 = [0, 1.0, 0]
            color_3 = [0, 0, 0]
            # Left eye
            self.draw_circle(-65, 0, 60, color_1)
            self.draw_circle(self.left_circle_x, self.left_circle_y, self.circle_radius, color_2)  # Círculo segue o rosto
            self.draw_circle(self.left_circle_x, self.left_circle_y, self.circle_radius / 3, color_3)  # Círculo segue o rosto
            # Right eye
            self.draw_circle(65, 0, 60, color_1)
            self.draw_circle(self.right_circle_x, self.right_circle_y, self.circle_radius, color_2)  # Círculo segue o rosto
            self.draw_circle(self.right_circle_x, self.right_circle_y, self.circle_radius / 3, color_3)  # Círculo segue o rosto
            pg.display.flip()
            self.clock.tick(60)
        self.quit()

    def draw_circle(self, x, y, raio, color):

        glBegin(GL_TRIANGLE_FAN)
        glColor3f(color[0], color[1], color[2])
        glVertex2f(x, y)

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
