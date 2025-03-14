from fastapi import APIRouter, UploadFile, File, HTTPException
from models.whisper_model import whisper_model
import os

router = APIRouter()

@router.post("/translate/")
async def translate_audio_route(file: UploadFile = File(...)):
    audio_path = f"audio/{file.filename}"
    
    # Save the audio file temporarily
    with open(audio_path, "wb") as f:
        f.write(file.file.read())
    
    # Whisper will auto-detect the language and translate directly to English
    result = whisper_model(audio_path, generate_kwargs={"task": "translate"})
    
    # Remove the temporary file
    os.remove(audio_path)
    
    return {"translated_text": result["text"]}