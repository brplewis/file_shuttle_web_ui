#!/usr/bin/python3.6
"""
\\\\\\\\\--------=   File Shuttle  =---------/////////
\\\\\\\\\\-= Head Controller "Washington"=-//////////
//////////=================================\\\\\\\\\\
"""


from flask import Flask, render_template, request, redirect, url_for, Blueprint, make_response
from flask_login import current_user, login_required
from flask import current_app as app
from .. import forms
from .. import auth
from datetime import datetime, date
from ..models import db, Launcher, Api, User
from flask_login import logout_user
from .. import login_manager
#from .launcher import Launcher
from .controller import Controller




# Blueprint Configuration
control_bp = Blueprint(
    'control_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

CONTROLLER = Controller()
LAUNCHER_INSTANCES = {}
LAUNCHER_LOGS = {}
SHUTTLE_LOGS = {}


print(auth.USER_ID)

#@app.context_processors
def insert_user():
    if auth.USER_ID == None:
        return dict(user='No User')
    else:
        id = int(auth.USER_ID)
        user = User.query.get(id)
        return dict(user=user.name)


#@app.context_processor
def if_admin():
    if auth.USER_ID == None:
        return dict(admin=False)
    else:
        user = User.query.get(auth.USER_ID)
        if user.account_type == 'admin':
            return dict(admin=True)
        else:
            return dict(admin=False)

#@app.context_processor
def user_type():
    if auth.USER_ID == None:
        return dict(user_type=None)
    else:
        user = User.query.get(auth.USER_ID)

        return dict(user_type=user.account_type)



def check_user():
    user = User.query.get(auth.USER_ID)
    if user.account_type == 'pend':
        return True

def check_admin():
    user = User.query.get(auth.USER_ID)
    if user.account_type != 'admin':
        return False

"""

def update_dashboard():
    # Get Status update from all launcher instances
    global LAUNCHER_INSTANCES = {}
    global LAUNCHER_LOGS = {}
    global SHUTTLE_LOGS = {}

    for launchers in Launcher.query.all():
        # Check if launcher is online
        if launchers in CONTROLLER.get_active_launchers():
            launcher_instances[launchers.name] = "Online"
        else:
            launcher_instances[launchers.name] = "Offline"

        # Get log entries from launcher
        with open(f'./launcher_logs/{launchers.name}.log', 'r') as log:
            message = []
            i = 0
            lines = log.read().splitlines()
            log_sample = []
            for l in range(10):
                try:
                    for f in range(len(lines)):
                        i += 1
                        message.append(lines[-i])
                        if f"INFO - Scanned" in lines[-i] and "for updates. Client_folders up to date." in lines[-i]:
                            message.reverse()
                            log_message = " \n".join(message)
                            post = "------= New Cycle Complete =------\n" + log_message + "\n" + "-------------= End =-------------"
                            log_sample.append(post)
                except IndexError:
                    break
            launcher_logs[launchers.name] = log_sample

        # Get logs for each shuttle belonging to launcher
        for shuttle in launchers.get_active_shuttles():
            try:
                with open(f'./transfer_logs/{shuttle}.log', 'r') as log:
                    log_lines = []
                    for line in log:
                        log_lines.append(line)
                        if len(log_lines) == 60:
                            break
                    sample_log = "\n".join(log_lines)
                    launcher_logs[launchers.name] = sample_log
            except FileNotFoundError:
                launcher_logs[launchers.name] = "ERROR: Logs not found!"

"""


@control_bp.route('/', methods=['POST', 'GET'])
#@login_required
def dashboard():

    #update_dashboard()
    launcher_instances = {'Houston' : 'Online'}
    controller = Controller()
    controller.start_launcher()
    controller_logs = controller.get_logs()





    """
    if request.method == 'POST':
        pass
    """
    return render_template('dashboard.html', status=launcher_instances, controller_logs=controller_logs)





"""
@tickets_bp.route('/pending', methods=['POST', 'GET'])
def pending():
    return render_template('pending.html')

@tickets_bp.route('/access_denied', methods=['POST', 'GET'])
def not_admin():
    return render_template('not_admin.html')

"""

@control_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
