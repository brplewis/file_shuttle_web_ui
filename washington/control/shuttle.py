#!/usr/bin/python3.6


"""
\\\\\\\\\\--------= File Shuttle =---------//////////
\\\\\\\\\\-=          Shuttle            =-//////////
//////////=================================\\\\\\\\\\
"""

import logging
import os
import smtplib
import ssl
import subprocess
import sys
import time
import requests
import hash
import threading


class Shuttle(threading.Thread):

    def __init__(self, name, api, root, target):
        threading.Thread.__init__(self)
        self.advisor = r"https://www.virustotal.com/api/v3/files/"
        self.content = "json"
        self.email = os.getenv("ALERT_EMAIL")
        self.emailp = os.getenv("ALERT_EMAIL_PASS")
        self.target_email = os.getenv("TARGET_EMAIL")
        self.transfer_folder = root
        self.transfer_log = self.transfer_folder.split('/')
        self.shuttle_name = name
        self.api_key = api
        self.root = root
        self.target_path = target


        log = open(f"./transfer_logs/{TRANSFER_LOG[2]}.log", 'w+')
        log.close()

        # Set up logging
        logging.basicConfig(level=logging.INFO, filename=f"./transfer_logs/{TRANSFER_LOG[2]}_transfers.log", format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S')

    def __del__(self):
        logging.info("Shuttle Terminated")

    def send_email(self, message, password):
        # Set up email functionality
        sender_email = self.email
        receiver_email = self.target_email
        message = message

        port = 465  # For SSL
        password = password

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Send Email
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("transferalertswlr@gmail.com", password)
            server.sendmail(sender_email, receiver_email, message)


    def unzip_folder(self,  zip_file, destination):
        try:
            # Unzip Folder
            subprocess.call(["unzip", zip_file, "-d", destination])
            # Remove zip folder
            subprocess.call(["rm", "-fr", zip_file])
        except Exception as ex:
            print(f'Unzip {zip_file} failed')
            print(f'Error: {ex}')
            logging.warning(f"{zip_file} Unzip Failed error: {ex}")


    def virus_check(file_path: str) -> bool:
        signature = hash.get_signature(file_path)
        suspect = requests.get(self.advisor + signature, headers={"x-apikey": self.api_key}, timeout=70)

        if suspect.status_code == 404:
            print("{}: Passed Inspection".format(f))
            logging.info("{}: Passed Inspection".format(f))
            return True

        elif suspect.status_code == 200:
            threat_detections = 0
            response_body = suspect.json()["data"]["attributes"]
            rep, total = response_body["reputation"], response_body["times_submitted"]
            providers = response_body["last_analysis_results"]
            for k, v in providers.items():
                if v["result"] != None:
                    print("{}: Threat Detected {} {}".format(f, k, v["result"]))
                    logging.warning("{}: Threat Detected {} {}".format(f, k, v["result"]))
                    threat_detections += 1
                    return False

            if threat_detections != 0:
                print("{}: Failed Inspection\nTotal Responses : {} / 72".format(f, threat_detections))
                logging.warning("{}: Failed Inspection\nTotal Responses : {} / 72".format(f, threat_detections))
            else:
                print("{}: Passed Inspection".format(f))
                logging.info("{}: Passed Inspection".format(f))
                return True

        else:
            print("Err: Unable to Parse File")
            return False


    def welcome_file(file_path: str):
        try:
            # Creates corresponding temp-xfer path
            base, file_name = os.path.split(file_path)
            destination = os.path.join(base + os.sep + file_name)
            destination = destination.replace(self.root, self.target_path)
            print("Destination: " + destination)

            # Check if folder exists, else create it
            if os.path.exists(os.path.dirname(destination)):
                subprocess.call(["mv", "--backup=t", file_path, destination])
            else:
                try:
                    xfer_destination = base.replace(self.root, self.target_path)
                    os.makedirs(xfer_destination, exist_ok=True)
                    subprocess.call(["mv", "--backup=t", file_path, xfer_destination])
                except Exception as ex:
                    print('Fileshare not configured! Auto-Configuration failed.')
                    print(f'Error: {ex}')
                    logging.warning(f"Fileshare error: {ex}")
                    log_to_slack()
                    return

            print("{}: File Transfer Successful".format(f))
            logging.info("{}: File Transfer Successful".format(f))
        except Exception as ex:
            print(f'Error: {ex}')
            logging.warning(f"{file_path} Transfer error: {ex}")


    def reject_file(message: str):
        # Send email explaining virus warning
        # Stop Samba service to stop access to client-xfer
        send_email(message, self.emailp)
        os.system("sudo service smbd stop")
        sys.exit()



    def run(self):

        try:
            for root, _, files in os.walk(self.transfer_folder):
                for f in files:
                    if os.path.splitext(f)[-1].lower() != ".exe" and '.DS_store' not in f:
                        if f.startswith("#chkpt_file") == False and f.startswith("#work_file") == False:
                            file_path = os.path.join(root + os.sep + f)

                            # If zip file then unzip
                            if os.path.splitext(f)[-1].lower() == ".zip":
                                folder, file_name = os.path.split(file_path)
                                unzip_folder(file_path, folder)

                            else:
                                clean = virus_check(file_path)
                                if clean == True:
                                    welcome_file(file_path)
                                    time.sleep(15)

                                else:
                                    email_message = "##############################################################\n" \
                                                    "VIRUS PROTOCOL INITIATED! {} failed virus check. TEMP-XFER is \n " \
                                                    "switching off SMB.\n Triggered by {} shuttle." \
                                                    "##############################################################".format(f, {self.transfer_folder})
                                    logging.warning(email_message)
                                    reject_file(email_message)

                        if os.path.splitext(f)[-1].lower() == ".exe":
                            email_message = "##############################################################\n" \
                                            "VIRUS PROTOCOL INITIATED! {} triggered the BLM / .EXE catcher. \n " \
                                            "TEMP-XFER is switching off SMB.\n Triggered by {} shuttle. " \
                                            "##############################################################".format(f, self.transfer_folder)
                            logging.warning(email_message)
                            reject_file(email_message)
        except Exception as ex:
            logging.warning(f"File_transfer has crashed. Error: {ex}")
            sys.exit()