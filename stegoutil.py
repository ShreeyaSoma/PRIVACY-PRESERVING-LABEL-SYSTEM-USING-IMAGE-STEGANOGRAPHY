from PIL import Image
import numpy as np
import datetime

def text_to_binary(text):
    return ''.join([format(ord(char), '08b') for char in text])

def binary_to_text(binary_data):
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    try:
        return ''.join([chr(int(char, 2)) for char in chars])
    except:
        return "[Decoding Error]"

def encode_text_to_image(secret_text, output_folder):
    binary_secret = text_to_binary(secret_text) + text_to_binary("#####")

    # Use your shield image as base
    img = Image.open("static/base/label_base.png")
    img = img.resize((300, 300))
    img = img.convert('RGB')
    data = np.array(img).copy()

    binary_index = 0
    for row in data:
        for pixel in row:
            for i in range(3):
                if binary_index < len(binary_secret):
                    pixel[i] = (pixel[i] & ~1) | int(binary_secret[binary_index])
                    binary_index += 1

    encoded_img = Image.fromarray(data)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"encoded_{timestamp}.png"
    full_path = f"{output_folder}/{filename}"
    encoded_img.save(full_path)
    return filename

def decode_image(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    data = np.array(img)

    binary_data = ''
    for row in data:
        for pixel in row:
            for i in range(3):
                binary_data += str(pixel[i] & 1)

    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ''
    for byte in chars:
        try:
            char = chr(int(byte, 2))
        except:
            break
        message += char
        if message.endswith("#####"):
            break

    if "#####" in message:
        return message.replace("#####", "")
    else:
        return "[No hidden message found]"
