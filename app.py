from flask import Flask, render_template, request
import os
from stegoutil import encode_text_to_image, decode_image
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'output_images'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']

    secret_data = f"Name: {name}\nAddress: {address}\nPhone: {phone}"

    try:
        filename = encode_text_to_image(secret_data, OUTPUT_FOLDER)
        web_path = f"/{OUTPUT_FOLDER}/{filename}"
        return render_template('index.html', encoded_image=web_path, success="✅ Info encoded successfully!")
    except Exception as e:
        return render_template('index.html', error=f"Error: {str(e)}")

@app.route('/decode', methods=['POST'])
def decode():
    image = request.files['decode_image']
    if not image:
        return render_template('index.html', error="No image uploaded for decoding.")

    filename = secure_filename(image.filename)
    decode_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(decode_path)

    try:
        hidden_text = decode_image(decode_path)
        return render_template('index.html', decoded_text=hidden_text)
    except Exception as e:
        return render_template('index.html', error=f"Decoding failed: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
