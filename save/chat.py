import socket
import threading
from cryptography.fernet import Fernet
import os

# Fonction pour générer une nouvelle clé Fernet
def generate_fernet_key():
    return Fernet.generate_key()

def handle_client(client_socket, client_address):
    print(f"Connexion établie avec {client_address}")
    client_name = client_socket.recv(1024).decode('utf-8')
    clients[client_name] = client_socket
    while True:
        try:
            data = client_socket.recv(1024)
            data = data.decode("utf-8")
            if not data:
                break
            else:
                broadcast(data, client_name)
        except Exception as e:
            print(f"Erreur: {e}")
            break
    print(f"Déconnexion de {client_name}")
    del clients[client_name]
    client_socket.close()

def handle_command():
    while True:
        command = input("").split()
        if command[0] == '/create' and len(command) == 2:
            group_name = command[1]
            groups[group_name] = set()
            # Générer une clé Fernet pour le nouveau groupe
            groups_keys[group_name] = generate_fernet_key()
            print(f"Groupe '{group_name}' créé avec succès.")
            print(f"Clé du groupe '{group_name}': {groups_keys[group_name]}")
        elif command[0] == '/ass' and len(command) == 3:
            group_name = command[1]
            target_client = command[2]
            if group_name in groups:
                groups[group_name].add(target_client)
                print(f"Client '{target_client}' ajouté au groupe '{group_name}'.")
                # Envoyer la clé associée au groupe au client
                if target_client in clients:
                    client_socket = clients[target_client]
                    if group_name in groups_keys:
                        key = groups_keys[group_name]
                        try:
                            client_socket.send(f"{group_name}:{key}".encode('utf-8'))
                        except Exception as e:
                            print(f"Erreur lors de l'envoi de la clé au client : {e}")
            else:
                print(f"Groupe '{group_name}' n'existe pas.")
        elif command[0] == '/rem' and len(command) == 3:
            group_name = command[1]
            target_client = command[2]
            if group_name in groups:
                groups[group_name].remove(target_client)
                print(f"Client '{target_client}' retiré du groupe '{group_name}'.")
            else:
                print(f"Groupe '{group_name}' n'existe pas.")
        elif command[0] == '/see' and len(command) == 1:
            clients_without_group = []
            for group_name, clients_in_group in groups.items():
                print(f"Groupe '{group_name}':")
                if clients_in_group:
                    for client in clients_in_group:
                        print(f"    - {client}")
                else:
                    print("    Aucun client dans ce groupe.")
                clients_without_group = [client for client in clients if client not in clients_in_group]
            if clients_without_group:
                print("Clients sans groupe :")
                for client in clients_without_group:
                    print(f"    - {client}")
            else:
                print("Tous les clients sont dans des groupes.")


def broadcast(message, sender_name):
    for client_name, client_socket in clients.items():
        if client_name != sender_name:
            try:
                client_socket.send(f"{sender_name}:{message}".encode('utf-8'))
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
groups = {}
groups_keys = {}  

# Lancer le thread de gestion des commandes
command_thread = threading.Thread(target=handle_command)
command_thread.start()

while True:
    client_socket, client_address = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()
