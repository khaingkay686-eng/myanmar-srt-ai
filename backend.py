from fastapi import FastAPI, UploadFile, File
import whisper
from moviepy.editor import VideoFileClip
import os
from googletrans import Translator

app = FastAPI()
model = whisper.load_model("base")
translator = Translator()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def video_to_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.close()

def format_time(seconds):
    ms = int((seconds - int(seconds)) * 1000)
    s = int(seconds)
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"

def make_srt(segments):
    srt = ""
    for i, seg in enumerate(segments, start=1):
        start = format_time(seg["start"])
        end = format_time(seg["end"])
        text = translator.translate(seg["text"], dest="my").text
        srt += f"{i}\n{start} --> {end}\n{text}\n\n"
    return srt

@app.post("/transcribe_srt")
async def transcribe_srt(file: UploadFile = File(...)):
    video_path = f"{UPLOAD_DIR}/{file.filename}"
    audio_path = video_path + ".mp3"

    with open(video_path, "wb") as f:
        f.write(await file.read())

    video_to_audio(video_path, audio_path)

    result = model.transcribe(audio_path)

    return {"srt": make_srt(result["segments"])}
