import google.generativeai as genai
import speech_recognition as sr
from langchain_community.chat_message_histories import ChatMessageHistory
import pyttsx3
from langchain_core.prompts import PromptTemplate
from pyttsx3 import speak

# Configure Gemini
genai.configure(api_key="your key")
model = genai.GenerativeModel("gemini-2.0-flash")

# Initialize chat message history
chat_history = ChatMessageHistory()

#initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 180) # Set speech rate

#speech recognition setup
recognizer = sr.Recognizer()

# Function to speech
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

# AI chat prompt
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="Given the chat history:\n{chat_history}\nAnswer the question: {question}"
)

# Function to run the AI chain
def run_chain(question):
    chat_history_text = "\n".join(
        [f"{msg.type.capitalize()}: {msg.content}" for msg in chat_history.messages])
    prompt_text = prompt.format(chat_history=chat_history_text, question=question)

    response = model.generate_content(prompt_text)
    ai_response = response.text

    chat_history.add_user_message(question)
    chat_history.add_ai_message(ai_response)

    return ai_response

#Main loop
speak("Hello, I am your AI assistant. How can I help you today?")
while True:
    user_input = listen()
    if "exit" in user_input or "quit" in user_input:
        speak("Goodbye!")
        break
    if user_input:
        response = run_chain(user_input)
        print(f"AI: {response}")
        speak(response)