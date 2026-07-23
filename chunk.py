from langchain_text_splitters import RecursiveCharacterTextSplitter
from ingest import load_pdfs
def chunk_documents(documents,chunk_size=800,chunk_overlap=100):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n","\n",". "," ",""]
    )
    all_chunks=[]
    for doc in documents:
        chunks=splitter.split_text(doc["text"])
        for i,chunk in enumerate(chunks):
            all_chunks.append({
                "text":chunk,
                "source":doc["filename"],
                "chunk_id":f"{doc['filename']}_chunk{i}"
            })
        print(f"{doc['filename']}:split into {len(chunks)} chunks")
    return all_chunks
if __name__=="__main__":
    docs=load_pdfs()
    chunks=chunk_documents(docs)
    print(f"\nTotal chunks: {len(chunks)}")
    print("\n---Sample chunk---")
    print(chunks[0]["text"][:300])