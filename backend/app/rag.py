from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

vectorstore = None
embeddings = None

def get_embeddings():
    global embeddings

    if embeddings is None:
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

    return embeddings

def add_document(text: str):
    global vectorstore

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    docs = splitter.create_documents([text])

    vectorstore = FAISS.from_documents(
        docs,
        get_embeddings()     # <-- IMPORTANT
    )

def retrieve_documents(query: str, k=4):
    global vectorstore

    if vectorstore is None:
        raise ValueError("Please upload a Job Description first.")

    return vectorstore.similarity_search(query, k=k)