from flask import render_template, redirect, session

from application import app
from application.models.hrs import Hrs


@app.route('/it/hrs/trace')
def it_trace_applicattion_hrs():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    requests = Hrs.get_all_requests_trace()
    
    return render_template(
        'it/trace_requests.html',
        requests = requests
    )


@app.route('/it/hrs/trace/ready/<int:hr_id>')
def it_application_hrs_ready(hr_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    Hrs.ready_request({"hr_id": hr_id})
    
    return redirect("/it/hrs/trace")


@app.route('/it/hrs/trace/submitted/<int:hr_id>')
def it_application_hrs_submitted(hr_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    Hrs.submitted_request({"hr_id": hr_id})
    
    return redirect("/it/hrs/trace")


@app.route('/it/hrs/trace/returned/<int:hr_id>')
def it_application_hrs_returned(hr_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    Hrs.returned_request({"hr_id": hr_id})
    
    return redirect("/it/hrs/trace")
