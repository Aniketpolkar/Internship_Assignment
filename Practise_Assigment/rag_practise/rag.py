import os
import faiss
import numpy as np
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# ---------------------------------------
# Step 1: Setup
# ---------------------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="Simple RAG App", layout="centered")
st.title("📄 PDF Question Answering (RAG)")

# ---------------------------------------
# Step 2: Read PDF
# ---------------------------------------
def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# ---------------------------------------
# Step 3: Chunk text
# ---------------------------------------
def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

# ---------------------------------------
# Step 4: Build vector store
# ---------------------------------------
@st.cache_resource
def build_vector_store(pdf_file):
    text = read_pdf(pdf_file)
    chunks = chunk_text(text)

    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedder.encode(chunks)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    return index, chunks, embedder

# ---------------------------------------
# Step 5: Retrieve context
# ---------------------------------------
def retrieve_context(query, index, chunks, embedder, top_k=3):
    query_embedding = embedder.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    return [chunks[i] for i in indices[0]]

# ---------------------------------------
# Step 6: Gemini model
# ---------------------------------------
model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")

def answer_question(query, index, chunks, embedder):
    context = retrieve_context(query, index, chunks, embedder)

    prompt = f"""
Answer the question using only the context below.

Context:
{''.join(context)}

Question:
{query}
"""

    response = model.generate_content(prompt)
    return response.text

# ---------------------------------------
# Step 7: Streamlit UI
# ---------------------------------------
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    with st.spinner("Processing PDF..."):
        index, chunks, embedder = build_vector_store(uploaded_file)

    query = st.text_input("Ask a question based on the PDF")

    if st.button("Get Answer") and query:
        with st.spinner("Generating answer..."):
            answer = answer_question(query, index, chunks, embedder)
        st.subheader("Answer")
        st.write(answer)
