#!/bin/bash


VIDEOS=(
        #Valid
        "11_22_23 Survey 1_CentralMaui2MahiPono2.mov" #Done
        "Central Maui 3_Mahi Pono 3 Colton Loque.mov" 

        "South Maui 3 Colton Loque.mov" #Done
        "Upcountry Maui 1 Colton Loque.mov" #Done

        "Kanaio_Kahikinui_Kipahulu 1A.mov" #Done
        #"Kanaio_Kahikinui_Kipahulu 1B.mov" #small

        "West Maui 2.mov" #Done
        "Lanai Pulama Rifle A1 & A2.mov" #Done
        "Lanaihale_Guided Hunting_CGMA Unit 3.mov"

        "Molokai Ranch South.mov" #Done

        #Test
        "11_29_23 Survey 1_CentralMauiCleanUp.mov"
        "11_29_23 Survey 2_SouthMaui1.mov"
        "Upcountry Maui 2 Colton Loque.mov"
        
        #"Kanaio_Kahikinui_Kipahulu 2A.mov" #small
        "Kanaio_Kahikinui_Kipahulu 2B.mov" #6 GB
        "Kanaio_Kahikinui_Kipahulu 2C.mov" #6 GB
        "Kanaio_Kahikinui_Kipahulu 2D.mov" #6 GB

        "Hanaula 1A Colton Loque.mov" #2.5 GB
        "Hanaula 1B Colton Loque.mov" #2.5 GB
        "Hanaula 1C Colton Loque.mov" #2.5 GB
        #"Hanaula 1D Colton Loque.mov" #2.5 GB
        #"Hanaula 1E Colton Loque.mov" #2.5 GB
        #"Hanaula 1F Colton Loque.mov" #2.5 GB
        #"Hanaula 1G Colton Loque.mov" #2.5 GB
        #"Hanaula 1H Colton Loque.mov" #2.5 GB
        #"Hanaula 1I Colton Loque.mov" #2.5 GB
        #"Hanaula 1J Colton Loque.mov" #2.5 GB
        #"Hanaula 1K Colton Loque.mov" #2.5 GB #Rer

        #"Kalaupapa 1.mov" #small
        "Kalaupapa 2.mov" #12 GB
        #"Kalaupapa 3.mov" #small

        "Kanaio_Kahikinui_Kipahulu 4.mov" #13 GB

        "Lanai CGMA Unit 2.mov"

        #"East Maui 1A.mov" #small
        "East Maui 1B.mov"
        
        


        
        #"Kula Ag Park 1&2A drone.mov"
        #"Kula Ag Park 1&2B drone.mov"
        #"Kula Ag Park 1&2C drone.mov"
        #"Kula Ag Park 1&2D drone.mov"

        #"Kula Ag Park 3&4_Pukalani 1-3 drone 1A.mov"
        #"Kula Ag Park 3&4_Pukalani 1-3 drone 1B.mov"
        #"Kula Ag Park 3&4_Pukalani 1-3 drone 1C.mov"
        #"Kula Ag Park 3&4_Pukalani 1-3 drone 1D.mov"
        )

# Number of GPUs available
NUM_GPUS=$(nvidia-smi -L | wc -l)

# Process videos in parallel across GPUs
for i in "${!VIDEOS[@]}"; do
    gpu_id=$((i % NUM_GPUS))
    video="${VIDEOS[$i]}"
    
    # Run processing on specific GPU
    CUDA_VISIBLE_DEVICES=$gpu_id python Inference.py "$video" &
    
done

wait
