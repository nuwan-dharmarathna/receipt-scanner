from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from google.cloud import speech_v1 as speech
import io
from pydub import AudioSegment
import datetime

from models.gpt_model import extract_transaction_details
from models.text_translation_model import trans_client

router = APIRouter()

# Load Google Cloud Speech Client
client = speech.SpeechClient.from_service_account_file("gcp_key.json")

@router.post("/voice-translate/")
async def translate_audio(
    file: UploadFile = File(...), 
    language_code: str = Form("en-US")  # Default to English if not provided
):
    try:
        # Read uploaded file
        audio_bytes = await file.read()

        # Convert to mono & 16kHz
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        audio = audio.set_channels(1).set_frame_rate(16000)

        # Export to WAV format in a byte buffer
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        
        # Read WAV content
        wav_content = wav_buffer.read()

        # Google Speech-to-Text API request
        recognition_audio = speech.RecognitionAudio(content=wav_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,  # Dynamic language code
        )

        response = client.recognize(config=config, audio=recognition_audio)
        
        gpt_response = {}
        transcript = None
        
        for result in response.results:
            transcript = result.alternatives[0].transcript
        
        print(f"Transcript: {transcript}")
        
        if transcript:
            if language_code == "si-LK":
                # Perform translation
                result = trans_client.translate(transcript, target_language="en")
                # result = await translator.translate(transcript, src='si', dest='en')
                print(f"Translated Text: {result['translatedText']}")
                transcript = result["translatedText"]
                print(f"Translated Transcript: {transcript}")
            gpt_response = extract_transaction_details(transcript)
        else:
            raise HTTPException(status_code=500, detail="No transcript found")
    
    
            
        return {
            "transactionType": gpt_response["transactionType"],
            "amount": gpt_response.get("amount", 0),
            "description": gpt_response["description"],
            "category": gpt_response["category"],
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "recieptUrl": None,
            "isRecurring": False,
            "recurringInterval": None,
            "nextRecurringDate": None,
            "lastProcessed": None,
            "transactionStatus": "completed"
        }

        # Extract transcriptions
        # transcriptions = [
        #     {"transcript": result.alternatives[0].transcript, "confidence": result.alternatives[0].confidence}
        #     for result in response.results
        # ]

        # return {"language": language_code, "transcriptions": transcriptions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")
