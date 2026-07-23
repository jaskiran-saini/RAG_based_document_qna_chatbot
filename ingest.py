import os
from pypdf import PdfReader
def load_pdfs(data_dir="data"):
    documents=[]
    for filename in os.listdir(data_dir):
        if filename.endswith(".pdf"):
            path=os.path.join(data_dir,filename)
            reader=PdfReader(path)
            text=""
            for page in reader.pages:
                text+=page.extract_text()+"\n"
            documents.append({"filename":filename,"text":text})
            print(f"Loaded {filename}: {len(text)} characters")
    return documents
if __name__=="__main__":
    docs=load_pdfs()
    print(f"\nTotal documents loaded: {len(docs)}")