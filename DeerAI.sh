#!/bin/bash

# Determining files to process
# -------------------------------------------------------------------------------------------
INPUT=$1
files=()
if [ -z "$INPUT" ]; then
	echo "ERROR: DeerAI.sh expects a file path or folder path, usage:"
	echo 'DeerAI.sh "C:\Users\John\deer_videos\video_1.mp4"'
	echo 'DeerAI.sh "C:\Users\John\deer_videos"'
	exit 1
elif [ -d "$INPUT" ]; then
	echo "'$INPUT' is a directory..."
	DIR="${1:-.}"
	mapfile -t files < <(find "$DIR" -type f \( -iname "*.mp4" -o -iname "*.mov" \) ! \( -iname "*_counts.mp4" -o -iname "*_counts.mov" \))

elif [ -f "$INPUT" ]; then
	EXT="${INPUT##*.}" 
	if [ "$EXT" = "mp4" ] || [ "$EXT" = "mov" ]; then
		files+=("$INPUT")
	else 
		echo "ERROR: DeerAI.sh expected a .mp4, .mov or directory but got a file with :.$EXT"
	fi
else
	echo "ERROR: '$INPUT' is not a valid path"
	exit 1
fi
NUM_FILES=${#files[@]}
echo "Found ${NUM_FILES} files"

# Environment setup
# -------------------------------------------------------------------------------------------
if [ -d "venv" ] ; then
	source venv/scripts/activate
else
	echo "Setting up environment"
	python -m venv venv
	source venv/scripts/activate
	pip install -q torch torchvision --index-url https://download.pytorch.org/whl/cu130
	pip install -q ultralytics tqdm lap cursor peakutils
fi

# Log setup setup
# -------------------------------------------------------------------------------------------
if [ -d "logs" ] ; then
	rm -rf logs
fi
mkdir logs

echo "Starting up detection models for each file"
PIDS=()
i=0
for file in "${files[@]}"; do

	if [ "$2" = "--logs" ]; then
		if [[ "$file" == *drone* ]]; then
			python Inference2.py drone-binary-1 Dearz-Drone-1-transfer "$file" "logs/worker_$i.log" &
		elif [[ "$file" == *helicopter* ]]; then
			python Inference2.py flir-binary-1 dearz13-baseline "$file" "logs/worker_$i.log" &
		fi		
	else
		if [[ "$file" == *drone* ]]; then
			python Inference2.py drone-binary-1 Dearz-Drone-1-transfer "$file" "logs/worker_$i.log" 2>/dev/null &
		elif [[ "$file" == *helicopter* ]]; then
			python Inference2.py flir-binary-1 dearz13-baseline "$file" "logs/worker_$i.log" 2>/dev/null &
		fi
	fi
        
	PIDS+=($!)
	
	i=$((i + 1))
	if [ $((i % 10 )) -eq 0 ]; then
		sleep 10
	fi
done

python monitor_logs.py "$NUM_FILES" &
MONITOR_PID=$!

wait ${PIDS[@]}
kill $MONITOR_PID
