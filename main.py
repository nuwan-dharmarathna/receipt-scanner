from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from routes.receipt_routes import router as receipt_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Receipt Scanner API"}

# routes
app.include_router(receipt_router, prefix="/api/v1/receipt")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)