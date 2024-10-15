from datetime import datetime
from flask import jsonify, render_template, redirect, session

from application import app
from application.models.hrs import Hrs


@app.route('/recruiter/trace/requests')
def recruiter_trace_applicattion_hrs():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "recruiter":
        return redirect("/login")
    
    requests = Hrs.get_all_requests_trace()
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    
    return render_template(
        'recruiter/trace_requests.html',
        requests = requests,
        full_name = full_name
    )
    
    
@app.route('/get-cancel-reason/<int:hr_id>', methods=['GET'])
def get_cancel_reason(hr_id):
    # Fetch the cancellation reason from the database using hr_id
    reason = Hrs.get_cancel_reason({"hr_id": hr_id})
    return jsonify({"cancel_reason": reason})
