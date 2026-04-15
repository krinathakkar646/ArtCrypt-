from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64

# Turns a password string into a proper AES key
def make_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    return kdf.derive(password.encode())

def encrypt(message: str, password: str) -> str:
    salt = os.urandom(16)       # random salt every time
    iv = os.urandom(16)         # random IV every time
    key = make_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    # Pad message to AES block size (16 bytes)
    msg_bytes = message.encode()
    pad_len = 16 - (len(msg_bytes) % 16)
    msg_bytes += bytes([pad_len] * pad_len)

    encrypted = encryptor.update(msg_bytes) + encryptor.finalize()

    # Pack salt + iv + encrypted together, encode as base64 string
    packed = base64.b64encode(salt + iv + encrypted).decode()
    return packed

def decrypt(packed_str: str, password: str) -> str:
    try:
        raw = base64.b64decode(packed_str.encode())
        salt = raw[:16]
        iv = raw[16:32]
        encrypted = raw[32:]

        key = make_key(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()

        decrypted = decryptor.update(encrypted) + decryptor.finalize()

        # Remove padding
        pad_len = decrypted[-1]
        return decrypted[:-pad_len].decode()

    except Exception:
        return "WRONG_PASSWORD"