# client.py
from dotenv import load_dotenv
import os
import ollama
import sys

# Load environment variables
load_dotenv()

# Get Ollama host, default to local
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Debug info (optional)
print(f"[client.py] Ollama host: {OLLAMA_HOST}", file=sys.stderr)

# Initialize client
client = ollama.Client(host=OLLAMA_HOST)

def ask_jarvis(prompt: str) -> str:
    """Send a prompt to Ollama and return the response."""
    try:
        response = client.chat(
            model="llama3",
            messages=[
                {
                    "role": "system",
                    "content": "You are Jarvis, a helpful voice assistant like Alexa/Google. Keep responses short."
                },
                {"role": "user", "content": prompt}
            ]
        )
        return response.get("message", {}).get("content", "No response.")
    except Exception as e:
        print(f"[client.py] Error: {e}", file=sys.stderr)
        return "Sorry, I couldn't process that."

# Optional: test run
if __name__ == "__main__":
    print(ask_jarvis("What is coding?"))
