import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

import peakutils
from peakutils.plot import plot as pplot
import numpy as np
import pandas as pd
import os
import sys

videos = []


threshold = 0.5
peak_dist = 120

counts = []
if __name__ == "__main__": 
    for j in range(len(videos)):
        try:
            video_name = "files/counts_csv/" + videos[j]
            df = pd.read_csv(video_name)
            filtered = df[df['confidence'] >= threshold]

            try:
                # Count detections per frame
                detections_per_frame = filtered.groupby('frame').size()
                dearz = detections_per_frame.reindex(range(detections_per_frame.index.max()), fill_value=0).tolist()     
                peaks = peakutils.indexes(np.array(dearz, dtype=int), thres=0, min_dist=peak_dist)
                count = 0
                for i in peaks:
                    count += dearz[i]
            except:
                count = 0
            print('Estimated Count for', videos[j], ":", count)
            
            counts.append(count)
    
            time = [i / 60 for i in range(len(dearz))]
            time_hms = [str(datetime.timedelta(seconds=t)) for t in time]
            
        
            
            time_hms = [t.rstrip('0') for t in time_hms]
            
            # Plot the list of y-values
            plt.plot(time_hms, dearz)
            plt.scatter(np.array(time_hms)[peaks.astype(int)], np.array(dearz)[peaks.astype(int)], color='red', marker='o', label='Deer Detected')
            plt.xticks(range(0, len(time_hms), 12000), time_hms[::12000], rotation=45)  # Rotate x-axis labels for better readability
            plt.legend()
            plt.show()
        except:
            #no += 1
            pass
