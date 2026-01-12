import ultralytics 
from ultralytics import YOLO
from ultralytics.utils import ThreadingLocked

from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO
import os
import math
import sys
import torch
import pandas as pd

def main(video_name):
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    #Choose model for inference

    #FLIR models
    model = YOLO("dearz13-baseline/weights/best.pt")
    filter_model = YOLO("flir-binary-1/weights/best.pt")

    #Drone models
    #model = YOLO("Dearz-Drone-1-transfer/weights/best.pt")
    #filter_model = YOLO("drone-binary-1/weights/best.pt")
    
    #Specify video path
    #vpath = "/data/hkerner/maui-deer/deer-survey-2024-2025/DEERSURVEY3/Molokai Helicopter/" + video_name
    vpath = video_name

    cap = cv2.VideoCapture(vpath)
  
    #torch.cuda.current_device()
    device = torch.device('cuda')
    model = model.to(device)
    filter_model = filter_model.to(device)
    
    # Define video properties for output video
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    new_fps =  10 
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    print(original_fps)
    
    dw = frame_width
    dh = frame_height
    
    # Define output video writer
    vname = video_name.replace('.mov','')
    #vname = video_name.replace('.MP4','')

    #vname = vname + '_D13_shear5'
    vname = '/scratch/ahessdun/' + vname + '_D13_two-step-test4'
    output_video_name = vname + ".mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
    out = cv2.VideoWriter(output_video_name, fourcc, new_fps, (frame_width, frame_height))
    
    output_label_dir = "output/labels" #os.path.join("output/labels", f'frame_{frame_number}.txt')
    output_image_dir = "output/images"
    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)
    
    dearz = []
    
    
    i = 0
    frame_count = 0

    results_log = []

    # Decorate the predict method to make it thread-safe
    @ThreadingLocked()
    def thread_safe_predict(image):
        """Thread-safe prediction using a shared model instance."""
        results = model.track(image, persist=True, iou = 0.25, conf = 0.1, show_conf = True, show_labels = True, verbose=False, save_txt=False, save_conf=False)
        return results

    def thread_safe_predict2(image):
        """Thread-safe prediction using a shared model instance."""
        results = filter_model(image, verbose=False)
        return results

    
    while cap.isOpened():
        
        i+=1
        frame_count += 1
    
        if frame_count % 600 == 0:
            print(frame_count)
        
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % int(math.ceil(original_fps / new_fps)) == 0:
            #Define location to write images and labels
            label_file = os.path.join(output_label_dir, f'frame_{i}.txt')
            image_file = os.path.join(output_image_dir, f'frame_{i}.jpg')
        
            #Save the frame
            cv2.imwrite(image_file, frame)
            
            # Perform detection
            #results = model.track(frame, persist=True, iou = 0.25, conf = 0.1, show_conf = True, show_labels = True, verbose=False, save_txt=False, save_conf=False)

            #Binary classifier to predict if deer in frame
            filter_results = thread_safe_predict2(frame)
            if filter_results[0].probs.data[0] > 0.5:
                # Get the boxes and track IDs
                results = thread_safe_predict(frame)
                boxes = results[0].boxes.xywh.cpu()
                        
                labels = results[0].names  # Class labels
                num_detections = len(boxes)
            
                # Visualize the results on the frame
                annotated_frame = results[0].plot()
            
                # Draw bounding boxes and display the number of detections
                for r in results:
                    for box in r.boxes:
                        x, y, w, h = map(float, box.xywh[0])
                        l = int((x - w / 2) * dw)
                        r = int((x + w / 2) * dw)
                        t = int((y - h / 2) * dh)
                        b = int((y + h / 2) * dh)
                        
                        if l < 0:
                          l = 0
                        if r > dw - 1:
                          r = dw - 1
                        if t < 0:
                          t = 0
                        if b > dh - 1:
                          b = dh - 1
                
                        x1 = int(x - w / 2)  # Left
                        y1 = int(y - h / 2)  # Top
                        x2 = int(x + w / 2)  # Right
                        y2 = int(y + h / 2)  # Bottom
                        # Draw bounding box
                        #cv2.rectangle(frame, (int(x), int(y)), (int(w), int(h)), (0, 255, 0), 2)
                        #cv2.rectangle(frame, (int(l), int(t)), (int(r), int(b)), (0, 255, 0), 2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        #f.write(f'{y1} {y2} {x1} {x2} {image_file}\n')
    
                        conf = float(box.conf[0])               # confidence score
                        cls = int(box.cls[0])                   # class index
                        label = model.names[cls]                # class label
        
                        #if label == 'Axis-Deer':
                        #    label = ''
                        text = f"{label} {conf:.2f}"
                        cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                                0.4, (0, 255, 0), 2)
    
                        results_log.append({
                            'frame': frame_count,
                            'class_id': int(cls),
                            'confidence': float(conf),
                        })
            else:
                num_detections = 0
        
            
            # Display the number of detections in the current frame
            cv2.putText(frame, f"Detections: {num_detections}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2)
            
            # Write the frame to output video
            out.write(frame)
        
            #Add dear counts to array
            dearz.append(num_detections)
    
    # Release resources
    cap.release()
    out.release()

    try:
        cv2.destroyAllWindows()
    except cv2.error:
        pass 
        
    torch.cuda.empty_cache()


    counts_file = vname + '.txt'
    #Save per-frame dear values
    with open(counts_file, 'w') as file:
        for number in dearz:
            file.write(f"{number}\n")

    counts_csv = vname + '.csv'
    #Save counts with confidence
    # Save to CSV
    df = pd.DataFrame(results_log)
    df.to_csv(counts_csv, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_video.py <video_name>")
        sys.exit(1)
    main(sys.argv[1])


