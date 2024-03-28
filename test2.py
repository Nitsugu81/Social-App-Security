from cryptography.fernet import Fernet

# Clé de chiffrement
key_string = b'PE8JfTD393CotRpfvj6FcEa8WGxWmn9Lq66ZAh9j1lg='
key_bytes = key_string

# Message à décoder
encrypted_message = "b'gAAAAABmBZJ_7k4XPZxLgx3Sp8qJHUwO42vBuGlBFZLOlnDL7SBKyPK3C2au8k5R9fCdnysFH9rugrtx535uHLzwu6N3mk5I2Q=='"

# Initialisation de l'objet Fernet
cipher_suite = Fernet(key_bytes)

# Décodage du message
decrypted_message = cipher_suite.decrypt(encrypted_message)

# Affichage du message décrypté
print(decrypted_message.decode())
