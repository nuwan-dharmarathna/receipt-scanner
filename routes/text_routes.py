from fastapi import APIRouter, HTTPException, Request
from models.text_translation_model import trans_client
from models.gpt_model import extract_transaction_details
import os
import datetime

router = APIRouter()

@router.post("/text-translate/")
async def text_translation(request: Request):
    data = await request.json()
    
    text = data.get("text")
    language = data.get("language")
    
    if not text or not language:
        raise HTTPException(status_code=400, detail="Both 'text' and 'language' fields are required.")
    
    # Perform translation
    result = trans_client.translate(text, target_language="en")
    print(f"Translated Text: {result['translatedText']}")
    response = extract_transaction_details(result['translatedText'])
    print(f"Extracted Transaction Details: {response}")
    
    
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