1. In Inference.py, select either drone or flir models and comment out the rest (below line 19)
2. Type in the video names you want to analyze in Dearz.sh (make sure names are surrounded by “ ”)
3. Run ./Dearz.sh from command line and wait for videos to be analyzed/annotated
4. Find the count files for the videos you want to count and add the names to the “videos” array in counts.py (make sure names are surrounded by “ ”)
5. Set peak_dist in counts.py (should be 2 times the frames per second of the original video)
6. Run python counts.py from the command line to get estimated deer counts for videos
