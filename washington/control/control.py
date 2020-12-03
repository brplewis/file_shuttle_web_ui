from flask import Flask, render_template, request, redirect, url_for, Blueprint, make_response
from flask_login import current_user, login_required
from flask import current_app as app
from .. import forms
from .. import auth
from datetime import datetime, date
from ..models import db, support_ticket, clients, User
from flask_login import logout_user
from .. import login_manager

# Blueprint Configuration
tickets_bp = Blueprint(
    'tickets_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


print(auth.USER_ID)

@app.context_processors
def insert_user():
    if auth.USER_ID == None:
        return dict(user='No User')
    else:
        id = int(auth.USER_ID)
        user = User.query.get(id)
        return dict(user=user.name)


@app.context_processor
def if_admin():
    if auth.USER_ID == None:
        return dict(admin=False)
    else:
        user = User.query.get(auth.USER_ID)
        if user.account_type == 'admin':
            return dict(admin=True)
        else:
            return dict(admin=False)

@app.context_processor
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


def log_input(text_input, ticket=None, entry_type=0, log_id=None):
    # except a text input and create a time stamp and user # NOTE
    # make a tuple of the two and either append it onto a list
    # Or replace the edited entry with new edit and updated time stamp

    # If new entry
    if entry_type == 0:
        # New log
        ticket_log = []
        time_stamp = f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} @{auth.USER} | "
        full_entry = [time_stamp, text_input + '\n']

    elif entry_type == 1:
        # If entry is an update
        ticket_log = eval(ticket)
        time_stamp = f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} @{auth.USER} | "
        full_entry = [time_stamp, text_input + '\n']

    elif entry_type == 2:
        ticket_log = eval(ticket)

        log_id = int(log_id)

        ticket_log[log_id][1] = text_input

        if '## EDITED' in ticket_log[log_id][0]:
            original_timestamp = ticket_log[log_id][0].split('## EDITED')[0]
            new_timestamp = f"## EDITED {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} @{auth.USER} | "
        else:
            original_timestamp = ticket_log[log_id][0].split('|')[0]
            new_timestamp = f"## EDITED {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} @{auth.USER} | "

        ticket_log[log_id][0] = original_timestamp + new_timestamp

        return ticket_log

    ticket_log.append(full_entry)

    return ticket_log


@tickets_bp.route('/', methods=['POST', 'GET'])
@login_required
def dashboard():
    #if check_user():
    #    return redirect(url_for('tickets_bp.pending'))

    #form = forms.DashboardSearch()

    """
    if request.method == 'POST':
        pass
    """
    return render_template('dashboard.html')





"""
@tickets_bp.route('/pending', methods=['POST', 'GET'])
def pending():
    return render_template('pending.html')

@tickets_bp.route('/access_denied', methods=['POST', 'GET'])
def not_admin():
    return render_template('not_admin.html')

"""

@tickets_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
