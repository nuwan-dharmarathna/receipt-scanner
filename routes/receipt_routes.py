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
        "recieptUrl": None,
        "isRecurring": False,
        "recurringInterval": None,
        "nextRecurringDate": None,
        "lastProcessed": None,
        "transactionStatus": "completed"
    }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# @router.post("/process_receipt")
# async def process_receipt(file: UploadFile = File(...)):
#     image = Image.open(file.file).convert("RGB")
#     ocr_result = ocr_model.extract_text(image)
#     gpt_response = await analyze_receipt(ocr_result)
    
#     print(f"GPT Result in Route: {gpt_response}")

#     return {
#         "transactionType": gpt_response["transactionType"],
#         "amount": gpt_response.get("amount", 0),
#         "description": gpt_response["description"],
#         "category": gpt_response["category"],
#         "date": gpt_response.get("date", None),
#         "recieptUrl": None,
#         "isRecurring": False,
#         "recurringInterval": None,
#         "nextRecurringDate": None,
#         "lastProcessed": None,
#         "transactionStatus": "completed"
#     }