# 📄 RAG-Based Document Q&A Chatbot

A Retrieval-Augmented Generation chatbot that answers questions grounded in a set of source PDFs-no hallucinated answers, every response cites which document it came from.

## How it works

1. **Ingestion**-PDFs are parsed and raw text extracted ('pypdf')
2. **Chunking**-text is split into ~800 character overlapping chunks ('langchain-text-splitters') to preserve context across boundaries
3. **Embedding**-each chunk is converted to a 384-dim vector using 'sentence-transformers' ('all-MinLM-L6-v2')
4. **Storage**-vectors are stored in a local persistent vector database ('ChromaDB')
5. **Retrieval**-a user's question is embedded and matched against stored chunks via cosine similarity (top-k)
6. **Generation**-retrieved chunks are passed as context to an LLM (''llama-3.1-8b-instatnt' via Groq), which answers *only* from that context
7. **Citation**-the source document for each answer is tracked and displayed in the UI

## Tech stack

| Component | Tool |
| --- | --- |
| PDF parsing | pypdf |
| Chunking | LangChain text splitters |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector store | ChromaDB |
| LLM | Groq API (Llama 3.1 8B) |
| UI | Streamlit |

## Dataset

Four public-domain/freely available PDFs, covering deliberately varied topics to stress-test retrieval accuracy:
- *Attention Is All You Need* (Vaswani et al.)
- *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (Lewis et al.)
- *Seven Strategies to Prevent Drowning*
- *Crumps*

## Setup

'''bash
git clone https://github.com/jaskiran-saini/RAG_based_document_qna_chatbot 
cd rag-document-qa-chatbot
pip install -r requirements.txt
'''

Create a '.env' file with [Groq API key] (https://console.groq.com/keys):
GROQ_API_KEY=your_key_here
Build the vector store:
'''bash
python embed_store.py
'''

Run the app:
'''bash
streamlit run app.py
'''

## Example

**Q. What are encoder and decoder stacks?***
> The encoder and decoder stacks are composed of a stack of N=6 identical layers. The encoder stack consists of two sub-layers in each layer: a multi-head self-attention mechanism and a position-wise feed-forward network. The decoder stack also consists of two sub-layers, plus a third sub-layer that performs multi-head attention over the encoder's output.
>
> 📎 Sources: Attention is All You Need.pdf

## Known limitations

- **PDF formatting noise**: page numbers, headers, and slide artifacts sometimes leak into chunks (visible in retrieval results as stray numbers/fragments). Doesn't currently break retrieval quality but is a known cleanup oppurtunity.
- **Full rebuild on data changes**: adding/removing PDFs currently requires wiping and rebuilding the entire vector store rather than incrementally updating it-a reasonable trade-off at this dataset size (~600 chunks embed in seconds), but wouldn't scale to a large document set.
- **No conversational memory**: each question is answered independently; follow-up questions referencing earlier turns aren't yet supported.

## Possible extensions
- Hybrid search (BM25+vector) for better keyword-sensitive retrieval
- Cross-encoder re-ranking of retrieved chunks
- RAGAS-based evaluation of retrieval precision and answer faithfulness
- Incremental (non-destructive) vector store updates