# Under Construction
Currently, this README is out of date. It will be updated shortly

# About
Tracks and synchronizes IoT device locations in real time, leveraging Hologram’s REST API with MongoDB as a location cache for persistent storage and fast retrieval.
# Setup and Installation

This program is designed to run in a Linux environment.

## 1. Clone the repository

Clone the repository anywhere in your filesystem.
Be sure to note the location, as you will need it later when setting up the scheduler.

## 2. Add the config file

Add the config file inside:

Loom_Map/src
### Option 1 — Transfer an existing config

If you already have a working config file, you can transfer it using SCP:
```bash
scp path/to/my/config.py user@machine_ip:path/to/Loom_Map/src
```
### Option 2 — Create the file manually

Create a file named:
```bash
config.py
```
with the following variables defined:
```python
org_id = ""
hologram_api_key = ""
credentials = f"apikey:{hologram_api_key}"
loom_mongo_uri = ""
hologram_url_location = f"https://dashboard.hologram.io/api/a/devices/locations?orgid={org_id}"
```
## 3. Make the install script executable

Run:
```bash
chmod +x install.sh
```
## 4. Run the install script
```bash
./install.sh
```
This script will:

create the Python virtual environment

install dependencies

prepare the runtime environment

## 5. Schedule the job with cron

Open the cron scheduler:
```bash
crontab -e
```
Add the following line at the bottom:
```bash
0 0,12 * * * /path/to/Loom_Map/script.sh >> /path/to/Loom_Map/cron.log 2>&1
```
This schedules the script to run twice per day:

00:00 (midnight)

12:00 (noon)

## Documentation and Demo
### Demo Video

https://youtu.be/SPvb7UfcVZg

### Full Documentation

https://docs.google.com/document/d/1iaowcdVThSG-IY-LXu3ZF7BfUnMEFDJIBt4f9tBCXrU/edit?usp=sharing

### Install and Scheduling

https://youtu.be/puvYCw-Wz0A
