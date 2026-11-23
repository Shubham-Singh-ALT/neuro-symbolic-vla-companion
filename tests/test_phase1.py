import time
import yaml
import json
import ollama
from mss import MSS
import numpy as np

print("🚀 Running Phase 1 Integration Test...")

# 1. Test Screen Grab
with MSS() as sct:
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    frame = np.array(sct.grab(monitor))
print(f"1. Screen Frame Captured Successfully! Shape: {frame.shape}")

# 2. Simulated Symbolic Event State
simulated_state = {"health": 15, "enemies_visible": 3, "cover_available": True}
print(f"2. Symbolic State Initialized: {simulated_state}")

# 3. Local LLM Decision Generation
start_llm = time.time()
response = ollama.chat(
    model='phi3:mini',
    messages=[{
        'role': 'system',
        'content': 'Tactical AI Assistant. Respond in under 10 words.'
    }, {
        'role': 'user',
        'content': f"State: {json.dumps(simulated_state)}. What to do?"
    }]
)
llm_time = (time.time() - start_llm) * 1000

print(f"3. Decision Generated in {llm_time:.1f}ms: \"{response['message']['content'].strip()}\"")
print("✅ PHASE 1 COMPLETE: All systems verified and functional!")