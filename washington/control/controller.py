#!/usr/bin/python3.6
"""
\\\\\\\\\--------=   File Shuttle  =---------/////////
\\\\\\\\\\-=      Controller Module      =-//////////
//////////=================================\\\\\\\\\\
"""

from .launcher import Launcher


class Controller:

    def __init__(self):
        self.active_launchers = {} # name: object

    def start_launcher(self):
        pass

    def delete_launcher(self):
        pass

    def get_active_launchers(self):
        # returns list of active launchers
        launchers = []
        for launcher in self.active_launchers:
            launchers.append(launcher)

        return launchers