from fastapi import APIRouter, UploadFile, File, HTTPException
from models.whisper_model import whisper_model
from models.gpt_model import extract_transaction_details
import os
import shutil
import datetime

router = APIRouter()

@router.post("/voice-translate/")
async def translate_audio(file: UploadFile = File(...)):
    # Create 'audio' folder if not exists
    audio_path = f"public/{file.filename}"
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)

    # Save the audio file
    try:
        with open(audio_path, "wb") as audio_file:
            shutil.copyfileobj(file.file, audio_file)
        
        # Transcribe and translate
        result = whisper_model(audio_path, beam_size=5, language="auto")
        print(f"Raw Whisper Response: {result}")
        response = extract_transaction_details(result['text'])
        print(f"Extracted Transaction Details: {response}")
        
        # Remove the audio file after processing
        os.remove(audio_path)
        
        return {
        "transactionType": response["transactionType"],
        "amount": response.get("amount", 0),
        "description": response["description"],
        "category": response["category"],
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "recieptUrl": None,
        "isRecurring": False,
        "recurringInterval": None,
        "nextRecurringDate": None,
        "lastProcessed": None,
        "transactionStatus": "completed"
    }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")