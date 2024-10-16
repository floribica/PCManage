from flask import render_template, redirect, session

from application import app


@app.route('/receptionist/dashboard')
def receptionist_dashboard():
    if 'user' not in session:
        return redirect('/')
    if session['user']['role'] != 'receptionist':
        return redirect('/')
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    return render_template(
        'receptionist/index.html',
        full_name = full_name
    )
