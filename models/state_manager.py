import time
import pyautogui

# Classe StateManager para gerenciar o estado do sistema, incluindo ações pendentes e tempo limite de confirmação
class StateManager:

    def __init__(self, timeout_seconds=3.0):

        self.state = "IDLE"

        self.pending_action = None

        self.confirmation_start_time = 0

        self.timeout_seconds = timeout_seconds

    # Solicita uma ação (NEXT ou PREV) e inicia o estado de espera por confirmação
    def request_action(self, action):

        if self.state == "IDLE":

            self.state = "WAITING_CONFIRMATION"

            self.pending_action = action

            self.confirmation_start_time = time.time()

            return True

        return False

    # Confirma a ação pendente (NEXT ou PREV) se o estado estiver aguardando confirmação
    def confirm_action(self):

        if self.state == "WAITING_CONFIRMATION":

            # Executa a ação pendente (NEXT ou PREV) usando pyautogui para simular a tecla de seta correspondente
            if self.pending_action == "NEXT":

                pyautogui.press('right')

            elif self.pending_action == "PREV":

                pyautogui.press('left')

            self.reset()

            return True

        return False

    # Verifica se o tempo limite para confirmação expirou e, em caso afirmativo, redefine o estado para IDLE
    def check_timeout(self):

        if self.state == "WAITING_CONFIRMATION":

            elapsed = time.time() - self.confirmation_start_time

            if elapsed >= self.timeout_seconds:

                self.reset()

                return True

        return False

    # Retorna o tempo restante para confirmação em segundos, ou 0 se não estiver aguardando confirmação
    def get_remaining_time(self):

        if self.state == "WAITING_CONFIRMATION":

            remaining = self.timeout_seconds - (time.time() - self.confirmation_start_time)

            return max(0.0, remaining)

        return 0.0

    # Redefine o estado para IDLE e limpa a ação pendente e o tempo de início da confirmação
    def reset(self):

        self.state = "IDLE"

        self.pending_action = None

        self.confirmation_start_time = 0