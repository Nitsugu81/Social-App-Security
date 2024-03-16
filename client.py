import socket
import threading

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith('/friendresponse '):
                response = message.split(' ')[1]
                friend_name = message.split(' ')[2]
                if response == 'True':
                    friends.append(friend_name)
                    print(f"Vous avez ajouté {friend_name} à votre liste d'amis.")
                else:
                    print(f"{friend_name} n'existe pas.")
            else:
                print(message)
        except Exception as e:
            print(f"Erreur: {e}")
            break

def send_messages():
    while True:
        message = input()
        if message.startswith('/addfriend '):
            friend_name = message.split(' ')[1]
            client_socket.send(f"/checkfriend {friend_name}".encode('utf-8'))  # Envoie la demande au serveur pour vérifier l'ami
        elif message.startswith('/message '):
            parts = message.split(' ', 2)
            friend_name = parts[1]
            if friend_name in friends:
                client_socket.send(parts[2].encode('utf-8'))
            else:
                print("Cet utilisateur n'est pas dans votre liste d'amis.")
        else:
            client_socket.send(message.encode('utf-8'))

HOST = '127.0.0.1'
PORT = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

name = input("Entrez votre nom : ")
client_socket.send(name.encode('utf-8'))

friends = []

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
