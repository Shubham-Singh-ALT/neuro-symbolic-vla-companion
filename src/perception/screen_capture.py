import time
import numpy as np
from mss import MSS
def benchmark_capture(duration_sec=5):
    # Captures the primary monitor (1920x1080)
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    sct = MSS()
    frame_count = 0
    start_time = time.time()

    print(f"⚡ Testing Screen Capture Speed for {duration_sec} seconds...")
    
    while time.time() - start_time < duration_sec:
        # Grab raw screen pixels
        sct_img = sct.grab(monitor)
        # Convert to numpy array so OpenCV/YOLO can read it later
        frame = np.array(sct_img)
        frame_count += 1

    elapsed = time.time() - start_time
    fps = frame_count / elapsed
    latency_ms = (elapsed / frame_count) * 1000

    print("\n✅ Screen Capture Benchmark Complete!")
    print(f"📊 Total Frames Captured: {frame_count}")
    print(f"🚀 Average Speed: {fps:.2f} FPS")
    print(f"⏱️ Average Latency per Frame: {latency_ms:.2f} ms")

if __name__ == "__main__":
    benchmark_capture()