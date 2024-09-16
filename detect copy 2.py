import cv2
import torch
import numpy as np
import pathlib
from pathlib import Path
import sys
import serial
import time

from models.common import DetectMultiBackend
from utils.general import (non_max_suppression, scale_boxes)
from utils.plots import Annotator, colors
from utils.torch_utils import select_device

sys.path.append(str(Path(__file__).resolve().parents[0]))
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Establish serial connection with Arduino
ser = serial.Serial('COM9', 9600)  # Adjust 'COM3' to your Arduino's port
time.sleep(2)  # Allow tinfhrtme for the serial connection to initialize

# Load YOLOv5 model and other necessary imports (shown in your previous Python code)
# Initialize camera
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
device = select_device('0' if torch.cuda.is_available() else 'cpu')
model = DetectMultiBackend('best.pt', device=device)

  # Preprocess the frame
img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
img = torch.from_numpy(img).to(device)
img = img.permute(2, 0, 1).float()  # HWC to CHW
img /= 255.0  # Normalize to [0, 1]
if img.ndimension() == 3:
     img = img.unsqueeze(0)
 # Inference
pred = model(img, augment=False)
pred = non_max_suppression(pred, 0.25, 0.45, classes=None, agnostic=False)
# Inference Loop
try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Preprocess the frame and perform inference (as shown in your previous code)

        # Process detections and control laser
        for det in pred:  # detections per image
            im0 = frame.copy()
            annotator = Annotator(im0, line_width=2, pil=not ascii)
            if len(det):
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], frame.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    label = f'{model.names[int(cls)]} {conf:.2f}'
                    annotator.box_label(xyxy, label, color=colors(int(cls), True))

                    # Calculate centroid
                    x_center = int((xyxy[0] + xyxy[2]) / 2)
                    y_center = int((xyxy[1] + xyxy[3]) / 2)

                    # Draw centroid
                    cv2.circle(im0, (x_center, y_center), 5, (0, 255, 0), -1)

            im0 = annotator.result()
                
            # Receive response from Arduino (optional)
            response = ser.readline().decode().strip()
            print("Arduino response:", response)

            cv2.imshow('YOLOv5', im0)
            
            # Exit condition when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                raise KeyboardInterrupt  # Raise KeyboardInterrupt untuk keluar dari loop
except KeyboardInterrupt:
    pass  # Tangani KeyboardInterrupt dengan tidak melakukan apa pun

ser.close()
cap.release()
cv2.destroyAllWindows()
