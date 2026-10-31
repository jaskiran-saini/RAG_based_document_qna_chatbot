import os
from dotenv import load_dotenv
from groq import Groq
from query import query_docs

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def answer_question(question, top_k=3):
    results = query_docs(question, top_k=top_k)
    chunks = results["documents"][0]
    sources = [meta["source"] for meta in results["metadatas"][0]]

    context = "\n\n".join(chunks)

    prompt = f"""Answer the question using ONLY the context below. If the answer isn't in the context, say "I don't have enough information to answer this."

Context:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    answer = response.choices[0].message.content
    print(f"\nAnswer: {answer}")
    print(f"\nSources: {set(sources)}")
    return answer,set(sources) 


if __name__ == "__main__":
    answer_question("What are encoder and decoder stacks?")