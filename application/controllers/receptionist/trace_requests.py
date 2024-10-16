from flask import render_template, redirect, session

from application import app
from application.models.hrs import Hrs


@app.route('/receptionist/ready/requests')
def receptionist_trace_applicattion_hrs():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "receptionist":
        return redirect("/login")
    
    requests = Hrs.get_all_ready_requests_trace()
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    
    return render_template(
        'receptionist/ready_pc.html',
        requests = requests,
        full_name = full_name
    )
