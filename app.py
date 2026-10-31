import streamlit as st
import os 
from embed_store import build_vector_store 
@st.cache_resource 
def ensure_vector_store():
    if not os.path.exists("./chroma_db"):
        build_vector_store()
ensure_vector_store()
from generate import answer_question
st.set_page_config(page_title="Document Q&A Chatbot",page_icon="📄")
st.title("📄 Document Q&A Chatbot")
st.caption("Ask questions about the document in your knowledge base-answers are grounded in retrieved context, with sources shown.")
if "messages" not in st.session_state:
    st.session_state.messages=[]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
if question:=st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role":"user","content":question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Retrieving and Generating..."):
            answer,sources=answer_question(question)
        st.markdown(answer)
        st.caption(f"📎 Sources:{', '.join(sources)}")
        st.session_state.messages.append({"role":"assistant","content":answer})
        