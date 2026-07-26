import chromadb
from sentence_transformers import SentenceTransformer
def query_docs(question,top_k=3):
    client=chromadb.PersistentClient(path="./chroma_db")
    collection=client.get_collection("docs")
    model=SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding=model.encode([question]).tolist()
    results=collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    print(f"\nQuestion: {question}\n")
    for i,(doc,meta) in enumerate(zip(results["documents"][0],results["metadatas"][0])):
        print(f"---Result {i+1} (source: {meta['source']})---")
        print(doc[:300])
        print()
    return results
if __name__=="__main__":
    query_docs("What are encoder and decoder stacks?")