import cursor
import os
import time
import sys

from pathlib import Path


cursor.hide()

try:
	num_workers = int(sys.argv[1])
	for _ in range(num_workers):
		print("")

	waiting_progress = ""

	while True:
		# Move cursor to top of block
		print(f"\033[{num_workers}A", end="")
	
		waiting_progress += "."
		if len(waiting_progress) > 3:
			waiting_progress = ""

	
		for i in range(num_workers):
			log_file = Path("logs") /  f"worker_{i}.log"
			log_line = f"Waiting {waiting_progress}"
			if log_file.exists():
				lines = log_file.read_text(encoding="utf-8", errors="replace").splitlines()
				if lines:
					log_line = lines[-1].rstrip()
			print(f"\033[K{log_line}")
			time.sleep(0.2)

finally:
	print(f"\033{num_workers}B", end="", flush=True)
	cursor.show()

