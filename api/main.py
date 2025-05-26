from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .routes.comics import router as comics_router
from .routes.stories import router as stories_router

app = FastAPI(
    title="Daily Comics API",
    description="API for generating and managing daily comics",
    version="1.0.0"
)

# Include routers
app.include_router(comics_router)
app.include_router(stories_router)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={"message": f"An unexpected error occurred: {str(exc)}"},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 