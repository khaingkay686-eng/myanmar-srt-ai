from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "API running ✅"}

@app.post("/transcribe_srt")
async def transcribe_srt(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 🔥 TEMP DEMO SRT (AI မပါသေး)
    srt = """1
00:00:01,000 --> 00:00:03,000
မင်္ဂလာပါ

2
00:00:03,000 --> 00:00:05,000
ဒီက AI Subtitle Demo ဖြစ်ပါတယ်
"""

    return {"srt": srt}
