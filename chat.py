import socket
import threading

def handle_client(client_socket, client_address):
    print(f"Connexion établie avec {client_address}")
    client_name = client_socket.recv(1024).decode('utf-8')
    clients[client_name] = client_socket
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"{client_name}: {data.decode('utf-8')}")
            if data.startswith(b'/checkfriend'):
                friend_name = data.decode('utf-8').split(' ')[1]
                if friend_name in clients:
                    client_socket.send(f"/friendresponse True {friend_name}".encode('utf-8'))
                else:
                    client_socket.send(f"/friendresponse False {friend_name}".encode('utf-8'))
            else:
                broadcast(data, client_name)
        except Exception as e:
            print(f"Erreur: {e}")
            break
    print(f"Déconnexion de {client_name}")
    del clients[client_name]
    client_socket.close()


def broadcast(message, sender_name):
    for client_name, client_socket in clients.items():
        if client_name != sender_name:
            try:
                client_socket.send(f"{sender_name}: {message}".encode('utf-8'))
            except Exception as e:
                print(f"Erreur lors de l'envoi du message : {e}")
                client_socket.close()
                del clients[client_name]

HOST = '127.0.0.1'
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"Serveur en attente de connexions sur le port {PORT}")

clients = {}

while True:
    client_socket, client_address = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()
