import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}  # {client_socket: username}

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print('채팅 서버가 시작되었습니다. {}:{}'.format(self.host, self.port))

        while True:
            client_socket, addr = self.server_socket.accept()
            print('{} 연결됨'.format(addr))
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def broadcast_message(self, message, exclude_socket=None):
        for client_socket in self.clients:
            if client_socket != exclude_socket:
                try:
                    client_socket.send(message.encode())
                except Exception:
                    client_socket.close()
                    self.remove_client(client_socket)

    def send_private_message(self, sender_socket, target_name, message):
        target_socket = None
        for sock, name in self.clients.items():
            if name == target_name:
                target_socket = sock
                break
        if target_socket:
            formatted_message = '(귓속말) {}> {}'.format(self.clients[sender_socket], message)
            target_socket.send(formatted_message.encode())
        else:
            sender_socket.send('사용자를 찾을 수 없습니다.'.encode())

    def handle_client(self, client_socket):
        try:
            client_socket.send('사용자 이름을 입력하세요: '.encode())
            username = client_socket.recv(1024).decode().strip()
            self.clients[client_socket] = username
            self.broadcast_message('{}님이 입장하셨습니다.'.format(username))

            while True:
                message = client_socket.recv(1024).decode().strip()
                if not message:
                    continue
                if message == '/종료':
                    client_socket.send('/종료'.encode())
                    self.remove_client(client_socket)
                    break
                # 귓속말 처리
                if message.startswith('/귓속말 '):
                    parts = message.split(' ', 2)
                    if len(parts) >= 3:
                        target_name = parts[1]
                        private_msg = parts[2]
                        self.send_private_message(client_socket, target_name, private_msg)
                    else:
                        client_socket.send('사용법: /귓속말 <사용자> <메시지>'.encode())
                    continue
                # 일반 메시지
                formatted_message = '{}> {}'.format(username, message)
                print(formatted_message)
                self.broadcast_message(formatted_message, exclude_socket=None)
        except Exception as e:
            print('오류:', e)
            self.remove_client(client_socket)

    def remove_client(self, client_socket):
        username = self.clients.get(client_socket, '알 수 없는 사용자')
        if client_socket in self.clients:
            del self.clients[client_socket]
        client_socket.close()
        self.broadcast_message('{}님이 퇴장하셨습니다.'.format(username))


if __name__ == '__main__':
    server = ChatServer()
    server.start_server()
