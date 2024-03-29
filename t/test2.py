import socket
import ssl
import os

# Générer un certificat auto-signé pour le client
os.system("openssl req -new -x509 -days 365 -nodes -out client.pem -keyout client.pem")

# Créer un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion du socket au serveur et ajout d'une couche SSL
ssl_socket = ssl.wrap_socket(client_socket, certfile="client.pem")

server_address = ('localhost', 10000)
ssl_socket.connect(server_address)

try:
    # Envoyer des données au serveur
    message = "Bonjour, serveur!"
    ssl_socket.sendall(message.encode())

    # Recevoir une réponse du serveur
    data = ssl_socket.recv(1024)
    print("Reçu :", data.decode())

finally:
    # Fermer la connexion
    ssl_socket.close()
