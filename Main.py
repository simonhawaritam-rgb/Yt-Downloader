import os
import json
from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

# Load your custom config (RACK FF | NEURAL CORE)
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"title": "YouTube Downloader", "version": "1.0"}

@app.route('/')
def index():
    config = load_config()
    return render_template('yt.html', config=config)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    # Temporary download path (Railway files are temporary)
    output_path = '/tmp/%(title)s.%(ext)s'

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info)
            
            # Send file to user and then cleanup (optional)
            return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # CRITICAL: Railway provides the port via an environment variable
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
