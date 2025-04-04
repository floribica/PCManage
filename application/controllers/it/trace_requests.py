from datetime import datetime
from flask import render_template, redirect, session

from application import app
from application.models.hrs import Hrs
from application.models.trace_date import Trace


@app.route('/it/hrs/trace')
def it_trace_applicattion_hrs():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    
    requests = Hrs.get_all_requests_trace()
    
    if session["user"]["role"] == "admin":
        full_name = session['user']['username'].capitalize()
        return render_template(
            'admin/request/trace_requests.html',
            requests = requests,
            full_name = full_name
        )
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    total_reuest = Hrs.total_request()
    
    return render_template(
        'it/trace_requests.html',
        requests = requests,
        full_name=full_name,
        total_reuest=total_reuest
    )


@app.route('/it/hrs/trace/ready/<int:hr_id>')
def it_application_hrs_ready(hr_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    
    data = {
        "hr_id": hr_id,
        "ready_date": datetime.now()
    }
    trace_date_id = Hrs.get_trace_date_id(data)
    if not trace_date_id:
        return redirect("/it/hrs/request")
    data["trace_date_id"] = trace_date_id["trace_date_id"]
    
    Trace.ready_request(data)
    Hrs.ready_request(data)
    
    return redirect("/it/hrs/trace")


@app.route('/it/hrs/trace/submitted/<int:hr_id>')
def it_application_hrs_submitted(hr_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "receptionist", "admin"]:
        return redirect("/login")
    
    data = {
        "hr_id": hr_id,
        "submitted_date": datetime.now()
    }
    trace_date_id = Hrs.get_trace_date_id(data)
    if not trace_date_id:
        return redirect("/it/hrs/request")
    data["trace_date_id"] = trace_date_id["trace_date_id"]
    
    Trace.submitted_request(data)
    Hrs.submitted_request(data)
    
    if session["user"]["role"] == "it":
        return redirect("/it/hrs/trace")
    else:
        return redirect("/receptionist/ready/requests")


@app.route('/it/hrs/trace/returned/<int:hr_id>')
def it_application_hrs_returned(hr_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    
    data = {
        "hr_id": hr_id,
        "returned_date": datetime.now()
    }
    trace_date_id = Hrs.get_trace_date_id(data)
    if not trace_date_id:
        return redirect("/it/hrs/request")
    data["trace_date_id"] = trace_date_id["trace_date_id"]
    
    Trace.returned_request(data)
    Hrs.returned_request(data)
    
    return redirect("/it/hrs/trace")
