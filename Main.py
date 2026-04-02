from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import yt_dlp
import json
import os

app = Flask(__name__)
CORS(app)

# Ensure config.json exists
if not os.path.exists('config.json'):
    with open('config.json', 'w') as f:
        json.dump({"title": "RACK FF | NEURAL CORE"}, f)

@app.route('/')
def index():
    return send_from_directory('.', 'Yt.html')

@app.route('/config.json')
def get_config():
    # Force no-cache so browsers don't hold onto the old title
    response = send_from_directory('.', 'config.json')
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/update_title', methods=['POST'])
def update_title():
    data = request.get_json()
    new_title = data.get('title')
    with open('config.json', 'w') as f:
        json.dump({"title": new_title}, f)
    print(f"[!] SAVED TITLE TO config.json: {new_title}") # Watch your terminal for this!
    return jsonify({"success": True})

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
    try:
        with yt_dlp.YoutubeDL({'format': 'best', 'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({"success": True, "video_url": info.get('url'), "title": info.get('title')})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
