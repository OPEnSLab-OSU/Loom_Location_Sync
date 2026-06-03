#!/bin/bash

# exits if anything fails
set -e
# make sure everything is updated
sudo apt update
# make sure we have what we need to create virtual environment and install requirements
sudo apt install -y python3 python3-venv python3-pip
# detects where the install script lives, and uses that for the location where we want to install. 
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"
# create virtual environment for intalling dependencies, with cehck to make sure it wasnt already created
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi 
# activate the virtual environment
source .venv/bin/activate
# install the requiremnts in the local repo
python -m pip install -r requirements.txt
# change permissions for bash script to be ran as an executable
chmod +x job_script.sh

echo "Please import config file, either by creating one or using scp from another device with the file."
echo "Please set up crontab with 0 0,12 * * * $PROJECT_DIR/job_script.sh >> $PROJECT_DIR/cron.log 2>&1"

