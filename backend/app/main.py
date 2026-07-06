from rag import add_document
from fastapi import UploadFile, File, FastAPI
from pydantic import BaseModel
import io
from pypdf import PdfReader
from llm import ask_llm
app=FastAPI()

class ChatRequest(BaseModel):
    prompt: str
class DocumentRequest(BaseModel):
    text: str

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
@app.post("/ingest")
def ingest_document(request: DocumentRequest):
    add_document(request.text)
    return {
        "message": "Document added successfully."
    }
@app.post("/upload-job-description")
def upload_job_description(file: UploadFile = File(...)):
    pdf_bytes = file.file.read()
    pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    add_document(text)
    return {
        "message": "Job description uploaded and processed successfully."
    }
@app.post("/chat")
def chat(request: ChatRequest):
    answer=ask_llm(request.prompt)
    return {
        "answer": answer
    }
    