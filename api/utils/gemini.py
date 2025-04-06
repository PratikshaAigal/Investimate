import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file for API key

# Configure Gemini
api_key=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-2.0-flash")

# Optional: Keep state between messages
chat_session = model.start_chat(history=[])

def ask_gemini(message: str, context: str = "") -> str:
    """
    Sends a message to Gemini and returns the AI's response.
    Optionally adds user-specific context to the prompt.
    """
    try:
        prompt = f"{context}\n\nUser: {message}"
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return f"❗ Error communicating with Gemini: {str(e)}"
