import cv2
import numpy as np
from ultralytics import YOLO
from mss import MSS

def run_vision_test():
    print("👁️ Loading YOLOv10n Vision Model...")
    model = YOLO("models/yolov10n.pt")
    
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    sct = MSS()

    print("🚀 Running live vision detection loop for 5 seconds (Press 'q' in the window to stop)...")
    
    import time
    start = time.time()
    
    while time.time() - start < 5:
        frame = np.array(sct.grab(monitor))
        
        results = model(frame, verbose=False)
        
        annotated_frame = results[0].plot()
        
        preview = cv2.resize(annotated_frame, (960, 540))
        cv2.imshow("VLA Companion - Vision Perception", preview)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    print("✅ Phase 2 Vision Test Complete!")

if __name__ == "__main__":
    run_vision_test()