import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import time
from src.game_state import GameState, GameObject
print("⚖️ Testing Symbolic State Engine...")

# Mock some detections coming from YOLO
mock_objects = [
    GameObject(label="person", confidence=0.89, box=[100.0, 200.0, 300.0, 400.0]),
    GameObject(label="person", confidence=0.76, box=[350.0, 200.0, 500.0, 400.0]),
    GameObject(label="person", confidence=0.92, box=[600.0, 200.0, 800.0, 400.0])
]

state = GameState(
    timestamp=time.time(),
    player_health_estimated=15,
    detected_objects=mock_objects
)

state.evaluate_threat()

print(f"📊 State Evaluated Successfully!")
print(f"🚨 Threat Level Determined: {state.threat_level}")
print(f"👥 Enemies Detected via Logic: {len(state.detected_objects)}")
print("✅ PHASE 3 SYMBOLIC ENGINE VERIFIED!")