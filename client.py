import socket
from cryptography.fernet import Fernet
# Configuration du client
HOST = '127.0.0.1'
PORT = 12345

# Fonction pour recevoir et déchiffrer un message
def receive_decrypted_message(client_socket):
    encrypted_message = client_socket.recv(1024)
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
    print("Message reçu:", decrypted_message)

# Code principal du client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    # Envoyer le groupe au serveur
    group = input("Entrez votre groupe : ")
    client_socket.send(group.encode())

    # Recevoir la clé de groupe
    key = client_socket.recv(1024)

    # Configurer la clé de chiffrement pour le groupe
    cipher_suite = Fernet(key)

    print("Connecté au serveur. Vous pouvez commencer à envoyer des messages.")

    while True:
        message = input("Votre message : ")
        client_socket.send(message.encode())
        receive_decrypted_message(client_socket)
