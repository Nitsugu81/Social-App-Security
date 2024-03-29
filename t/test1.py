import socket
import ssl
import os

# Générer un certificat auto-signé pour le serveur
os.system("openssl req -new -x509 -days 365 -nodes -out server.pem -keyout server.pem")

# Créer un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liaison du socket à l'adresse et au port
server_address = ('localhost', 10000)
server_socket.bind(server_address)

# Écoute pour les connexions entrantes
server_socket.listen(1)

print("Le serveur écoute sur le port", server_address[1])

# Accepter la connexion
connection, client_address = server_socket.accept()

# Ajouter une couche SSL
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile="server.pem")
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.load_verify_locations(cafile="client.pem")  # Utilisez le certificat du client pour la vérification

ssl_connection = ssl_context.wrap_socket(connection, server_side=True)

try:
    print("Connexion établie depuis :", client_address)
    
    # Vérification du certificat du client
    cert = ssl_connection.getpeercert()
    if not cert:
        raise ValueError("La vérification du certificat a échoué.")
    
    # Vérification de l'identité du client
    subject = dict(x[0] for x in cert['subject'])
    common_name = subject.get('commonName')
    print(common_name)
    if common_name != "test":
        raise ValueError("L'identité du client n'est pas celle attendue.")

    # Recevoir les données du client
    data = ssl_connection.recv(1024)
    print("Reçu :", data.decode())

    # Envoyer une réponse au client
    message = "Message reçu par le serveur"
    ssl_connection.sendall(message.encode())

finally:
    # Fermer la connexion
    ssl_connection.close()