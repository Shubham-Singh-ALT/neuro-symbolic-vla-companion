import time
import ollama

print("🧠 Waking up the local AI...")
start = time.time()

response = ollama.chat(
    model='phi3:mini',
    messages=[{
        'role': 'system',
        'content': 'You are a tactical gaming AI. Respond in max 1 sentence.'
    }, {
        'role': 'user',
        'content': 'Health: 15%, Enemies: 3 on right. What is the action?'
    }]
)

elapsed = (time.time() - start) * 1000
print(f"🤖 AI Decision: {response['message']['content'].strip()}")
print(f"⏱️ Thinking Time: {elapsed:.2f} ms")