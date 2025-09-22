import cv2
from ultralytics import YOLO

yolo detect train data=ai/dataset/data.yaml model=yolov8n.pt epochs=50 imgsz=640
