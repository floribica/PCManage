from datetime import datetime
from flask import render_template, redirect, session

from application import app
from application.models.hrs import Hrs
from application.models.trace_date import Trace


@app.route('/planning/confirm/requests')
def planning_confirm_applicattion_hrs():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["planning", "admin"]:
        return redirect("/login")
    
    requests = Hrs.get_all_requests_and_approved()
    
    if session["user"]["role"] == "admin":
        full_name = session['user']['username'].capitalize()
        return render_template(
            'admin/request/confirm_requests.html',
            requests = requests,
            full_name = full_name
        )
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    
    return render_template(
        'planning/confirm_requests.html',
        requests = requests,
        full_name = full_name
    )


@app.route('/planning/confirm/requests/<int:hr_id>')
def planning_confirm_request(hr_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "planning":
        return redirect("/login")
    
    trace_date_id = Hrs.get_trace_date_id({"hr_id": hr_id})
    
    data = {
        "trace_date_id": trace_date_id["trace_date_id"],
        "authorization_date": datetime.now()
    }
    Trace.authorization_request(data)
    
    return redirect("/planning/confirm/requests")
