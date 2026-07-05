from fastapi import FastAPI
from pydantic import BaseModel
from llm import ask_llm
app=FastAPI()

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {
        "message": "Welcome to JobDecode AI Backend!"
    }
@app.get("/hello")
def hello():
    return {
        "message": "Hello from FastAPI!"
    }
@app.post("/chat")
def chat(request: ChatRequest):
    answer=ask_llm(request.prompt)
    return {
        "answer": answer
    }
    