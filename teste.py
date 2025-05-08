import requests

# Nome exato do modelo no Ollama
MODEL = "llama3:latest"

# Prompt de teste
prompt = input("🧠 Digite seu prompt: ")

# Payload da requisição
payload = {
    "model": MODEL,
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "stream": False  # Se quiser resposta em tempo real, mude para True
}

try:
    response = requests.post("http://localhost:11434/api/chat", json=payload)
    response.raise_for_status()
    resultado = response.json()
    print("\n🤖 Resposta do modelo:")
    print(resultado["message"]["content"])

except requests.exceptions.RequestException as e:
    print(f"❌ Erro ao conectar com o Ollama: {e}")
