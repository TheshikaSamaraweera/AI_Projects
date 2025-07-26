import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
import streamlit as st
from bs4 import BeautifulSoup
import requests

# Configure Gemini
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-2.0-flash")

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
        return text[:2000]  # Limit to 2000 characters
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

# Function to summarize content using AI
def summarize_content(content):
    prompt = f"Summarize the following content:\n\n{content[:1000]}"
    response = model.generate_content(prompt)
    return response.text

# Streamlit web UI
st.title("Web Scraping Bot")
st.write("Enter a website URL to get a summarized version")

url = st.text_input("Website URL")

if url:
    content = scrape_web_content(url)

    if "Failed" in content or "Error" in content:
        st.error(content)
    else:
        summary = summarize_content(content)
        st.subheader("Web Summary")
        st.write(summary)
