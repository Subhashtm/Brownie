from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="AniAthu's brownies - Minimal Version")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving
@app.get("/static/{file_path:path}")
async def serve_static(file_path: str):
    """Serve static files from frontend directory"""
    static_file_path = Path("frontend") / file_path
    
    if not static_file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine content type
    content_type = "text/plain"
    if file_path.endswith('.css'):
        content_type = "text/css"
    elif file_path.endswith('.js'):
        content_type = "application/javascript"
    elif file_path.endswith('.html'):
        content_type = "text/html"
    
    return FileResponse(static_file_path, media_type=content_type)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Minimal app is running",
        "environment": {
            "SUPABASE_URL": bool(os.getenv("SUPABASE_URL")),
            "SECRET_KEY": bool(os.getenv("SECRET_KEY"))
        }
    }

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        return FileResponse("frontend/index.html")
    except Exception as e:
        return HTMLResponse(f"<h1>Welcome to AniAthu's brownies</h1><p>Error loading frontend: {e}</p>")

@app.get("/api/test")
async def test_endpoint():
    return {"message": "API is working", "status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)