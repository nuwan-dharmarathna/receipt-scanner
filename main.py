from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from routes.receipt_routes import router as receipt_router
from routes.text_routes import router as text_router
from routes.gcp_speech_routes import router as gcp_speech_router

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

app = FastAPI()

# Allows CORS from frontend
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Receipt Scanner API"}

# routes
app.include_router(receipt_router, prefix="/api/v1/receipt")
app.include_router(text_router, prefix="/api/v1/text")
app.include_router(gcp_speech_router, prefix="/api/v1/speech")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)