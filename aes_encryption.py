from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_data(data, key):
    iv = os.urandom(16)  # AES requires a 16-byte IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad data to be a multiple of 16 bytes
    padding_length = 16 - (len(data) % 16)
    padded_data = data + (chr(padding_length) * padding_length).encode()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext  # Store IV with the ciphertext

def decrypt_data(encrypted_data, key):
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    padding_length = padded_data[-1]
    return padded_data[:-padding_length]

key = os.urandom(32)  
data = b"Data"

encrypted = encrypt_data(data, key)
decrypted = decrypt_data(encrypted, key)

print("Encrypted:", encrypted)
print("Decrypted:", decrypted.decode())
