from flask import Flask, request, jsonify, send_from_directory
from video_engine import generate_script, generate_images, generate_voice, generate_music, combine_assets
import os

app = Flask(__name__)
VIDEO_DIR = 'videos'
os.makedirs(VIDEO_DIR, exist_ok=True)

@app.route('/api/generate', methods=['POST'])
def generate_video():
    data = request.get_json()
    topic = data.get('topic', 'default topic')
    video_type = data.get('type', 'short')
    duration = 60 if video_type == 'short' else 420

    try:
        script = generate_script(topic, duration)
        scenes = generate_images(script)
        voice_path = generate_voice(script)
        music_path = generate_music()
        video_path = combine_assets(scenes, voice_path, music_path)
        return jsonify({'url': f'/videos/{video_path}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(VIDEO_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
