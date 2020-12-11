#!/usr/bin/python3.6
"""
\\\\\\\\\--------=   File Shuttle  =---------/////////
\\\\\\\\\\-=      Controller Module      =-//////////
//////////=================================\\\\\\\\\\
"""

from .launcher import Launcher
import logging


class Controller:

    def __init__(self):
        self.active_launchers = {} # name: object
        logging.basicConfig(level=logging.INFO, filename="./controller.log",
                            format='%(asctime)s | %(levelname)s | %(message)s',
                            datefmt='%d-%b-%y %H:%M:%S')

    def start_launcher(self):
        logging.info('Controller starting...')
        return

    def delete_launcher(self):
        pass

    def get_active_launchers(self):
        # returns list of active launchers
        launchers = []
        for launcher in self.active_launchers:
            launchers.append(launcher)

        return launchers

    def get_logs(self):
        # Return logs
        controller_logs = []
        # Get log entries from launcher
        with open('./controller.log', 'r+') as log:
            for line in log.readlines():
                line_split = line.split('|')
                controller_logs.append(line_split)
        controller_logs.reverse()

        return controller_logs


