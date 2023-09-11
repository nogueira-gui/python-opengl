import pygame as pg
import cv2

largura_janela = 320
altura_janela = 240

class Face:

    def __init__(self):
        pg.init()
        pg.display.set_caption("Pygame Face")
        self.fullscreen = False
        self.screen = pg.display.set_mode((largura_janela, altura_janela))
        self.clock = pg.time.Clock()

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
        camera_index = 0  # Use 0 para a primeira câmera, 1 para a segunda, etc.

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
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_f:
                    # Alternar entre tela cheia e janela
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.screen = pg.display.set_mode((largura_janela, altura_janela), pg.FULLSCREEN)
                    else:
                        self.screen = pg.display.set_mode((largura_janela, altura_janela))
    

            # Capturar um quadro do feed de vídeo
            ret, frame = cap.read()

            # Detectar faces no quadro
            faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Se uma face for detectada, atualize a posição dos círculos com base na posição da face
            if len(faces) > 0:
                x, y, w, h = faces[0]  # Supomos que a primeira face detectada é a principal
                x_centro = x + w // 2
                y_centro = y + h // 2
                x_centro = largura_janela - x_centro
                y_centro = y_centro - altura_janela 
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

            self.screen.fill((0, 0, 0))  # Preencha o fundo com preto
            color_1 = (255, 255, 255)
            color_2 = (0, 255, 0)
            color_3 = (0, 0, 0)
            
            # Desenhe os círculos usando o Pygame
            self.draw_circle(self.screen, largura_janela // 2 - 65, altura_janela // 2, 60, color_1)
            self.draw_circle(self.screen, self.left_circle_x + largura_janela // 2, self.left_circle_y + altura_janela // 2, self.circle_radius, color_2)
            self.draw_circle(self.screen, largura_janela // 2 + 65, altura_janela // 2, 60, color_1)
            self.draw_circle(self.screen, self.right_circle_x + largura_janela // 2, self.right_circle_y + altura_janela // 2, self.circle_radius, color_2)
            
            pg.display.flip()
            self.clock.tick(60)
        self.quit()

    def draw_circle(self, surface, x, y, raio, color):
        pg.draw.circle(surface, color, (int(x), int(y)), int(raio))

    def quit(self):
        pg.quit()

if __name__ == "__main__":
    myFace = Face()
