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

def ask_gemini(message: str, context: str = "", recommendations: list = None, risk_level: str = "") -> str:
    """
    Sends a message to Gemini. If asset-related and recommendations are available,
    it enhances the context with recommendation explanations.
    """

    try:
        message_lower = message.lower()

        # 🔍 Check if question mentions any recommended asset
        matched_assets = []
        if recommendations:
            for asset in recommendations:
                if asset['Asset'].lower() in message_lower:
                    matched_assets.append(asset)

        #  Build enriched context if matches found
        if matched_assets:
            asset_info = "\n".join(
                f"{a['Asset']}: {a['Explanation']}" for a in matched_assets
            )
            context = f"""You are a helpful financial assistant. The user's risk profile is "{risk_level}".

Here is the context of their recommended assets:
{asset_info}

Now answer the user's question below.
"""
        elif recommendations:
            # Add general asset overview if no asset name matched
            all_assets = "\n".join(
                f"{a['Asset']}: {a['Explanation']}" for a in recommendations
            )
            context = f"""You are a helpful financial assistant. The user's risk profile is "{risk_level}".

These were the recommended assets:
{all_assets}

Now answer the user's question below.
"""

        #  Combine with user message
        prompt = f"{context}\n\nUser: {message}"
        response = chat_session.send_message(prompt)
        return response.text

    except Exception as e:
        return f" Error communicating with Gemini: {str(e)}"
