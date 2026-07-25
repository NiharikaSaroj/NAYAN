from fastapi import FastAPI
from pydantic import BaseModel

from app.services.pipeline import ask_question
from app.services.pipeline import generate_quiz_from_question

app = FastAPI(title="NAYAN API")


class QuestionRequest(BaseModel):
    question: str

class QuizRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "Welcome to NAYAN"}


@app.post("/ask")
def ask(request: QuestionRequest):
    result = ask_question(request.question)
    return result

@app.post("/quiz")
def quiz(request: QuizRequest):
    return generate_quiz_from_question(request.question)