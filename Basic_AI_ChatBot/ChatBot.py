import streamlit as st
import google.generativeai as genai
from langchain_community.chat_message_histories import ChatMessageHistory

# Configure Gemini
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-2.0-flash")

# Initialize chat message history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()


def run_chain(question):
    chat_history_text = "\n".join(
        [f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages])
    prompt_text = f"Given the chat history:\n{chat_history_text}\nAnswer the question: {question}"

    response = model.generate_content(prompt_text)
    ai_response = response.text

    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(ai_response)

    return ai_response


# Streamlit UI
st.title("AI ChatBot with Google Gemini")
st.write("Ask me anything!")

user_input = st.text_input("Your Question:")
if user_input:
    response = run_chain(user_input)
    st.write(f"**You:** {user_input}")
    st.write(f"**AI:** {response}")

# Show history
st.subheader("Chat History")
for msg in st.session_state.chat_history.messages:
    st.write(f"**{msg.type.capitalize()}**: {msg.content}")
