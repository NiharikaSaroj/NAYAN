from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi import HTTPException
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    service: str

from app.services.pipeline import ask_question
from app.services.pipeline import generate_quiz_from_question

app = FastAPI(title="NAYAN API")

# Allow frontend/Electron to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        description="Student question"
    )


class QuizRequest(BaseModel):
    question: str = Field(
        min_length=1,
        description="Topic for quiz generation"
    )


@app.get("/")
def home():
    return {"message": "Welcome to NAYAN"}


@app.get("/health")
def health():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "NAYAN Backend"
    }


@app.post("/ask")
def ask(request: QuestionRequest):
    """
    Answer a student's question using the NCERT knowledge base.
    Falls back to general knowledge if needed.
    """
    try:
        return ask_question(request.question)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="The AI service is temporarily unavailable..."
        )


@app.post("/quiz")
def quiz(request: QuizRequest):
    """
    Generate a quiz from the retrieved NCERT context.
    """
    try:
        return generate_quiz_from_question(request.question)

    except Exception as e:
        print(e)

        raise HTTPException(
            status_code=500,
            detail="The AI service is temporarily unavailable. Please try again in a few moments."
        )