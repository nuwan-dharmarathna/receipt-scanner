from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
# from models.donut_model import ocr_model
# from models.gpt_model import analyze_receipt
from models.gpt_ocr_model import extract_transaction_details

router = APIRouter()

@router.post("/extract-receipt")
async def extract_receipt(file: UploadFile = File(...)):
    """
    Endpoint to extract transaction details from a receipt image.
    """
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        # Process the image
        result = extract_transaction_details(image_bytes)
        
        return {
        "transactionType": result["transactionType"],
        "amount": result.get("amount", 0),
        "description": result["description"],
        "category": result["category"],
        "date": result.get("date", None),
    }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    