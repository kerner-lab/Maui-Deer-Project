
# DeerAI Detection System
Detects deer in infrared helicopter and drone videos.

To run on a Windows machine, download the latest release and run the script: `run.vbs`.

The script will check all dependencies including: Git Bash, CUDA Drivers, Python.


### Models

**Deer vs. No Deer Filter Models**

The drone-binary-1 and flir-binary-1 directories contain lighter-weight models designed for an initial processing step to filter out video frames containing no deer (for drone and FLIR data respectively). Since the vast majority of frames contain no animals, this initial filtering step cuts down on both processing time and false-positives

**Deer Segmentation Models**

The Dearz-Drone-1-transfer and dearz13-baseline models are designed to segment and count the deer in a given frame (for drone and FLIR data respectively) after the initial "deer or no deer" filtering step.
