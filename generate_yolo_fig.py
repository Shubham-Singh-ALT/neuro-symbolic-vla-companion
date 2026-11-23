import cv2
from ultralytics import YOLO

# Load model and run inference on the image
model = YOLO("models/yolov10n.pt")
image_path = "gameplay_sample.png"
results = model(image_path)

# Render bounding boxes onto the frame
annotated_frame = results[0].plot()

# Save output image for LaTeX research paper
cv2.imwrite("fig_yolo.png", annotated_frame)
print("✅ Saved fig_yolo.png successfully!")