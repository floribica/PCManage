from flask import render_template, redirect, session

from application import app


@app.route('/it/dashboard')
def it_dashboard():
    if 'user' not in session:
        return redirect('/')
    if session['user']['role'] != 'it':
        return redirect('/')
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    return render_template(
        'it/index.html',
        full_name=full_name
    )
