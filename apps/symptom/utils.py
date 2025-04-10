from cryptography.fernet import Fernet

# Generar una clave (esto debe hacerse una vez y almacenarse de forma segura)
KEY = Fernet.generate_key()
cipher_suite = Fernet(KEY)

def encrypt_file(file_data):
    return cipher_suite.encrypt(file_data)

def decrypt_file(encrypted_data):
    return cipher_suite.decrypt(encrypted_data)