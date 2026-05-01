#!/bin/bash

INPUT=$1
INTRO="                                            
▄▄▄▄▄▄                       ▄▄▄▄   ▄▄▄▄▄   
███▀▀██▄                   ▄██▀▀██▄  ███    
███  ███ ▄█▀█▄ ▄█▀█▄ ████▄ ███  ███  ███    
███  ███ ██▄█▀ ██▄█▀ ██ ▀▀ ███▀▀███  ███    
██████▀  ▀█▄▄▄ ▀█▄▄▄ ██    ███  ███ ▄███▄   
"

if [ -z "$INPUT" ]; then
	echo "$INTRO"
	echo ""
	echo "Welcome to the DeerAI Detection system."
	echo ""
fi

# Dependency check
# -------------------------------------------------------------------------------------------

GPU=$(powershell.exe -command "CimInstance Win32_VideoController | Select-Object -ExpandProperty Name" 2>/dev/null | grep -i NVIDIA)
if [ -z "$GPU" ]; then
	echo "No NVIDIA GPU found. DeerAI Detection system requires a machine with a GPU."
	exit 1
fi
echo "✓ GPU: $GPU"

if command -v nvidia-smi &>/dev/null; then
	echo "✓ CUDA:  $(nvidia-smi | grep "CUDA Version" | awk '{print $9}')"
else
	echo "CUDA Driver not found, install from: https://www.nvidia.com/drivers, and try again."
	exit 1
fi

if command -v python &>/dev/null; then
	echo "✓ $(python --version)"
else
	echo "Python not found, install from https://www.python.com/downloads, and try again."
	exit 1
fi


if [ -d "venv" ] ; then
	source venv/scripts/activate
else
	echo "Setting up python environment ..."
	python -m venv venv
	source venv/scripts/activate
	echo "Installing required packages ..."
	pip install -r requirements.txt
fi

echo "✓ Python environment activated."


while true; do

	# File specification
	# -------------------------------------------------------------------------------------------
	files=()
	NUM_FILES=0
	while [ $NUM_FILES -eq 0 ]; do
		echo ""
		echo ""
		read -r -p "Enter a video file or folder path [SHIFT+INS to paste] or (Q)uit: " INPUT
		if [[ "$INPUT" == "q" ]] || [[ "$INPUT" == "Q" ]]; then
			exit 1
		elif [ -d "$INPUT" ]; then
			DIR="${INPUT:-.}"
			mapfile -t files < <(find "$DIR" -type f \( -iname "*.mp4" -o -iname "*.mov" \) ! \( -iname "*_counts.mp4" -o -iname "*_counts.mov" \))

		elif [ -f "$INPUT" ]; then
			EXT="${INPUT##*.}" 
			if [ "$EXT" = "mp4" ] || [ "$EXT" = "mov" ]; then
				files+=("$INPUT")
			else 
				echo "ERROR: DeerAI.sh expected a .mp4, .mov or directory but got a file with :.$EXT"
			fi
		else
			echo "ERROR: $INPUT is not a valid file path or folder path."
		fi
		NUM_FILES=${#files[@]}
	done
	echo "Found ${NUM_FILES} video files."


	# Drone or helicopter videos?
	# -------------------------------------------------------------------------------------------
	PROCESSING_TYPE=""
	if [[ "$INPUT" == *drone* ]]; then
		PROCESSING_TYPE="drone"
	elif [[ "$INPUT" == *helicopter* ]]; then
		PROCESSING_TYPE="helicopter"
	else
		PROCESSING_TYPE=""
		while [-z "$PROCESSING_TYPE" ]; do
			read -r -p "Are these (d)rone or (h)elicopter videos?: " CHOICE
			case $CHOICE in
				h|H) PROCESSING_TYPE="helicopter" ;;
				d|D) PROCESSING_TYPE="drone"	;;
				*) echo "Please enter d or h"	;;
			esac
		done
	fi


	# Log setup setup
	# -------------------------------------------------------------------------------------------
	if [ -d "logs" ] ; then
		rm -rf logs
	fi
	mkdir logs


	# Inference
	# -------------------------------------------------------------------------------------------
	echo "Starting up detection models for each file (file paths can be opened with CTRL+click)."
	PIDS=()
	i=0
	for file in "${files[@]}"; do
		if [[ "$PROCESSING_TYPE" == "drone" ]]; then
			python Inference2.py drone-binary-1 Dearz-Drone-1-transfer "$file" "logs/worker_$i.log" 2>logs/error_$i.log &
		elif [[ "$PROCESSING_TYPE" == "helicopter" ]]; then
			python Inference2.py flir-binary-1 dearz13-baseline "$file" "logs/worker_$i.log" 2>logs/error_$i.log &
		else
			echo "Processing type could not be determined."
		fi	
		PIDS+=($!)
		i=$((i + 1))

		# If more than 10 videos, wait to free up I/O
		if [ $((i % 10 )) -eq 0 ]; then
			sleep 10
		fi
	done

	python monitor_logs.py "$NUM_FILES" &
	MONITOR_PID=$!

	wait ${PIDS[@]}
	kill $MONITOR_PID

	sleep 1

done