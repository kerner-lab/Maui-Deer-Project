from ultralytics import YOLO

model = YOLO("yolo12n.pt")
results = model.tune(data="/home/ahessdun/Dearz13/data.yaml". epochs=30, iterations=20, optimizer="AdamW", workers=0)