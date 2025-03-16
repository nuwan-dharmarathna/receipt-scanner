from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from routes.receipt_routes import router as receipt_router
from routes.whisper_routes import router as whisper_router
from routes.text_routes import router as text_router

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Receipt Scanner API"}

# routes
app.include_router(receipt_router, prefix="/api/v1/receipt")
app.include_router(whisper_router, prefix="/api/v1/voice")
app.include_router(text_router, prefix="/api/v1/text")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)