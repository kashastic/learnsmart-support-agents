from pathlib import Path
#from langchain_community.vectorstores import Chroma
#from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DB_DIR = DATA / "vectordb"

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

    # Use a local embedding model served by Ollama
    embeddings = OllamaEmbeddings(model="nomic-embed-text")  # or "all-minilm", "mxbai-embed-large"

    vs = Chroma.from_documents(docs, embeddings, persist_directory=str(DB_DIR))
    vs.persist()
    return vs

def get_kb():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return Chroma(persist_directory=str(DB_DIR), embedding_function=embeddings)

def retrieve(query: str, k: int = 4):
    return get_kb().similarity_search(query, k=k)

if __name__ == "__main__":
    build_kb()
    print("KB built at", DB_DIR)
