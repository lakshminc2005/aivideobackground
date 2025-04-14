from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import video_engine  # Your existing video logic module

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

        # Call your video generation function
        file_path = video_engine.generate_video(prompt, script, voice, format_ratio)

        # Return the video file as downloadable
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
