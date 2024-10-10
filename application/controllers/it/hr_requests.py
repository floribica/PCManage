from flask import jsonify, render_template, redirect, request, session

from application import app
from application.models.hrs import Hrs


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
    
    Hrs.approve_request({"hr_id": hr_id})
    
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
        "reason": reason
    }
    Hrs.cancel_request(cancel_data)
    
    return jsonify({"status": "success"})
