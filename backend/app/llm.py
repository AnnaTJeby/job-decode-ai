from groq import Groq
from rag import retrieve_documents
from config import GROQ_API_KEY
client=Groq(
    api_key=GROQ_API_KEY
)
def ask_llm(prompt: str):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content