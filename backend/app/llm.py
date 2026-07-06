from groq import Groq
from rag import retrieve_documents
from config import GROQ_API_KEY
client=Groq(
    api_key=GROQ_API_KEY
)
def ask_llm(prompt: str):
    docs=retrieve_documents(prompt)
    context = "\n\n".join(
    doc.page_content for doc in docs
    )
    full_prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{prompt}

Answer:
"""
    response= client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": full_prompt
            }
        ]
    )
    return response.choices[0].message.content