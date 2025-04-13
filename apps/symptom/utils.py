from cryptography.fernet import Fernet
from decouple import config

key = config('FERNET_KEY').encode()
cipher_suite = Fernet(key)

def encrypt_file(data):
    print(f"FERNET_KEY: {key}")
    return cipher_suite.encrypt(data)

def decrypt_file(encrypted_data):
    print(f"FERNET_KEY: {key}")
    return cipher_suite.decrypt(encrypted_data)