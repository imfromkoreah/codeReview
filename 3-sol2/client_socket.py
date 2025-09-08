import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message == '/종료':
                print('서버가 연결을 종료했습니다.')
                break
            print(message)
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))

threading.Thread(target=receive_messages, args=(client_socket,)).start()

while True:
    msg = input()
    client_socket.send(msg.encode())
    if msg == '/종료':
        break

client_socket.close()
