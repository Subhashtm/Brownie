from fastapi import FastAPI

app = FastAPI(title="Test App")

@app.get("/")
async def read_root():
    return {"message": "Test app is working"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)