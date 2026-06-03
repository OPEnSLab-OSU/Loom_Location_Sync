#!/bin/bash

# outputs commands in script_output.txt
set -x
# locates directory where script.sh lives
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
# runs python script, and stores output in script_output.txt
OUTPUT_RES=$($PROJECT_DIR/.venv/bin/python $PROJECT_DIR/src/job.py) 
TIME=$(date +"%Y-%m-%d_%H-%M-%S")

echo -e "$TIME\n$OUTPUT_RES" >> $PROJECT_DIR/script_output.txt 2>&1
