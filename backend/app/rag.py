from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
embeddings=HuggingFaceEmbeddings(
    model_name="all-MiniLM-l6-v2",
)
vectorstore=None
def add_document(text: str):
    global vectorstore
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )  
    docs=splitter.create_documents([text])
    vectorstore=FAISS.from_documents(docs, embeddings)
def retrieve_documents(query: str):
    if vectorstore is None:
        return []
    return vectorstore.similarity_search(query, k=3)
    