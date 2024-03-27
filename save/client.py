import socket
import threading
from cryptography.fernet import Fernet
import ast
import sys 

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print(f"Erreur: {e}")
            break

def send_messages():
    while True:
        message = input()
        if message.startswith('/'):
            print(groups_keys)
            parts = message.split(' ', 1)
            if len(parts) >= 2:
                command, content = parts
                if command == '/all':
                    client_socket.send(f"all:{content}".encode())
                elif command.startswith('/'):
                    group_name = command[1:]
                    if group_name in groups_keys:
                        key_string = groups_keys[group_name]
                        key_bytes = ast.literal_eval(key_string)
                        cipher_suite = Fernet(key_bytes)
                        encrypted_message = cipher_suite.encrypt(content.encode())
                        client_socket.send(f"{group_name}:{encrypted_message}".encode())
                    else:
                        print("Le groupe spécifié n'existe pas ou la clé est manquante.")
                else:
                    print("Commande non valide.")
            else:
                print("Commande non valide.")
        else:
            print("Choissisez un destinataire : '/all' or  '/group'")

def receive_group_key():
    while True:
        try:
            key_message = client_socket.recv(1024).decode('utf-8')
            parts = key_message.split(':')
            if len(parts) == 2:
                group_name, group_key = parts
                groups_keys[group_name] = group_key
                print(key_message)
            else:
                break
        except Exception as e:
            print(f"Erreur lors de la réception de la clé du groupe : {e}")
            break

HOST = '127.0.0.1'
PORT = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

name = input("Entrez votre nom : ")
client_socket.send(name.encode('utf-8'))


groups_keys = {}  # Dictionnaire pour stocker les clés des groupes

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()

group_key_thread = threading.Thread(target=receive_group_key)
group_key_thread.start()
