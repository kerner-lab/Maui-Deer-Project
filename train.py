from ultralytics import YOLO

model = YOLO("yolo12n.pt") #Specify base model for transfer learning
results = model.train(data="Dearz13/data.yaml", 
                      epochs=300, imgsz=640, workers=1, name='model-name')