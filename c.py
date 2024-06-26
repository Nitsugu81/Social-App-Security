import socket
import threading
from cryptography.fernet import Fernet
import ast
import ssl

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            parts = message.split(':')
            if len(parts) == 2:
                group_name, group_key = parts
                if group_name == "remove":
                    del groups_keys[group_key]
                    print(f"Vous avez été retiré du groupe '{group_key}'.")
                else:
                    if group_name in groups_keys : 
                        groups_keys[group_name] = group_key
                        print("Modification clef du groupe : ",group_name)
                    else : 
                        groups_keys[group_name] = group_key
                        print("Ajouté au groupe : ",group_name)
            
            else:
                sender, group_name, message_content = parts
                if group_name in groups_keys:  # Vérification si le groupe existe dans les clés
                    key_string = groups_keys[group_name]
                    key_bytes = ast.literal_eval(key_string)
                    cipher_suite = Fernet(key_bytes)
                    
                    message_content = ast.literal_eval(message_content)
                    message_content= cipher_suite.decrypt(message_content)
                    
                    print(sender,":",group_name,":",message_content)
                else:
                    message = " : ".join(message.split(":"))
                    print(message)
        except Exception as e:
            print(f"Erreur: {e}")
            break



def send_messages():
    while True:
        message = input()
        if message.startswith('/'):
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


HOST = '127.0.0.1'
PORT = 8000

# Chargement du certificat auto-signé
context = ssl.create_default_context()
context.load_verify_locations("cert.pem")  # Remplacez "path_to_your_certificate.pem" par le chemin de votre certificat


client_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname="localhost")
client_socket.connect((HOST, PORT))

name = input("Entrez votre nom : ")
client_socket.send(name.encode('utf-8'))


groups_keys = {}  # Dictionnaire pour stocker les clés des groupes

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
