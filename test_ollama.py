import ollama

response = ollama.chat(
    model="llama3",
    messages=[{"role":"user","content":"What is machine learning?"}]
)

print(response["message"]["content"])