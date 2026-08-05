
# DeerAI Detection System
Detects deer in infrared helicopter and drone videos.

To run on a Windows machine, download the latest release and run the script: `run.vbs`.

The script will check all dependencies including: Git Bash, CUDA Drivers, Python.

## Datasets

Download the datasets:
```
gcloud storage cp -r gs://deer-datasets/* .
```

### Model Training


| Model             | Purpose                                           | Baseline          | Train Command                                 |
| -------------     | -------------                                     | -------------     |  -------------                                |
| flir-binary-1     | Filter out non-deer frames in helicopter videos.  | yolo11n           | `yolo cfg=flir-binary-1/args.yaml`            |
| drone-binary-1    | Filter out non-deer frames in drone videos.       | yolo11n           | `yolo cfg=drone-binary-1/args.yaml`           |
| dearz13-baseline  | Detects deer in helicopter videos.                | yolo12n           | `yolo cfg="dearz13-baseline/args.yaml`        |
| Dearz-Drone-1-transfer | Detects deer in drone videos.                | dearz13-baseline  | `yolo cfg="Dearz-Drone-1-transfer/args.yaml`  |






