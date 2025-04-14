from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import video_engine  # Importing from video_engine.py
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def home():
    return jsonify({"message": "AI Video Generator Backend is running!"})

@app.route("/generate", methods=["POST"])
def generate_video():
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        script = data.get("script")
        voice = data.get("voice")
        format_ratio = data.get("format")

        if not all([prompt, script, voice, format_ratio]):
            return jsonify({"error": "Missing required fields"}), 400

        print("Received data:", data)

        file_path = video_engine.generate_video(prompt, script, voice, format_ratio)
        print("Generated video at:", file_path)

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        print("Error generating video:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    os.makedirs("videos", exist_ok=True)
    app.run(debug=True)
