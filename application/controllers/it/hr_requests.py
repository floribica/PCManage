from datetime import datetime
from flask import jsonify, render_template, redirect, request, session

from application import app
from application.models.hrs import Hrs
from application.models.trace_date import Trace


@app.route('/it/hrs/request')
def it_applicattion_hrs():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    requests = Hrs.get_all_requests()
    
    return render_template(
        'it/hr_requests.html',
        requests = requests
    )


@app.route('/it/hrs/approve/<int:hr_id>')
def approve_hrs_request(hr_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    data = {
        "hr_id": hr_id,
        "approved_date": datetime.now()
    }
    trace_date_id = Hrs.get_trace_date_id(data)
    if not trace_date_id:
        return redirect("/it/hrs/request")
    data["trace_date_id"] = trace_date_id["trace_date_id"]
    
    Hrs.approve_request(data)
    Trace.approve_request(data)
    
    return redirect("/it/hrs/request")


@app.route('/it/hrs/cancel/<int:hr_id>', methods=["POST"])
def cancel_hrs_request(hr_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    data = request.get_json()
    reason = data.get('reason')
    cancel_data = {
        "hr_id": hr_id,
        "reason": reason,
        "cancel_date": datetime.now()
    }
    trace_date_id = Hrs.get_trace_date_id(cancel_data)
    if not trace_date_id:
        return redirect("/it/hrs/request")
    cancel_data["trace_date_id"] = trace_date_id["trace_date_id"]
    
    Trace.cancel_request(cancel_data)
    Hrs.cancel_request(cancel_data)
    
    return jsonify({"status": "success"})
