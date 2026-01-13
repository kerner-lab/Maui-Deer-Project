1. In Inference.py, select either drone or flir models and comment out the rest (below line 19)
2. Type in the video names you want to analyze in Dearz.sh (make sure names are surrounded by “ ”)
3. Run ./Dearz.sh from command line and wait for videos to be analyzed/annotated
4. Find the count files for the videos you want to count and add the names to the “videos” array in counts.py (make sure names are surrounded by “ ”)
5. Set peak_dist in counts.py (should be 2 times the frames per second of the original video)
6. Run python counts.py from the command line to get estimated deer counts for videos

Deer vs. No Deer Filter Models

The drone-binary-1 and flir-binary-1 directories contain lighter-weight models designed for an initial processing step to filter out video frames containing no deer (for drone and FLIR data respectively). Since the vast majority of frames contain no animals, this initial filtering step cuts down on both processing time and false-positives

Deer Segmentation Models

The Dearz-Drone-1-transfer and dearz13-baseline models are designed to segment and count the deer in a given frame (for drone and FLIR data respectively) after the initial "deer or no deer" filtering step.
