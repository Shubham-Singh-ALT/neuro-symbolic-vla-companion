import time
import json
import os
import numpy as np
from mss import MSS
from ultralytics import YOLO
import ollama

from game_state import GameState, GameObject

def run_companion_loop():
    print("🤖 Initializing Autonomous VLA Game Companion...")
    
    print("👁️ Loading YOLOv10n weights...")
    vision_model = YOLO("models/yolov10n.pt")
    
    sct = MSS()
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    
    # --- NEW: Short-Term Memory for the AI ---
    last_advice = "None"
    
    print("\n🚀 VLA Companion Loop Active! Press Ctrl+C in terminal to stop.\n")
    
    try:
        while True:
            loop_start = time.time()
            
            # --- PERCEPTION ---
            raw_frame = np.array(sct.grab(monitor))
            frame_rgb = raw_frame[:, :, :3]
            
            results = vision_model(frame_rgb, verbose=False)
            detections = []
            
            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    label = vision_model.names[cls_id]
                    conf = float(box.conf[0])
                    detections.append(GameObject(label=label, confidence=conf, box=box.xyxy[0].tolist()))

            # --- SYMBOLIC LOGIC ---
            game_state = GameState(
                timestamp=time.time(),
                player_health_estimated=20, 
                detected_objects=detections
            )
            game_state.evaluate_threat()
            
            print(f"[{time.strftime('%H:%M:%S')}] Threat: {game_state.threat_level} | Objects Detected: {len(game_state.detected_objects)}")
            
            # --- COGNITION & VOICE ---
            if game_state.threat_level == "Critical":
                
                # --- NEW: Extract all unique object labels to give the AI environmental context ---
                visible_labels = list(set([obj.label for obj in game_state.detected_objects]))
                
                prompt_data = {
                    "health": game_state.player_health_estimated,
                    "enemies": len([obj for obj in game_state.detected_objects if obj.label in ['person', 'enemy']]),
                    "surroundings": visible_labels 
                }
                
                print("🧠 LLM is thinking...")
                response = ollama.chat(
                    model='phi3:mini',
                    messages=[{
                        'role': 'system',
                        'content': f'Tactical game AI. Give advice in max 8 words. DO NOT repeat your previous advice: "{last_advice}". Use the surroundings in your strategy if helpful. No punctuation.'
                    }, {
                        'role': 'user',
                        'content': f"Situation: {json.dumps(prompt_data)}. Action?"
                    }],
                    options={'temperature': 0.8} # <--- NEW: Higher temperature makes the AI more creative
                )
                
                advice = response['message']['content'].strip().replace('"', '').replace("'", "").replace('\n', ' ')
                print(f"💡 Advice: {advice}")
                
                # --- NEW: Update the memory so it remembers this for the next loop ---
                last_advice = advice
                
                try:
                    os.system(f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{advice}\')"')
                except Exception as e:
                    print(f"⚠️ Voice Engine warning: {e}")
                
                time.sleep(2)

            elapsed = time.time() - loop_start
            time.sleep(max(0, 1.0 - elapsed))
            
    except KeyboardInterrupt:
        print("\n🛑 VLA Companion shut down safely.")

if __name__ == "__main__":
    run_companion_loop()