import requests
from bs4 import BeautifulSoup
import streamlit as st
import numpy as np
import faiss

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain.schema import Document
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-2.0-flash")

# Load HuggingFace embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize FAISS index
index = faiss.IndexFlatL2(384)
stored_docs = []  # To keep track of chunks

# Function to scrape web content
def scrape_web_content(url):
    try:
        st.write(f"Scraping content from: {url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/58.0.3029.110"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"Failed to fetch {url}"
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([para.get_text() for para in paragraphs])
        return text[:5000]
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

# Store scraped content in FAISS
def store_content_in_vector_store(content, url):
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_text(content)
    documents = [Document(page_content=chunk, metadata={"source": url}) for chunk in chunks]
    vectors = embeddings.embed_documents([doc.page_content for doc in documents])
    for i, vector in enumerate(vectors):
        index.add(np.array([vector], dtype=np.float32))
        stored_docs.append(documents[i])
    return "Data saved successfully"

# Retrieve and answer based on query
def retrieve_relevant_chunks(query):
    query_vector = np.array(embeddings.embed_query(query), dtype=np.float32).reshape(1, -1)
    D, I = index.search(query_vector, k=5)
    context = ""
    for idx in I[0]:
        if idx < len(stored_docs):
            context += stored_docs[idx].page_content + "\n\n"

    if not context:
        return "No relevant content found."

    prompt = f"Based on the following context, answer the question:\n\n{context}\n\nQuestion: {query}\nAnswer:"
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("Web Scraping + RAG Bot")
url = st.text_input("Enter a website URL")

if url:
    content = scrape_web_content(url)
    if "Failed" in content or "Error" in content:
        st.error(content)
    else:
        msg = store_content_in_vector_store(content, url)
        st.success(msg)

query = st.text_input("Ask a question about the scraped content")

if query:
    if not stored_docs:
        st.error("No data available. Please scrape a website first.")
    else:
        answer = retrieve_relevant_chunks(query)
        st.subheader("Answer")
        st.write(answer)
