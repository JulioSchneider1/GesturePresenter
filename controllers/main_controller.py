import cv2
import time
from models.gesture_detector import GestureDetector
from models.state_manager import StateManager
from views.popup_view import PopupView

# Classe MainController para gerenciar a lógica principal do aplicativo, incluindo captura de vídeo, detecção de gestos e gerenciamento de estado
class MainController:

    def __init__(self):

        self.detector = GestureDetector()

        self.state_mgr = StateManager(timeout_seconds=3.0)

        self.popup = PopupView()

        self.cap = cv2.VideoCapture(0)

    # Executa o loop principal do aplicativo, capturando frames da câmera, processando gestos e gerenciando o estado do sistema
    def run(self):

        try:

            while self.cap.isOpened():

                ret, frame = self.cap.read()

                if not ret:
                    break

                frame = cv2.flip(frame, 1)

                landmarks_list = self.detector.process_frame(frame)

                # Se houver pontos de referência da mão detectados, processa os gestos e gerencia o estado do sistema
                if landmarks_list:

                    landmarks = landmarks_list[0]

                    # Desenha os pontos de referência da mão na imagem para depuração visual
                    h, w, _ = frame.shape

                    for lm in landmarks:

                        cx, cy = int(lm.x * w), int(lm.y * h)

                        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

                    # Se o estado atual for "IDLE", detecta gestos de swipe (NEXT ou PREV) e solicita confirmação, exibindo a janela pop-up
                    if self.state_mgr.state == "IDLE":

                        action = self.detector.detect_swipe(landmarks)

                        if action:

                            self.state_mgr.request_action(action)

                            direction = "Avançar" if action == "NEXT" else "Voltar"

                            self.popup.show(f"Confirmar {direction} slide?\nFaça 👍 (3.0s)")

                    # Se o estado atual for "WAITING_CONFIRMATION", verifica se o gesto é um "joinha" (polegar para cima) e confirma a ação pendente, ocultando a janela pop-up
                    elif self.state_mgr.state == "WAITING_CONFIRMATION":

                        if self.detector.is_thumbs_up(landmarks):

                            self.state_mgr.confirm_action()

                            self.popup.hide()

                            time.sleep(0.5)

                # Verifica se o tempo limite para confirmação expirou e, em caso afirmativo, redefine o estado para IDLE e oculta a janela pop-up
                if self.state_mgr.check_timeout():

                    self.popup.hide()

                # Atualiza o texto exibido na janela pop-up com o tempo restante para confirmação, se o estado estiver aguardando confirmação
                if self.state_mgr.state == "WAITING_CONFIRMATION":

                    rem_time = self.state_mgr.get_remaining_time()

                    direction = "Avançar" if self.state_mgr.pending_action == "NEXT" else "Voltar"

                    self.popup.update_text(f"Confirmar {direction} slide?\nFaça 👍 ({rem_time:.1f}s)")

                # Atualiza a interface do Tkinter na Thread Principal
                self.popup.update()

                # Exibe o frame da câmera em uma janela do OpenCV
                cv2.imshow("Gesture Presenter - Câmera", frame)

                # O loop principal continua até que a tecla 'q' seja pressionada, momento em que os recursos da câmera são liberados e as janelas do OpenCV são fechadas
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    
                    break

        finally:

            self.cleanup()

    # Libera os recursos da câmera, fecha as janelas do OpenCV e destrói a janela pop-up
    def cleanup(self):

        self.cap.release()

        cv2.destroyAllWindows()

        self.popup.destroy()