# 🤖 AI ChatBot with Memory using Google Gemini & Streamlit

Welcome to the **AI ChatBot Project**! This project demonstrates how to build a conversational AI chatbot using **Google's Gemini API** with a memory feature using **Streamlit** for the UI.

> 💡 **Goal:** Help you learn how to integrate LLMs like Google Gemini into Python applications, maintain chat memory, and build interactive web interfaces.

---

## 📚 Features

* ✅ Uses **Google Gemini Pro** for answering questions.
* 💬 Maintains full **chat history (memory)** using session state.
* 🌐 Interactive **web-based UI** using Streamlit.
* 📦 Simple, readable code – perfect for learning and expanding.

---

## 🛠️ Technologies Used

| Technology             | Purpose                           |
| ---------------------- | --------------------------------- |
| `Streamlit`            | Web UI for the chatbot            |
| `google-generativeai`  | API access to Gemini LLM          |
| `LangChain` (optional) | For chat message history tracking |

---

## 📄 Code Structure Explained

### 1. **Imports and Setup**

```python
import streamlit as st
import google.generativeai as genai
from langchain_community.chat_message_histories import ChatMessageHistory
```

* `streamlit`: used to create a simple UI.
* `google.generativeai`: Google's SDK to access Gemini Pro.
* `ChatMessageHistory`: manages chat memory (can be replaced by a simple list).

---

### 2. **Model Initialization**

```python
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.0-flash")
```

* `genai.configure`: sets your API key.
* `GenerativeModel`: loads the Gemini model.

---

### 3. **Session-based Memory Initialization**

```python
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()
```

* Keeps all messages (user + AI) in session memory.
* Used to maintain continuity in conversation.

---

### 4. **AI Chat Function**

```python
def run_chain(question):
    chat_history_text = "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages])
    prompt_text = f"Given the chat history:\n{chat_history_text}\nAnswer the question: {question}"

    response = model.generate_content(prompt_text)
    ai_response = response.text

    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(ai_response)

    return ai_response
```

* Converts chat history into a readable format.
* Sends this history + question to Gemini.
* Adds both the new question and AI’s response to memory.

---

### 5. **Streamlit UI Logic**

```python
st.title("AI ChatBot with Google Gemini")
st.write("Ask me anything!")

user_input = st.text_input("Your Question:")
if user_input:
    response = run_chain(user_input)
    st.write(f"**You:** {user_input}")
    st.write(f"**AI:** {response}")
```

* Displays a text input field for the user.
* On submission, calls `run_chain()` and shows the response.

---

### 6. **Chat History Display**

```python
st.subheader("Chat History")
for msg in st.session_state.chat_history.messages:
    st.write(f"**{msg.type.capitalize()}**: {msg.content}")
```

* Loops through stored messages and prints them.

---

## 🚀 Running the Project

### 1. Install dependencies

```bash
pip install streamlit google-generativeai langchain
```

### 2. Set your API key

```python
genai.configure(api_key="your_api_key")
```

Or create a `.env` file and load it securely (with `python-dotenv`).

### 3. Run the app

```bash
streamlit run ChatBot.py
```

---

## 🧩 Example Prompt to Gemini

```
Given the chat history:
User: What's AI?
AI: AI stands for Artificial Intelligence...
User: Can it be dangerous?

Answer the question: What are some uses of AI?
```

This format helps Gemini give smarter, context-aware answers.

---

## ✅ Potential Improvements

* Add **streamed responses** for more dynamic UX.
* Replace `LangChain` with a simple list if you want minimal dependencies.
* Deploy on **Streamlit Cloud**, **Render**, or **Railway**.

---

## 📄 License

MIT License – Free to use, modify, and share.

---

## 🌟 Star the Repo

If this helped you learn, please ⭐ the repo and share it with others!
