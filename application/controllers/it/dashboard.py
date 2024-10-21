from flask import render_template, redirect, session

from application import app
from application.models.hrs import Hrs
from application.models.pc_action import PC_Action


@app.route('/it/dashboard')
def it_dashboard():
    if 'user' not in session:
        return redirect('/')
    if session['user']['role'] != 'it':
        return redirect('/')
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    
    total_pc_action = PC_Action.count_pc_action_by_month()
    total_hrs = Hrs.count_hrs_by_month()
    total_reuest = Hrs.total_request()
    return render_template(
        'it/index.html',
        full_name=full_name,
        total_pc_action=total_pc_action,
        total_hrs=total_hrs,
        total_reuest=total_reuest
    )
