import os
import faiss
import numpy as np
from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# Step 1: Load environment variablesF
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Step 2: Read PDF
def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

pdf_text = read_pdf("data/sample.pdf")

# Step 3: Chunk text
def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

chunks = chunk_text(pdf_text)

# Step 4: Create embeddings
embedder = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embedder.encode(chunks)

# Step 5: Store embeddings in FAISS
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Step 6: Retrieve relevant chunks
def retrieve_context(query, top_k=3):
    query_embedding = embedder.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    return [chunks[i] for i in indices[0]]

# Step 7: Generate answer using Gemini
model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")

def answer_question(query):
    context = retrieve_context(query)

    prompt = f"""
Answer the question using only the context below.

Context:
{''.join(context)}

Question:
{query}
"""
    response = model.generate_content(prompt)
    return response.text

# Step 8: Ask user questions
while True:
    query = input("Ask a question (type 'exit' to quit): ")
    if query.lower() == "exit":
        break

    answer = answer_question(query)
    print("\nAnswer:\n", answer, "\n")
