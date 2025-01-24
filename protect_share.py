import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt(password: str, plaintext: str) -> str:
    if password == "":
        return plaintext
    # Generate a random 16-byte salt
    salt = os.urandom(16)
    # Derive a 32-byte key using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode('utf-8'))
    
    # Generate a random 12-byte nonce for AES-GCM
    nonce = os.urandom(12)
    # Encrypt the plaintext
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
    
    # Combine salt, nonce, tag, and ciphertext
    encrypted_data = salt + nonce + encryptor.tag + ciphertext
    # Return as base64-encoded string
    return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

def decrypt(password: str, encrypted_data_b64: str) -> str:
    if password == "":
        return encrypted_data_b64
    # Decode the base64 string
    encrypted_data = base64.urlsafe_b64decode(encrypted_data_b64)
    # Extract components
    salt = encrypted_data[:16]
    nonce = encrypted_data[16:28]
    tag = encrypted_data[28:44]
    ciphertext = encrypted_data[44:]
    
    # Derive the key using the same salt and parameters
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode('utf-8'))
    
    # Decrypt the ciphertext
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode('utf-8')
