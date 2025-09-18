# app/services/rag.py
from pathlib import Path
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DB_DIR = DATA / "vectordb"
COLLECTION = "learnsmart_kb"

def _load_md():
    texts = []
    for name in ["FAQ.md", "Policy.md", "CourseCatalog.md"]:
        p = DATA / name
        if p.exists():
            texts.append(p.read_text())
    return "\n\n".join(texts)

def build_kb():
    text = _load_md()
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=60)
    docs = splitter.create_documents([text])

    embeddings = OllamaEmbeddings(model="nomic-embed-text")  # or all-minilm / mxbai-embed-large
    # NOTE: langchain-chroma auto-persists when persist_directory is set.
    Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=str(DB_DIR),
        collection_name=COLLECTION,
    )
    return True

def get_kb():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return Chroma(
        persist_directory=str(DB_DIR),
        embedding_function=embeddings,
        collection_name=COLLECTION,
    )

def retrieve(query: str, k: int = 4):
    return get_kb().similarity_search(query, k=k)

if __name__ == "__main__":
    build_kb()
    print("KB built at", DB_DIR)
