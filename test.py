import rsa 

public_key, private_key = rsa.newkeys(1024)

#with open("public.pem", "wb") as f :
#    f.write(public_key.save_pkcs1("PEM"))

#with open("private.pem", "wb") as f :
#    f.write(private_key.save_pkcs1("PEM"))


message = "bonjour"
print("Message : ", message)

encrypted_message = rsa.encrypt(message.encode(), public_key)
print("Message crypté : ", encrypted_message)

decrypted_message = rsa.decrypt(encrypted_message, private_key)
print("Message décrypté : ", decrypted_message.decode())
