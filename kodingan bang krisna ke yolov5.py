import cv2
import torch
import numpy as np
import pathlib
from pathlib import Path
import serial
import time
from PIL import Image

# Manually add the parent directory to sys.path
import sys
# sys.path.append(str(Path(__file__).resolve().parent.parent))  # Adjust the path as per your project structure
sys.path.append(str(Path(__file__).resolve().parent.parent))
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_boxes
from utils.plots import Annotator, colors
from utils.torch_utils import select_device

# Establish serial connection with Arduino
ser = serial.Serial('COM9', 9600)  # Adjust 'COM6' to your Arduino's port

def send_to_arduino(data):
    ser.write(data.encode())

# Load YOLOv5 model
weights = 'best.pt'  # Path to YOLOv5 weights file
device = select_device('0' if torch.cuda.is_available() else 'cpu')
model = attempt_load(weights)

# Load class labels from obj.names file
classes = []
obj_names_path = "path/to/obj.names"  # Update with the correct path to your obj.names file
try:
    with open(obj_names_path) as f:
        classes = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    print(f"Error: File '{obj_names_path}' not found.")


# Initialize video capture
cap = cv2.VideoCapture(0)

# Inference Loop
try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Preprocess the frame
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = torch.from_numpy(img).to(device)
        img = img.permute(2, 0, 1).float()  # HWC to CHW
        img /= 255.0  # Normalize to [0, 1]
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        pred = model(img, augment=False)[0]
        pred = non_max_suppression(pred, 0.25, 0.45, classes=None, agnostic=False)
        
        # Process detections
        for det in pred:  # detections per image
            im0 = frame.copy()
            annotator = Annotator(im0, line_width=2, pil=False)
            if len(det):
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], frame.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    label = f'{classes[int(cls)]} {conf:.2f}'
                    annotator.box_label(xyxy, label, color=colors(int(cls), True))

                    # Calculate centroid
                    x_center = int((xyxy[0] + xyxy[2]) / 2)
                    y_center = int((xyxy[1] + xyxy[3]) / 2)
                    Sx = 0
                    Sy = 0
                    inputX = '0'
                    
                    if x_center > 320:
                        if y_center >= 240:
                            Sx = int(-((630 * (x_center)) / 640))
                            Sy = int(-((530 * (y_center) / 480)))
                            if Sx and Sy:
                                inputX = '1'
                        if y_center < 240:
                            Sx = int(((630 * (x_center)) / 640))
                            Sy = int(((530 * (y_center) / 480)))
                            if Sx and Sy:
                                inputX = '1'
                    if x_center <= 320:
                        if y_center >= 240:
                            Sx = int(-((630 * (x_center)) / 640))
                            Sy = int(-((530 * (y_center) / 480)))
                            if Sx and Sy:
                                inputX = '1'
                        if y_center < 240:
                            Sx = int(((630 * (x_center)) / 640))
                            Sy = int(((530 * (y_center) / 480)))
                            if Sx and Sy:
                                inputX = '1'

                    # Display centroid coordinates
                    centroid_text = f'({x_center}, {y_center})'
                    cv2.putText(im0, centroid_text, (x_center, y_center - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Draw centroid
                    cv2.circle(im0, (x_center, y_center), 5, (0, 255, 0), -1)
                    
                    # Send data to Arduino
                    send_to_arduino(f"{Sx} {Sy} {inputX}\n")

            im0 = annotator.result()

        # Display the resulting frame outside the object detection loop
        cv2.imshow('YOLOv5', im0)
        # Exit condition when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            raise KeyboardInterrupt  # Raise KeyboardInterrupt to exit the loop

except KeyboardInterrupt:
    pass  # Handle KeyboardInterrupt by doing nothing

# Release resources
ser.close()
cap.release()
cv2.destroyAllWindows()
