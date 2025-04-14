import os
import shutil
import uuid
import subprocess

# Ensure the videos directory exists
os.makedirs("videos", exist_ok=True)

def generate_script(topic, duration):
    return f"Welcome to a deep dive on {topic}. Let’s explore in detail..."

def generate_images(script):
    sentences = script.split('.')
    image_paths = []
    for i, _ in enumerate(sentences):
        filename = f'videos/scene{i}.png'
        shutil.copyfile('public/sample.jpg', filename)
        image_paths.append(filename)
    return image_paths

def generate_voice(script):
    voice_path = f'videos/voice-{uuid.uuid4()}.wav'
    shutil.copyfile('public/sample-voice.wav', voice_path)
    return voice_path

def generate_music():
    return 'public/music.mp3'

def combine_assets(images, voice, music):
    output_path = f'videos/video-{uuid.uuid4()}.mp4'
    cmd = [
        'ffmpeg', '-loop', '1', '-i', images[0], '-i', voice, '-i', music,
        '-c:v', 'libx264', '-t', '30', '-pix_fmt', 'yuv420p', '-shortest', output_path
    ]
    subprocess.run(cmd, check=True)
    return output_path  # Return full path

def generate_video(prompt, script, voice, format_ratio):
    images = generate_images(script)
    voice_path = generate_voice(script)
    music_path = generate_music()
    final_video_path = combine_assets(images, voice_path, music_path)
    return final_video_path
