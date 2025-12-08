#Create time graph
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import cv2
import os

#Define path of annotated video, file containing per-frame counts, and name/path for the outpuy video

video_name = "video name"
count_file = "count file"
output_video_path = "output path"

#Load per-frame dear values
with open(count_file, 'r') as file:
    # Read all lines, strip the newline characters, and convert each line to an integer
    dearz = [int(line.strip()) for line in file]
len(dearz)

time = [i / 10 for i in range(len(dearz))]
time_hms = [t.rstrip('0') for t in time_hms]

# Plot the list of y-values
plt.plot(time_hms, dearz, linewidth=0.3)
plt.xticks(range(0, len(time_hms), 2000), time_hms[::2000], rotation=45)  # Rotate x-axis labels for better readability


plt.savefig("output_with_boxes.png")
plt.close()

cap = cv2.VideoCapture(video_name)


# Get video properties for output video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Define output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

output_label_dir = "output/labels"
output_image_dir = "output/images"
os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_label_dir, exist_ok=True)


# Read the saved graph image
graph = cv2.imread("output_with_boxes.png")
graph_height, graph_width, _ = graph.shape

print(graph_height, graph_width)
#New resizing code
graph_height = int(graph_height * 0.6)
graph_width = int(graph_width * 0.6)
graph = cv2.resize(graph, (graph_width, graph_height))
i = 0
frame_num = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if i < len(dearz) - 1:
    
        top_left_x = frame_width - graph_width - 10  # 10px padding from the right edge
        top_left_y = 10  # 10px padding from the top edge
        
        graph_with_dot = graph.copy()
    
        #General:
        x_scale = 1.56 * 175/ len(dearz)
        x_offset = 60 / x_scale
    
        y_scale = 1.95 * 100 / max(dearz)
        y_offset = 245.7 / y_scale
        
        graph_with_dot = cv2.circle(graph_with_dot, (int(x_scale*(i+ x_offset)), int(y_scale*(y_offset - dearz[i]))), 2, (0, 0, 255), -1)
            
        frame[top_left_y:top_left_y+graph_height, top_left_x:top_left_x+graph_width] = graph_with_dot
        out.write(frame)
    
        print('Frame:', i)
        i+=1
    frame_num+=1

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
