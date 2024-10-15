from datetime import datetime
from flask import jsonify, render_template, redirect, session

from application import app
from application.models.hrs import Hrs


@app.route('/planning/trace/requests')
def planning_trace_applicattion_hrs():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "planning":
        return redirect("/login")
    
    requests = Hrs.get_all_requests_trace()
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    
    return render_template(
        'planning/trace_requests.html',
        requests = requests,
        full_name = full_name
    )
