import json
import socket
import threading
import time
import pygame
import select
from game import Game
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SERVER_LISTEN_IP, SERVER_PORT, ROTATE_AMOUNT, FPS
import chatlib

class Server:
    def __init__(self):
        # Propriedades do servidor
        self.players_status = []
        self.game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_ip = SERVER_LISTEN_IP
        self.port = SERVER_PORT
        self.messages_to_send = []
        self.players = []
        self.setup_socket()
        self.game_running = True
        self.last_shot_white = 0
        self.last_shot_black = 0
        self.winner = None

    def setup_socket(self):
        # Configurando o socket para o servidor
        try:
            address = (self.listen_ip, self.port)
            self.__server_socket.bind(address)
            self.__server_socket.listen()
            print("[SERVER] Listening for connections...")
        except socket.error as e:
            print("[SERVER] An error occurred:", str(e))
            exit()

    def build_and_send_message(self, client_socket: socket.socket, command: str, data: str) -> None:
        # Construindo uma mensagem de acordo com o protocolo e enviando ao cliente
        message = chatlib.build_message(command, data) + chatlib.END_OF_MESSAGE
        self.messages_to_send.append((client_socket, message))
        print("[SERVER] -> [{}]:  {}".format(client_socket.getpeername(), message))

    def recv_message_and_parse(self, client_socket: socket.socket) -> tuple:
        # Recebendo a mensagem do cliente e analisando de acordo com o protocolo
        try:
            full_msg = ''
            while True:  # Recebendo uma mensagem em um loop, um caractere por vez, até que o caractere final da mensagem apareça
                char = client_socket.recv(1).decode()
                if char == chatlib.END_OF_MESSAGE:
                    break
                full_msg += char
            cmd, data = chatlib.parse_message(full_msg)
            print("[{}] -> [SERVER]:  {}".format(client_socket.getpeername(), full_msg))
            return cmd, data
        except:
            return None, None

    def disconnected_player(self, disconnected_socket: socket.socket) -> None:
        # Desconectando um jogador do servidor
        if not self.winner:  # Se o jogador desconectado sair antes do final do jogo, o segundo jogador vence
            winner_id = 1 - self.players.index(disconnected_socket)
            self.winner = winner_id
        self.players.remove(disconnected_socket)
        disconnected_socket.close()  # Fechando o socket do jogador
        if len(self.players) == 0:  # Se o último jogador sair, reinicia o servidor
            self.__server_socket.close()
            self.__init__()
            self.start()

    def handle_client_key_down(self, client_socket: socket.socket, data: str) -> None:
        # Manipulando a mensagem quando o cliente pressiona uma tecla
        try:
            data = int(data)  # O valor deve estar no formato "int"
        except:
            return
        plane_num = self.players.index(client_socket)  # Obtendo o índice do jogador
        if plane_num == 0:  # Se o jogador for o jato branco
            if data == pygame.K_LEFT:
                self.game.planes[plane_num].rotate_amount = ROTATE_AMOUNT
            elif data == pygame.K_RIGHT:
                self.game.planes[plane_num].rotate_amount = -ROTATE_AMOUNT
        elif plane_num == 1:  # Se o jogador for o jato preto
            if data == pygame.K_a:
                self.game.planes[plane_num].rotate_amount = ROTATE_AMOUNT
            elif data == pygame.K_d:
                self.game.planes[plane_num].rotate_amount = -ROTATE_AMOUNT
        if data == pygame.K_SPACE:  # A tecla de espaço (tiro) é válida para ambas as cores (dois players)
            if plane_num == 0:
                if time.time() - self.last_shot_white < 1.5:  # Verificando se o jogador um já pode atirar novamente
                    return
                else:
                    self.last_shot_white = time.time()
            elif plane_num == 1:
                if time.time() - self.last_shot_black < 1.5:  # Verificando se o jogador dois já pode atirar novamente
                    return
                else:
                    self.last_shot_black = time.time()
            self.game.planes[plane_num].shoot()  # Atirando

    def handle_client_key_up(self, client_socket: socket.socket, data: str) -> None:
        # Manipulando a mensagem de que o cliente liberou uma tecla
        try:
            data = int(data)
        except:
            return
        plane_num = self.players.index(client_socket)
        if plane_num == 0:
            if data == pygame.K_LEFT or data == pygame.K_RIGHT:
                self.game.planes[plane_num].rotate_amount = 0
        elif plane_num == 1:
            if data == pygame.K_a or data == pygame.K_d:
                self.game.planes[plane_num].rotate_amount = 0

    def handle_status_message(self, client_socket: socket.socket):
        # Enviando o status atual do jogo para o cliente
        if self.winner == 0 or self.winner == 1:  # Se houver um vencedor, envia uma mensagem de vencedor
            self.build_and_send_message(client_socket, chatlib.PROTOCOL_SERVER['winner_msg'], str(self.winner))
        else:
            game_str = json.dumps(self.game.up_to_date_game_data())
            # Obtem dados do jogo na forma de um dicionário em formato de string e envia ao cliente
            self.build_and_send_message(client_socket, chatlib.PROTOCOL_SERVER['game_status_response'], game_str)

    def handle_game_init_request(self, client_socket: socket.socket):
        # Lidando com a solicitação inicial de dados do jogo
        initial_data = json.dumps(self.game.get_init_data())
        self.build_and_send_message(client_socket, chatlib.PROTOCOL_SERVER['initial_data_response'], initial_data)

    def handle_message(self, client_socket: socket.socket, command: str, data: str) -> None:
        # Chamando a função apropriada para cada solicitação
        if command == chatlib.PROTOCOL_CLIENT['disconnect_msg']:
            self.disconnected_player(client_socket)
        elif command == chatlib.PROTOCOL_CLIENT['key_down_msg']:
            self.handle_client_key_down(client_socket, data)
        elif command == chatlib.PROTOCOL_CLIENT['game_status_request']:
            self.handle_status_message(client_socket)
        elif command == chatlib.PROTOCOL_CLIENT['initial_details']:
            self.handle_game_init_request(client_socket)
        elif command == chatlib.PROTOCOL_CLIENT['key_up_msg']:
            self.handle_client_key_up(client_socket, data)

    def update_game(self):
        # Atualizando dados do jogo
        while self.game_running:
            self.game.update()
            self.game.clock.tick(FPS)

    def start(self) -> None:
        # Iniciando o servidor e ouvindo conexões e solicitações
        pygame.init()  # Inicializando o pygame
        threading.Thread(target=self.update_game).start()  # Atualizando o jogo em tópicos separados
        while True:
            if self.game.hits:  # Se alguma das balas atingir um avião, atualiza a pontuação
                for bullet in self.game.hits:
                    if bullet.is_white:
                        self.game.score_0 += 1
                    else:
                        self.game.score_1 += 1
                    self.game.hits.remove(bullet)
            # Verificando se um jogador ganhou
            if self.game.score_0 == 5:
                self.winner = 0
            elif self.game.score_1 == 5:
                self.winner = 1
            # Verificando se há mensagens disponíveis de jogadores tentando se conectar
            read_list, write_list, error_list = select.select([self.__server_socket] + self.players, self.players, [])
            for current_socket in read_list:
                if current_socket is self.__server_socket:  # Se um novo cliente estiver tentando se conectar
                    client_socket, client_address = self.__server_socket.accept()
                    if len(self.players) >= 2:  # Verificando se a quantidade máxima de clientes foi atingida
                        self.build_and_send_message(client_socket, chatlib.PROTOCOL_SERVER['connection_limit'], '')
                        client_socket.close()
                    else:
                        # Conectando o jogador
                        player_id = len(self.players)  # Obtendo o ID do jogador
                        self.build_and_send_message(client_socket, chatlib.PROTOCOL_SERVER['connected_successfully'],
                                                    str(player_id))  # Enviando a mensagem de conexão bem-sucedida
                        self.players.append(client_socket)
                        if player_id == 1:
                            # Se o segundo jogador se conectar, envia ao primeiro jogador uma mensagem de início do jogo
                            self.build_and_send_message(self.players[0],
                                                        chatlib.PROTOCOL_SERVER['game_starting_message'], '')
                else:  # Se um jogador enviou uma solicitação
                    command, data = self.recv_message_and_parse(current_socket)  # Recebendo a solicitação
                    if command is None:  # Se houve um erro com a mensagem
                        self.disconnected_player(current_socket)  # Desconectando o cliente
                    try:
                        self.handle_message(current_socket, command, data)  # Tratamento da mensagem do cliente
                    except socket.error:
                        self.disconnected_player(current_socket)  # Se ocorrer um erro ao desconectar o cliente

            # Enviando todas as mensagens que podem ser enviadas
            for message in self.messages_to_send:
                current_socket, data = message
                if current_socket in write_list:
                    if current_socket in self.players:
                        current_socket.send(data.encode())
                        self.messages_to_send.remove(message)


if __name__ == '__main__':
    server = Server()
    server.start()
