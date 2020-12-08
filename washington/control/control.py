from flask import Flask, render_template, request, redirect, url_for, Blueprint, make_response
from flask_login import current_user, login_required
from flask import current_app as app
from .. import forms
from .. import auth
from datetime import datetime, date
from ..models import db, Launcher, Api, User
from flask_login import logout_user
from .. import login_manager
#from . import launcher
import psutil

# Blueprint Configuration
control_bp = Blueprint(
    'control_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


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



@control_bp.route('/', methods=['POST', 'GET'])
#@login_required
def dashboard():


    # Get Status update from all launcher instances

    launcher_instances = {}

    for launchers in Launcher.query.all():
        launcher_instances[launchers.name] = launchers.name in (p.name() for p in psutil.process_iter())

        if launcher_instances[launchers.name]:
            launcher_instances[launchers.name] = "Online"
        else:
            launcher_instances[launchers.name] = "Offline"

    





    """
    # check if programs are running
    ml_share_stat = "ML_share" in (p.name() for p in psutil.process_iter())
    houston_stat = "Houston_Control" in (p.name() for p in psutil.process_iter())

    # Change to values to offline/online
    if ml_share_stat:
        ml_share_stat = 'Online'
    else:
        ml_share_stat = 'Offline'

    if houston_stat:
        houston_stat = 'Online'
    else:
        houston_stat = 'Offline'
    """








    """
    if request.method == 'POST':
        pass
    """
    return render_template('dashboard.html', status=launcher_instances)





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
