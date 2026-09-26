# GesturePresenter - Controle de Apresentações por Gestos

O GesturePresenter é uma aplicação Python desenvolvida sob o padrão arquitetural MVC (Model-View-Controller) que permite controlar apresentações de slides (PowerPoint, Google Slides, PDFs) utilizando gestos manuais capturados pela câmera do computador.

O sistema utiliza OpenCV para captura do feed de vídeo e a API MediaPipe Tasks para detecção precisa dos pontos de referência da mão (landmarking). Para evitar trocas acidentais de slides, o sistema conta com uma janela de confirmação flutuante (Always-on-Top) que exige um gesto de "Joinha" (👍) dentro de um limite de tempo de 3 segundos para efetivar o comando.

## Pré-requisitos e Instalação

### Pré-requisitos:
<ul>
  <li> Python 3.9 ou superior. </li>
  <li> WebCam conectada ao computador. </li>
</ul>

### Instalação
<details>
<summary><b>1. Clonar o Repositório</b></summary>

```bash
git clone https://github.com/JulioSchneider1/GesturePresenter.git
cd GesturePresenter
```
</details>

<details>
<summary><b>2. Crie e ative um ambiente virtual (recomendado)</b></summary>

```bash
Windows:
python -m venv .venv
.\.venv\Scripts\activate

Linux:
python3 -m venv .venv
source .venv/bin/activate
```
</details>

<details>
<summary><b>3. Instale as Dependências</b></summary>

```bash
pip install -r requirements.txt
```
</details>

## Como Executar

<ol>
  <li>Abra sua apresentação em tela cheia (PowerPoint, Google Slides, Leitor de PDF, etc.)</li>
  <li>Execute o script principal no terminal

  ```bash
  python main.py
  ```
  </li>
  <li>O aplicativo abrirá uma janela de vídeo exibindo a câmera com a sobreposição dos pontos da mão para depuração visual</li>
</ol>

## Como Usar

<ol>
  <li>
    <p>Iniciando um comando</p>
    <ul>
      <li>Faça um movimento firme com a mão na vertical em frente à câmera.</li>
      <li>Movimento para a Direita ➡️ solicita avançar o slide.</li>
      <li>Movimento para a Esquerda ⬅️ solicita voltar o slide.</li>
    </ul>
  </li>
  <li>
    <p>Confirmando a ação</p>
    <ul>
      <li>Assim que o movimento for reconhecido, uma pequena janela escura surgirá no canto superior esquerdo da tela com o tempo restante (ex: Confirmar Avançar slide? Faça 👍 (2.8s)).</li>
      <li>Faça o gesto de "Joinha" (👍) em frente à câmera dentro de 3 segundos.</li>
      <li>O slide mudará automaticamente assim que a confirmação for detectada.</li>
    </ul>
  </li>
  <li>
    <p>Cancelando ou ignorando</p>
    <ul>
      <li>Se você não fizer o gesto de "Joinha", a solicitação expira após 3 segundos, o popup fecha e o slide não é alterado.</li>
    </ul>
  </li>
  <li>
    <p>Encerrando a aplicação</p>
    <ul>
      <li>Pressione a tecla "q" com a janela da câmera selecionada, ou pressione "Ctrl + C" no terminal.</li>
    </ul>
  </li>
</ol>

## Tecnologias Utilizadas
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-2A2A2A?style=for-the-badge&logo=python&logoColor=white)](https://pyautogui.readthedocs.io/)
[![Tkinter](https://img.shields.io/badge/Tkinter-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/library/tkinter.html)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe Tasks](https://img.shields.io/badge/MediaPipe-00979D?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/edge/mediapipe/solutions/guide)
