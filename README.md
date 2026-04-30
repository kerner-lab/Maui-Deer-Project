
# DeerAI Detection System
Detects deer in infrared helicopter and drone videos.

### Setup
On a machine with an NVIDIA GPU
1. Install CUDA Drivers: nvidia.com/drivers
2. Install python: python.org/downloads
3. Install git: git-scm.com/install
4. Download and unzip latest release: 

### First run
Inside unziped folder click run.vbs to run the detection system. 
The first time this will automatically install necessary prerequisites. 


### Models

**Deer vs. No Deer Filter Models**

The drone-binary-1 and flir-binary-1 directories contain lighter-weight models designed for an initial processing step to filter out video frames containing no deer (for drone and FLIR data respectively). Since the vast majority of frames contain no animals, this initial filtering step cuts down on both processing time and false-positives

**Deer Segmentation Models**

The Dearz-Drone-1-transfer and dearz13-baseline models are designed to segment and count the deer in a given frame (for drone and FLIR data respectively) after the initial "deer or no deer" filtering step.
