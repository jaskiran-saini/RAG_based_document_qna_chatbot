import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_pdfs
from chunk import chunk_documents
import shutil,os 
def build_vector_store():
    if os.path.exists("./chroma_db"):
        shutil.rmtree("./chroma_db")
    docs=load_pdfs()
    chunks=chunk_documents(docs)
    print("Loading embedding model...")
    model=SentenceTransformer("all-MiniLM-L6-v2")
    texts=[c["text"]for c in chunks]
    print(f"Embedding {len(texts)} chunks...")
    embeddings=model.encode(texts,show_progress_bar=True).tolist()
    client=chromadb.PersistentClient(path="./chroma_db")
    collection=client.get_or_create_collection("docs")
    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=[c["chunk_id"]for c in chunks],
        metadatas=[{"source":c["source"]}for c in chunks]
    )
    print(f"\nStored {collection.count()} chunks in ChromaDB")
    return collection
if __name__=="__main__":
    build_vector_store()