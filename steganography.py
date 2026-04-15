from PIL import Image
import numpy as np
from crypto_utils import encrypt, decrypt

def text_to_bits(text):
    bits = ''.join(format(ord(c), '08b') for c in text)
    return bits + '1111111111111110'

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def encode(image: Image.Image, message: str, password: str = None) -> Image.Image:
    if password:
        message = encrypt(message, password)  # encrypt before hiding

    img = image.convert('RGB')
    pixels = np.array(img)
    flat = pixels.flatten()

    bits = text_to_bits(message)
    if len(bits) > len(flat):
        raise ValueError("Message is too long for this image.")

    for i, bit in enumerate(bits):
        flat[i] = (flat[i] & 0xFE) | int(bit)

    new_pixels = flat.reshape(pixels.shape)
    return Image.fromarray(new_pixels.astype('uint8'), 'RGB')

def decode(image: Image.Image, password: str = None) -> str:
    img = image.convert('RGB')
    pixels = np.array(img)
    flat = pixels.flatten()

    bits = ''.join(str(p & 1) for p in flat)
    delimiter = '1111111111111110'
    end = bits.find(delimiter)
    if end == -1:
        return "No hidden message found."

    extracted = bits_to_text(bits[:end])

    if password:
        result = decrypt(extracted, password)
        if result == "WRONG_PASSWORD":
            return "❌ Wrong password. Access denied."
        return result

    return extracted