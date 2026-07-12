from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
embeddings = None

def get_embeddings():
    global embeddings
    if embeddings is None:
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
    return embeddings
vectorstore = None
def add_document(text: str):
    global vectorstore
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )  
    docs=splitter.create_documents([text])
    vectorstore=FAISS.from_documents(docs, embeddings)
def retrieve_documents(query: str, k: int = 4):
    global vectorstore
    if vectorstore is None:
        raise ValueError("Vectorstore is not initialized. Please add documents first.")
    docs=vectorstore.similarity_search(query, k=k)
    return docs
