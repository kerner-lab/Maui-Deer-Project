#Loop through conf thresholds
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

import peakutils
from peakutils.plot import plot as pplot
import numpy as np

import matplotlib.pyplot as plt
import math
from sklearn.metrics import r2_score
from matplotlib.ticker import MultipleLocator

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

#Define file names

#video_name = videos[j] + '_D9' + '.csv'
#video_name = videos[j] + '_D9_cls3_dfl1p5' + '.csv'
#video_name = videos[j] + '_D10' + '.csv'
#video_name = videos[j] + '_D11_yolo12' + '.csv'
video_name = videos[j] + '_D12_part' + '.csv'
#video_name = videos[j] + '_D13_hyp' + '.csv'


conf_list = [0.00, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.60, 0.65, 0.70]


for conf_thres in conf_list:
    counts = []
    DLNR_Counts_valid = []
    video_name_list = []
    
    for j in range(len(videos)):
        #if 'lanai' in videos[j].lower() or 'cgma' in videos[j].lower():
        #if 'molokai' in videos[j].lower():
        #if not ('lanai' in videos[j].lower() or 'cgma' in videos[j].lower()):
        #if not ('south maui 2' in videos[j].lower() or 'south maui 3' in videos[j].lower() or 'east maui 1' in videos[j].lower() or 'ranch south' in videos[j].lower() or 'rifle b' in videos[j].lower() or 'lanaihale_guided' in videos[j].lower()):
        #if 'south maui 2' in videos[j].lower() or 'southmaui1' in videos[j].lower() or 'centralmaui2' in videos[j].lower() or 'ranch south' in videos[j].lower() or 'cleanup' in videos[j].lower():
            try:
                #print(video_name)
                df = pd.read_csv(video_name)
                #print(df)
        
                # Apply a new confidence threshold
                threshold = conf_thres
                filtered = df[df['confidence'] >= threshold]
                
                # Count detections per frame
                detections_per_frame = filtered.groupby('frame').size()
                dearz = detections_per_frame.reindex(range(detections_per_frame.index.max()), fill_value=0).tolist()
        
                #Take every 6th value (10 frames per second)
                #dearz = dearz[0::6]
                    
                peaks = peakutils.indexes(np.array(dearz, dtype=int), thres=0.0001, min_dist=120)
                count = 0
                for i in peaks:
                    count += dearz[i]
                    
                counts.append(count)
                DLNR_Counts_valid.append(DLNR_Counts[j])
                video_name_list.append(videos[j])
    
                
                #print(videos[j], '\n')
                #print('number of maximums:', len(peaks))
                #print('Estimated Count:', count)
                #print('DLNR Count:', DLNR_Counts[j])
        
                time = [i / 60 for i in range(len(dearz))]
                time_hms = [str(datetime.timedelta(seconds=t)) for t in time]
                
                
                #Extract part of lists
                n = len(dearz)
                quarter_length = n // 4
                
                #dearz_slice = dearz[2 * quarter_length: 3 * quarter_length]
                #time_hms = time_hms[2 * quarter_length: 3 * quarter_length]
                time_hms = [t.rstrip('0') for t in time_hms]
                
                # Plot the list of y-values
                #plt.plot(time_hms, dearz_slice)
                #plt.plot(time_hms, dearz)
                #print(np.array(time_hms)[peaks.astype(int)])
                #plt.scatter(np.array(time_hms)[peaks.astype(int)], np.array(dearz)[peaks.astype(int)], color='red', marker='o', label='Deer Detected')
                #plt.xticks(range(0, len(time_hms), 12000), time_hms[::12000], rotation=45)  # Rotate x-axis labels for better readability
                #plt.legend()
                #plt.show()
                #plt.savefig(“filename.png", dpi=300, bbox_inches="tight") / subplot

                
            except:
                #no += 1
                pass
    print('Confidence Threshold: \n', conf_thres) 
    MAE = mae(DLNR_Counts_valid, counts)

    MSE = np.square(np.subtract(DLNR_Counts_valid,counts)).mean()  
    RMSE = math.sqrt(MSE)
    
    r2 = r2_score(DLNR_Counts_valid, counts)
    
    mape = np.mean(np.abs((np.array(DLNR_Counts_valid) - np.array(counts))/np.array(DLNR_Counts_valid)))*100
    
    
    DLNR_Counts_valid = np.array(DLNR_Counts_valid, dtype=float)  # force numeric array
    counts = np.array(counts, dtype=float)
    
    plt.scatter(DLNR_Counts_valid, counts)
    for i in range(len(video_name_list)):
        plt.annotate(video_name_list[i], (DLNR_Counts_valid[i], counts[i]))
    
    plt.axline((0, 0), slope=1)
    
    ax = plt.gca()
    
    ax.grid()
    plt.minorticks_on()
    
    m, b = np.polyfit(DLNR_Counts_valid, counts, 1)
    plt.plot(counts, m*counts + b, color="red", label="Best fit line")
    
    
    plt.xlabel("DLNR Counts")
    plt.ylabel("Estimated Counts")
    
    plt.title("Dearz12")
    plt.show()
    
    print('MAE:', MAE)
    print('RMSE:', RMSE)
    print('MAPE:', mape)
    print('R2:', r2)
    _
    print(f"Slope (m): {m}")
    print(f"Intercept (b): {b}")
