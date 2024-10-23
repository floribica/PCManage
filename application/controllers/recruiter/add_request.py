from datetime import datetime
from flask import flash, redirect, render_template, request, session

from application import app
from application.models.hrs import Hrs
from application.models.trace_date import Trace


@app.route('/recruiter/add/request', methods=['GET', 'POST'])
def recruiter_add_request():
    if 'user' not in session:
        return redirect('/')
    if session['user']['role'] not in ['recruiter', 'admin']:
        return redirect('/')

    if request.method == 'POST':
        add_request_data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "fushata": request.form['fushata'],
            "request_by": session['user']['username'],
        }

        if not Hrs.validate_add_request(add_request_data):
            return redirect('/recruiter/add/request')

        Trace.add_request({"request_date": datetime.now()})
        trace_date_id = Trace.get_last_trace_date_id()
        add_request_data["trace_date_id"] = trace_date_id["trace_date_id"]
        Hrs.add_request(add_request_data)
        flash('Request added successfully', 'success')

        return redirect('/recruiter/add/request')
    
    if session['user']['role'] == 'admin':
        full_name = session['user']['username'].capitalize()
        return render_template(
            'admin/request/add_request.html',
            full_name = full_name
        )

    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    return render_template(
        'recruiter/add_request.html',
        full_name = full_name
    )
