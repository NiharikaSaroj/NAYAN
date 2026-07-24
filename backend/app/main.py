from fastapi import FastAPI

app = FastAPI(
    title="NAYAN API",
    description="AI-powered Voice Assistant for Visually Impaired Students",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to NAYAN API 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "NAYAN Backend"
    }