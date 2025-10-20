#Plot peaks (with adjustable confidence values)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

import peakutils
from peakutils.plot import plot as pplot
import numpy as np

def mae(y_true, predictions):
    y_true, predictions = np.array(y_true), np.array(predictions)
    return np.mean(np.abs(y_true - predictions))

videos = ['Central Maui 4_Mahi Pono 4 Colton Loque', '11_29_23 Survey 2_SouthMaui1', 'Lanaihale_Guided Hunting_CGMA Unit 3',
          'Kanaio_Kahikinui_Kipahulu 4', 'Lanai Pulama Rifle A1 & A2', 
          'Lanai Pulama Rifle B_Archery 1_Shotgun 1', 'Lanai CGMA Unit 2', "South Maui 3 Colton Loque",
          '11_22_23 Survey 1_CentralMaui2MahiPono2', '11_29_23 Survey 1_CentralMauiCleanUp',
          'Molokai Ranch South', 'East Maui 1', 'Kanaio_Kahikinui_Kipahulu 1', 'Kanaio_Kahikinui_Kipahulu 3',
          'South Maui 2 Colton Loque', 'Hana 1', 'Hana 2', 'West Maui 1', 'West Maui 2',
          'Upcountry Maui 1 Colton Loque', 'Upcountry Maui 2 Colton Loque', '10_30_23 Survey KaonaoluDHHLWaiohuli', 'Kanaio_Kahikinui_Kipahulu 2',
          '11_17_23 Survey 1_CentralMaui1MahiPono1', 'Central Maui 3_Mahi Pono 3 Colton Loque', 'Wailau Valley', 'Kalaupapa', 'Hanaula 1 Colton Loque', 'Guided Hunting_CGMA Unit 1&3_Pulama Rifle C']

DLNR_Counts = [1772, 2469, 1107, 
               202, 69,
               489, 202, 324,
               1421, 411,
               988, 211, 3113, 40,
               5346, 8, 4, 4, 7,
               689, 1146, 1950, 0,
               266, 1262, 14, 500, 340, 815]

#Choose desired confidence threshold
threshold = 0.5

#Define file names

#video_name = videos[j] + '_D9' + '.csv'
#video_name = videos[j] + '_D9_cls3_dfl1p5' + '.csv'
#video_name = videos[j] + '_D10' + '.csv'
#video_name = videos[j] + '_D11_yolo12' + '.csv'
video_name = videos[j] + '_D12_part' + '.csv'
#video_name = videos[j] + '_D13_hyp' + '.csv'

counts = []
DLNR_Counts_valid = []
video_name_list = []

for j in range(len(videos)):
    #if 'lanai' in videos[j].lower() or 'cgma' in videos[j].lower():
    #if 'molokai' in videos[j].lower():
    #if not ('lanai' in videos[j].lower() or 'cgma' in videos[j].lower()):
    #if not ('south maui 2' in videos[j].lower()):
    #if 'south maui 2' in videos[j].lower() or 'southmaui1' in videos[j].lower() or 'centralmaui2' in videos[j].lower() or 'ranch south' in videos[j].lower() or 'cleanup' in videos[j].lower():
        try:

            #print(video_name)
            df = pd.read_csv(video_name)
            #print(df)
    
            # Apply a new confidence threshold
            threshold = 0.5
            filtered = df[df['confidence'] >= threshold]
            
            # Count detections per frame
            detections_per_frame = filtered.groupby('frame').size()
            dearz = detections_per_frame.reindex(range(detections_per_frame.index.max()), fill_value=0).tolist()
                
            peaks = peakutils.indexes(np.array(dearz, dtype=int), thres=0, min_dist=120)
            count = 0
            for i in peaks:
                count += dearz[i]
                
            counts.append(count)
            DLNR_Counts_valid.append(DLNR_Counts[j])
            video_name_list.append(videos[j])

            
            print(videos[j], '\n')
            print('Estimated Count:', count)
            print('DLNR Count:', DLNR_Counts[j])
    
            time = [i / 60 for i in range(len(dearz))]
            time_hms = [str(datetime.timedelta(seconds=t)) for t in time]
            
            
            #Extract part of lists
            n = len(dearz)
            quarter_length = n // 4
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