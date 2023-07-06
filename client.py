import json
import socket
import threading
import time
import pygame.event
import game
from ImageLabel import ImageLabel
from constants import SERVER_IP, SERVER_PORT, LOADING_IMG, WHITE_CONTROLS, BLACK_CONTROLS
import chatlib
import tkinter as tk
from tkinter import messagebox
import ipaddress
import os


pygame.mixer.init()
espera = pygame.mixer.Sound("sons/espera.wav")
gaming = pygame.mixer.Sound("sons/menu_theme.mp3")
class Client:
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = 0
        self.game = None
        self.server_ip = SERVER_IP
        self.server_port = SERVER_PORT

    def build_and_send_message(self, command: str, data: str) -> None:
        # Criando uma mensagem e enviando ao servidor
        message = chatlib.build_message(command, data) + chatlib.END_OF_MESSAGE
        self.__socket.send(message.encode())
        print("[SERVER] -> [{}]:  {}".format(self.__socket.getpeername(), message))

    def recv_message_and_parse(self) -> tuple:
        # Recebendo uma mensagem do servidor e analisando
        try:
            full_msg = ''
            while True:  # Recebendo uma mensagem em um loop, um caractere por vez, até que o caractere final da mensagem apareça
                char = self.__socket.recv(1).decode()
                if char == chatlib.END_OF_MESSAGE:
                    break
                full_msg += char
            cmd, data = chatlib.parse_message(full_msg)
            print("[{}] -> [SERVER]:  {}".format(self.__socket.getpeername(), full_msg))
            return cmd, data
        except:
            return None, None

    def connect(self):
        # Conectando ao servidor
        try:
            self.__socket.connect((self.server_ip, self.server_port))
            cmd, data = self.recv_message_and_parse()
            if cmd == chatlib.PROTOCOL_SERVER['error_msg']:
                raise Exception("ERROR: " + data)
            elif cmd == chatlib.PROTOCOL_SERVER['connected_successfully']:
                data = int(data)
                if data == 0 or data == 1:
                    self.id = data
            elif cmd == chatlib.PROTOCOL_SERVER['connection_limit']:
                raise Exception("Partida Cheia.")
            else:
                raise Exception("Mensagem de conexao invalida:", cmd, data)

        except Exception as e:
            return "Erro de conexao!!! " + str(e)

    def startup_screen(self):
        # Mostrando uma tela de inicialização solicitando que o player insira o IP e a PORTA do servidor
        
        # Criando uma janela Tkinter
        root = tk.Tk()
        root.title("Game Startup")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        startup_width = 400
        startup_height = 500
        root.geometry(f'{startup_width}x{startup_height}+{int(screen_width / 2 - startup_width / 2)}'
                      f'+{int(screen_height / 2 - startup_height / 2)}')
        root.protocol('WM_DELETE_WINDOW', exit)
        root.configure(bg='#777')
        root.resizable(False, False)

        # Adicionando widgets
        tk.Label(root, text='', bg='#777').pack()
        heading = tk.Label(root, text="SpaceBattle 🛩", font=('Calibri Bold', 40), bg='#777')
        heading.pack()

        tk.Label(root, text='', bg='#777').pack()
        tk.Label(root, text='', bg='#777').pack()
        tk.Label(root, text='', bg='#777').pack()
        ip = tk.Entry(root, width=25, fg='black', border=0, bg='#777', font=('Microsoft YaHei UI Light', 14))
        ip.insert(0, 'Server IP')
        ip.pack()

        def on_enter_ip(event):
            ip.delete(0, tk.END)

        def on_leave_ip(event):
            name = ip.get()
            if name == '':
                ip.insert(0, 'Server IP')

        ip.bind('<FocusIn>', on_enter_ip)
        ip.bind('<FocusOut>', on_leave_ip)

        tk.Frame(root, width=295, height=2, bg='black').pack()
        tk.Label(root, text='', bg='#777').pack()
        tk.Label(root, text='', bg='#777').pack()
        port = tk.Entry(root, width=25, fg='black', border=0, bg='#777', font=('Microsoft YaHei UI Light', 14))
        port.insert(0, 'Server port')
        port.pack()

        def on_enter_port(event):
            port.delete(0, tk.END)

        def on_leave_port(event):
            name = port.get()
            if name == '':
                port.insert(0, 'Server port')

        port.bind('<FocusIn>', on_enter_port)
        port.bind('<FocusOut>', on_leave_port)

        tk.Frame(root, width=295, height=2, bg='black').pack()

        tk.Label(root, text='', bg='#777').pack()
        tk.Label(root, text='', bg='#777').pack()
        tk.Label(root, text='', bg='#777').pack()
        tk.Label(root, text='', bg='#777').pack()

        def wait_start_msg(result: list):
            # Função para aguardar a mensagem de início do servidor
            global destroy_screen
            cmd, data = self.recv_message_and_parse()
            if cmd != chatlib.PROTOCOL_SERVER['game_starting_message']:
                messagebox.showerror("Game Start Error", "Error while waiting for another player to connect.")
                result.append(True)
                connect_and_start()
            result.append(True)
            return 1

        def connect_and_start():
            """Obtendo as informações fornecidas pelo cliente, verificando-as e conectando-se ao servidor.
            Se o jogo começar depois disso, comece o jogo. Se o jogo estiver esperando por outro jogador, exibindo uma tela de carregamento"""

            # Obtendo informações dos campos de entrada
            ip_txt = ip.get()
            port_txt = port.get()
            # Verificando as informações
            try:
                ipaddress.ip_address(ip_txt)
            except:
                messagebox.showerror("Invalid IP", "This IP address is invalid")
                return
            self.server_ip = ip_txt
            if not port_txt.isnumeric() or port_txt == '' or port_txt is None or not 0 <= int(port_txt) <= 65535:
                messagebox.showerror("Type Error", "Port must be a number between 0 and 65,535")
                return
            self.server_port = int(port_txt)

            status = self.connect()  # Conectando ao servidor
            if status:  # Sair se houver um erro
                messagebox.showerror("Error", status)
                return

            # Fechando a janela de conexão
            root.destroy()
            if self.id == 0:  # Se o jogador atual for o primeiro jogador -> Aguardando outro jogador.
                # Criando uma janela 'esperando pelo jogador'
                waiting_screen = tk.Tk()
                waiting_screen.geometry("400x400")
                waiting_screen.overrideredirect(True)
                waiting_screen.eval('tk::PlaceWindow . center')
                waiting_screen.configure(bg='white')
                result = []
                # Iniciando um thread para ouvir a mensagem inicial do servidor
                wait = threading.Thread(target=wait_start_msg, args=[result])
                wait.start()

                tk.Label(text="Esperando oponente conectar", font=('Calibri Bold', 20), background='#fff').pack()
                img = ImageLabel()
                img.pack()
                img.load(LOADING_IMG)
                espera.play()
      
                while True:
                    # Atualizando tela
                    waiting_screen.update()
                    waiting_screen.update_idletasks()
                    if result:  # Verificando se o servidor enviou uma mensagem inicial
                        waiting_screen.destroy()
                        break   
                    time.sleep(0.01)

                gaming.play()
        bt = tk.Button(root, width=27, pady=7, text='Conectar', bg='black', fg='white', border=0,
                       font=('Calibri Bold', 14), command=connect_and_start)
        bt.pack()
        root.mainloop()
        

    def disconnect(self):
        # Desconectando do servidor, fechando o socket e saindo do programa
        self.build_and_send_message(chatlib.PROTOCOL_CLIENT['disconnect_msg'], '')
        self.__socket.close()
        exit()

    def request_game_obj(self) -> None or int:
        # Solicitando o status atual do jogo
        try:
            self.build_and_send_message(chatlib.PROTOCOL_CLIENT['game_status_request'], '')
        except socket.error:
            return None
        cmd, data = self.recv_message_and_parse()
        if cmd != chatlib.PROTOCOL_SERVER['game_status_response']:
            if cmd == chatlib.PROTOCOL_SERVER['winner_msg']:  # Verificando se o jogo terminou e se há um vencedor
                if self.id == int(data):
                    messagebox.showinfo('Jogo Finalizado!', 'Parabens! Voce Venceu!!! :)')
                else:
                    messagebox.showinfo('Jogo Finalizado!', 'Voce perdeu!!! :(')
                self.disconnect()
            return None
        try:
            game_data = json.loads(data)  # Analisando o dicionário recebido
            self.game.score_0 = game_data['score_0']
            self.game.score_1 = game_data['score_1']
            for i in range(len(self.game.planes)):
                self.game.planes[i].data_from_dict(game_data['planes'][i])
            return 1
        except:
            return None

    def request_initial_data(self) -> dict or None:
        # Solicitando os dados iniciais do jogo para iniciar a partida
        try:
            self.build_and_send_message(chatlib.PROTOCOL_CLIENT['initial_details'], '')
        except socket.error:
            return None
        cmd, data = self.recv_message_and_parse()
        if cmd != chatlib.PROTOCOL_SERVER['initial_data_response']:
            return None
        try:
            data = json.loads(data)  # Carregando o dicionário
            return data
        except:
            return None

    def handle_key_press(self, key: int):
        # Enviando as informações relevantes para o servidor quando uma tecla é pressionada
        if self.id == 1:
            if key == pygame.K_RIGHT:
                key = pygame.K_d
            elif key == pygame.K_LEFT:
                key = pygame.K_a
        if (self.id == 0 and key in WHITE_CONTROLS) or (self.id == 1 and key in BLACK_CONTROLS) \
                or key == pygame.K_SPACE:  # Só enviando as informações se a tecla for permitida
            self.build_and_send_message(chatlib.PROTOCOL_CLIENT['key_down_msg'], str(key))

    def handle_key_release(self, key: int):
        # Enviando as informações relevantes para o servidor quando uma tecla é liberada
        if self.id == 1:
            if key == pygame.K_RIGHT:
                key = pygame.K_d
            elif key == pygame.K_LEFT:
                key = pygame.K_a
        if (self.id == 0 and key in WHITE_CONTROLS) or (self.id == 1 and key in BLACK_CONTROLS):
            # Só enviando as informações se a tecla for permitida
            self.build_and_send_message(chatlib.PROTOCOL_CLIENT['key_up_msg'], str(key))

    def start(self):
        # Iniciando e gerenciando o jogo
        self.startup_screen()  # Mostrando a tela de inicialização e conectando ao servidor
        init_data = self.request_initial_data()  # Obtendo dados iniciais
        if not init_data:
            messagebox.showerror('Data error', 'Could\'nt get game data')
            exit()
        # Configurando os parâmetros iniciais
        screen_width = init_data['width']
        screen_height = init_data['height']
        plane_pos = init_data['planes_pos']
        self.game = game.Game(screen_width, screen_height, plane_pos)
        self.game.initialise_window()  # Iniciando a janela do jogo
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    self.handle_key_press(key)
                elif event.type == pygame.KEYUP:
                    key = event.key
                    self.handle_key_release(key)
            self.request_game_obj()  # Atualizando os dados do jogo a cada iteração
            self.game.draw()
        self.disconnect()


if __name__ == '__main__':
    client = Client()
    client.start()
