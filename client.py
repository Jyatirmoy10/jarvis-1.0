import ollama  # pip install ollama

# Initialize Ollama client (default local host)
client = ollama.Client(host="http://localhost:11434")

response = client.chat(
    model="llama3",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
        {"role": "user", "content": "what is coding"}
    ]
)

print(response['message']['content'])
