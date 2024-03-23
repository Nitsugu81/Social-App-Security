import socket
from cryptography.fernet import Fernet

# Générer une clé de chiffrement
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Configuration du serveur
HOST = '127.0.0.1'
PORT = 12345

# Dictionnaire pour stocker les clés des groupes
group_keys = {}

# Fonction pour envoyer un message chiffré à tous les clients du groupe
def send_encrypted_message(client_socket, message, group):
    if group in group_keys:
        key = group_keys[group]
        encrypted_message = cipher_suite.encrypt(message.encode())
        client_socket.send(encrypted_message)
    else:
        client_socket.send("Error: Group key not found".encode())

# Code principal du serveur
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Serveur en écoute...")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connexion établie avec {addr}")

            # Recevoir le groupe de l'utilisateur
            group = conn.recv(1024).decode()

            # Envoyer la clé de groupe à l'utilisateur
            conn.send(key)

            # Stocker la clé de groupe pour le groupe spécifié
            group_keys[group] = key

            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # Envoyer le message chiffré à tous les clients du même groupe
                for client_group, client_key in group_keys.items():
                    if client_group != group:
                        send_encrypted_message(conn, data, client_group)
