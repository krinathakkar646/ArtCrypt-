from generate import generate_image
from steganography import encode, decode

def generate_and_hide(prompt: str, message: str):
    print("Generating image...")
    image = generate_image(prompt)

    print("Hiding message in image...")
    result = encode(image, message)
    
    return result

def reveal_from_image(image):
    return decode(image)