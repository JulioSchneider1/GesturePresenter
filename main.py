from controllers.main_controller import MainController

# Executa o aplicativo de controle de apresentação baseado em gestos, iniciando o loop principal do controlador
if __name__ == "__main__":

    print("Iniciando Controlado de Apresentação em Segundo Plano...")

    print("Pressione 'Ctrl + C' no terminal para encerrar.")

    try:

        app = MainController()

        app.run()

    except KeyboardInterrupt:

        print("\nAplicação encerrada com sucesso pelo usuário.")