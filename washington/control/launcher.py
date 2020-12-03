#!/usr/bin/python3.6
"""
\\\\\\\\\--------=   File Shuttle  =---------/////////
\\\\\\\\\\-= Houston Transfer Controller =-//////////
//////////=================================\\\\\\\\\\
"""

# Dependencies

import logging
import os
import subprocess
import sys
import time
import setproctitle


logging.basicConfig(level=logging.INFO, filename="houston_logs.log", format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


# Launcher Set Up Variables
NAME = sys.argv[1]
ROOT = sys.argv[2]
APIS = sys.argv[3]
setproctitle.setproctitle(f'{NAME}')

ALL_APIS = []
USED_APIS = {}
FREE_APIS = []


def launch_shuttle(api, target_folder) -> str:
    # Launches an instance of auto transfer
    # Returns name
    os.system(f"python3 shuttle.py {target_folder} {api} & disown")


def kill_shuttle(folder_name):
    # Kills instance of shuttle
    proc_name = f"{folder_name}_Shuttle"[:15]
    subprocess.call(["pkill", f"{proc_name}"])


def get_size(start_path):
    total_size = 0
    for path, dirs, files in os.walk(start_path):
        for f in files:
            if f.startswith("#chkpt_file") == False and f.startswith("#work_file") == False:
                fp = os.path.join(path, f)
                total_size += os.path.getsize(fp)
            else:
                pass
    return total_size


def manage_shuttles(root):
    # Checks if folder is empty if so stops transfer
    # And reassigns api
    global FREE_APIS
    global USED_APIS
    assigned_folders = []
    empty_folders = []
    client_folders = []

    # Scans all directories in root folder
    for dir in os.listdir(root):
        client_folders.append(root + os.sep + dir)

    logging.info(f"Scanned {root} for updates. Client_folders up to date.")

    # Check if folders have data in
    # And organise into lists
    for folder in client_folders:
        folder_size = get_size(folder)
        logging.info(f"{folder} size: {folder_size}")
        # If folder has files to transfer
        if folder_size > 0:
            if folder in assigned_folders:
                pass
            else:
                assigned_folders.append(folder)
                logging.info(f"{folder} added to assigned_folders.")

                if folder in empty_folders:
                    empty_folders.remove(folder)
                    logging.info(f"{folder} removed from empty_folders.")

        # If folder has no files to transfer
        else:
            if folder in assigned_folders:
                assigned_folders.remove(folder)
                logging.info(f"{folder} removed from assigned_folders.")

            if folder in empty_folders:
                pass
            else:
                empty_folders.append(folder)
                logging.info(f"{folder} added to empty_folders.")

    # Kill unused shuttles
    for folder in empty_folders:
        try:
            FREE_APIS.append(USED_APIS[folder])
            del USED_APIS[folder]
            kill_shuttle(folder)
            logging.info(f"Killed {folder} shuttle.")
        except KeyError:
            pass

    # Assign shuttles to folders
    for folder in assigned_folders:
        if folder in USED_APIS:
            pass
        else:
            if len(FREE_APIS) >= 1:
                # Assign API to shuttle
                launch_shuttle(FREE_APIS[0], folder)
                USED_APIS[folder] = FREE_APIS[0]
                del FREE_APIS[0]
                logging.info(f"Launched {folder} shuttle")
            else:
                logging.warning(f"No API free to launch {folder} shuttle")

    logging.info("Launch cycle complete. God speed...")


def start_up():
    # Set up apis for use with shuttles
    global FREE_APIS
    for api in ALL_APIS:
        FREE_APIS.append(api)


if __name__ == "__main__":
    start_up()
    while True:
        try:
            time.sleep(15)
            manage_shuttles(ROOT)
        except:
            pass