from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.comics import router as comics_router
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Daily Comics API",
    description="API for serving daily comics",
    version="0.1.0"
)

# Include routers
app.include_router(comics_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Daily Comics API!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"An unexpected error occurred: {str(exc)}"},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)