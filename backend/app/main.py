from backend.app.rag import add_document
from fastapi import UploadFile, File, FastAPI
from pydantic import BaseModel
from backend.app.rag import retrieve_documents
import io
import storage
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

    text = request.text.strip()

    if len(text) < 200:
        return {
            "error": "Please provide a complete Job Description (minimum 200 characters)."
        }

    add_document(text)

    return {
        "message": "Job Description uploaded successfully."
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
@app.post("/upload-resume")
def upload_resume(file: UploadFile = File(...)):
    pdf_bytes = file.file.read()
    pdf_reader = PdfReader(io.BytesIO(pdf_bytes))

    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    storage.resume_text = text

    return {
        "message": "Resume uploaded successfully!"
    }
@app.post("/chat")
def chat(request: ChatRequest):

    docs = retrieve_documents(request.prompt)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an AI assistant that answers questions ONLY using the uploaded Job Description.

If the answer is not available in the Job Description, say:

"I couldn't find that information in the uploaded Job Description."

Job Description:
{context}

Question:
{request.prompt}

Answer:
"""

    answer = ask_llm(prompt)

    return {
        "answer": answer
    }
@app.post("/analyze-resume")
def analyze_resume():
    resume = storage.resume_text

    if not resume:
        return {
            "error": "Resume not uploaded yet"
        }

    context_docs = retrieve_documents("job requirements skills responsibilities")
    context = "\n".join([doc.page_content for doc in context_docs])
    prompt = f"""
You are an ATS Resume Analyzer.

Return ONLY in the following format:

Match Score: <percentage>

Matching Skills:
- skill 1
- skill 2

Missing Skills:
- skill 1
- skill 2

Suggestions:
- suggestion 1
- suggestion 2

Final Verdict:
- one short paragraph

Do NOT add extra sections.
Do NOT repeat information.
Keep it concise and structured.

Job Description:
{context}

Resume:
{resume}
"""

    result = ask_llm(prompt)

    return {
        "analysis": result
}
