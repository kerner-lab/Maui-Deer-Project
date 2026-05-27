from datetime import date
from tqdm import tqdm
from ultralytics import YOLO
from ultralytics.utils import ThreadingLocked
from pathlib import Path
from time import sleep

import math
import numpy as np
import os
import sys
import torch
import cv2
import peakutils

def main(video_name, filter_model_name="flir-binary-1", detect_model_name="dearz13-baseline", log_path=None, draw_bboxes="y"):
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    device = torch.device('cuda')
    filter_model = YOLO(f"{filter_model_name}/weights/best.pt").to(device)
    model = YOLO(f"{detect_model_name}/weights/best.pt").to(device)

    video_capture = cv2.VideoCapture(video_name)
    total_frames =  int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    width =         int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height =        int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    original_fps =  video_capture.get(cv2.CAP_PROP_FPS)

    out_name = video_name.replace('.mov','').replace('.mp4','').replace('.MP4', '') + '_counts'
    new_fps =  10
    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # Codec for .mp4 files on web
    out_video = cv2.VideoWriter(out_name + ".mp4", fourcc, new_fps, (width, height))        
    @ThreadingLocked()
    def thread_safe_predict(image):
        return model.track(image, persist=True, iou = 0.25, conf = 0.1, show_conf = True, show_labels = True, verbose=False, save_txt=False, save_conf=False)

    @ThreadingLocked()
    def thread_safe_predict2(image):
        return filter_model(image, verbose=False)
    
    check_every_n_frame = int(math.ceil(original_fps / new_fps))
    i = 0
    deer_counts = []
    deer_counts_confident = []
    max_desc_length = 110
    if log_path:
        log_file = open(log_path, 'w', encoding="utf-8")
        pbar = tqdm(total=total_frames, desc=video_name[-max_desc_length:], file=log_file)
    else:
        pbar = tqdm(total=total_frames, desc=video_name[-max_desc_length:])

    while video_capture.isOpened():
        i += 1
        pbar.update(1)
        success, frame = video_capture.read()
        if not success:
            break
        if i % check_every_n_frame != 0:
            continue
        num_detections = 0
        num_detections_confident = 0
        deer_in_frame_out = thread_safe_predict2(frame)
        deer_in_frame = deer_in_frame_out[0].probs.data[0] > 0.5
        if deer_in_frame:
            results = thread_safe_predict(frame)
            num_detections = len(results[0].boxes.xywh.cpu())
            for r in results:
                for box in r.boxes:
                    x, y, w, h = map(float, box.xywh[0])
                    confidence_score = float(box.conf[0])  
                    if confidence_score > 0.5:
                        num_detections_confident += 1
                    
                    if draw_bboxes == "y":
                        x1, x2 = int(x - w / 2), int(x + w / 2)
                        y1, y2 = int(y - h / 2), int(y + h / 2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)      
                        class_index = int(box.cls[0])                 
                        class_label = model.names[class_index]                
                        text = f"{class_label} {confidence_score:.2f}"
                        cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
        
        cv2.putText(frame, f"Detections: {num_detections}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 2)
        out_video.write(frame)
        deer_counts.append(num_detections)
        deer_counts_confident.append(num_detections_confident)

    deer_counts_np = np.array(deer_counts)
    deer_counts_confident_np = np.array(deer_counts_confident)
    deer_counts_peak_indices = peakutils.indexes(deer_counts_np, thres=0, min_dist=120)
    deer_counts_confident_peak_indices = peakutils.indexes(deer_counts_confident_np, thres=0, min_dist=120)

    estimate_range_min = sum(deer_counts_confident_np[deer_counts_confident_peak_indices].tolist())
    estimate_range_max = sum(deer_counts_np[deer_counts_peak_indices].tolist())
    estimates_str = f"{estimate_range_min}" if (estimate_range_min == estimate_range_max) else f"{estimate_range_min}-{estimate_range_max}"

    pbar.set_postfix(deer_estimates=f"{estimates_str}")
    
    video_capture.release()
    out_video.release()
    torch.cuda.empty_cache()
    try:
        cv2.destroyAllWindows()
    except cv2.error:
        pass 

    with open(f"template.html", "r", encoding="utf-8") as f:
        html_template = f.read()
    
    html_file = html_template \
        .replace("<<DATE>>", f"{date.today()}") \
        .replace("<<MODEL>>", detect_model_name) \
        .replace("<<COUNTS>>", f"{deer_counts}") \
        .replace("<<ESTIMATE>>", f"{estimate_range_max}") \
        .replace("<<PEAKS>>", f"{deer_counts_peak_indices.tolist()}")
    
    with open(f"{out_name}.html", "w", encoding="utf-8") as f:
        f.write(html_file)
    pbar.set_description(f"{out_name[-max_desc_length:]}.html")
    pbar.close()

if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(filter_model_name=sys.argv[1], detect_model_name=sys.argv[2], video_name=sys.argv[3])
    elif len(sys.argv) == 5:
        main(filter_model_name=sys.argv[1], detect_model_name=sys.argv[2], video_name=sys.argv[3], log_path=sys.argv[4])
    elif len(sys.argv) == 6:
        main(filter_model_name=sys.argv[1], detect_model_name=sys.argv[2], video_name=sys.argv[3], log_path=sys.argv[4], draw_bboxes=sys.argv[5])

    else:
        print("Usage:       python Inference2.py <filter_model> <detect_model> <video_name>")
        print("HELICOPTER:  python Inference2.py flir-binary-1 dearz13-baseline <video_name>")
        print("DRONE:       python Inference2.py drone-binary-1 Dearz-Drone-1-transfer <video_name>")
    sys.exit(1)

