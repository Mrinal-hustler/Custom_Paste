
BOT_TOKEN = "6729717811:AAEeW-xlnvGHtfm2HUOV47ewkdKu2sKUxYQ"
CHAT_ID = "5067741519"  # Replace with the chat ID or use dynamic fetching

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Telegram Bot Token and Chat ID
BOT_TOKEN = "6729717811:AAEeW-xlnvGHtfm2HUOV47ewkdKu2sKUxYQ"  # Replace with your bot token
CHAT_ID = "5067741519"  # Replace with your Telegram chat ID

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Send the file to Telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(filepath, 'rb') as doc:
        response = requests.post(url, data={"chat_id": CHAT_ID}, files={"document": doc})

    os.remove(filepath)

    if response.status_code == 200:
        return jsonify({"message": "File sent to Telegram!"})
    else:
        return jsonify({"message": "Failed to send file to Telegram"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
