import tkinter as tk

# Classe PopupView para criar e gerenciar uma janela pop-up de confirmação usando Tkinter
class PopupView:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Confirmação")

        self.root.geometry("320x100+50+50")

        self.root.overrideredirect(True)

        self.root.wm_attributes("-topmost", True)

        self.root.configure(bg='#222222')

        self.label = tk.Label(

            self.root,

            text="",

            font=("Helvetica", 12, "bold"),

            fg="white",

            bg="#222222",

            justify="center"

        )

        self.label.pack(expand=True, fill='both', padx=10, pady=10)

        self.root.withdraw()

        self.is_visible = False

    # Exibe a janela pop-up com o texto fornecido e torna a interface visível
    def show(self, text):

        self.label.config(text=text)

        if not self.is_visible:

            self.root.deiconify()

            self.is_visible = True

    # Atualiza o texto exibido na janela pop-up, se ela estiver visível
    def update_text(self, text):

        if self.is_visible:

            self.label.config(text=text)

    # Oculta a janela pop-up, se ela estiver visível, e redefine o estado de visibilidade
    def hide(self):

        if self.is_visible:

            self.root.withdraw()

            self.is_visible = False

    # Processa os eventos da interface do Tkinter no loop principal da aplicação
    def update(self):

        if self.root:

            self.root.update_idletasks()

            self.root.update()

    # Destrói a janela e libera os recursos do Tkinter ao encerrar a aplicação
    def destroy(self):

        if self.root:

            self.root.destroy()