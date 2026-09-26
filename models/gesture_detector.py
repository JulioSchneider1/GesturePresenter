import os
import cv2
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from collections import deque

# Classe GestureDetector para detectar gestos de mão usando MediaPipe Tasks e OpenCV
class GestureDetector:

    def __init__(self, model_path="hand_landmarker.task"):

        self.model_path = model_path

        # Faz o download do modelo hand_landmarker.task do MediaPipe se não existir localmente
        if not os.path.exists(self.model_path):

            model_url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

            urllib.request.urlretrieve(model_url, self.model_path)

        base_options = python.BaseOptions(model_asset_path=self.model_path)

        options = vision.HandLandmarkerOptions(

            base_options=base_options,

            running_mode=vision.RunningMode.IMAGE,

            num_hands=1,

            min_hand_detection_confidence=0.7,

            min_hand_presence_confidence=0.7,

            min_tracking_confidence=0.7

        )

        self.landmarker = vision.HandLandmarker.create_from_options(options)

        self.x_history = deque(maxlen=10)

    # Processa o frame da câmera e retorna os pontos de referência da mão
    def process_frame(self, frame):

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        results = self.landmarker.detect(mp_image)

        if results.hand_landmarks:

            return results.hand_landmarks

        return None

    # Detecta o movimento de swipe com base no centro da palma e na distância percorrida para evitar disparos acidentais
    def detect_swipe(self, landmarks):

        # Calcula a posição X do centro da palma (média entre o pulso [0] e a base do dedo médio [9])
        palm_center_x = (landmarks[0].x + landmarks[9].x) / 2.0

        self.x_history.append(palm_center_x)

        if len(self.x_history) < 10:

            return None

        delta_x = self.x_history[-1] - self.x_history[0]

        # Requer um movimento mais longo (28% da largura da tela) para confirmar a intenção do usuário
        if delta_x > 0.28:

            self.x_history.clear()

            return "NEXT"

        elif delta_x < -0.28:

            self.x_history.clear()

            return "PREV"

        return None

    # Detecta se o gesto é um "joinha" (polegar para cima) utilizando os pontos de referência da mão
    # Quando o polegar está para cima e os outros dedos estão dobrados, retorna True, caso contrário, retorna False
    def is_thumbs_up(self, landmarks):

        lm = landmarks

        # Verifica se o polegar está para cima comparando a posição do polegar com a posição do dedo indicador
        thumb_up = lm[4].y < lm[2].y

        # Verifica se os outros dedos estão dobrados comparando a posição dos dedos com a posição das articulações correspondentes
        fingers_folded = (

            lm[8].y > lm[6].y and

            lm[12].y > lm[10].y and

            lm[16].y > lm[14].y and

            lm[20].y > lm[18].y

        )

        return thumb_up and fingers_folded