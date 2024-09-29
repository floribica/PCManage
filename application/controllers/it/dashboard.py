from flask import render_template, redirect, session

from application import app


@app.route('/it/dashboard')
def it_dashboard():
    if 'user' not in session:
        return redirect('/')
    if session['user']['role'] != 'it':
        return redirect('/')
    return render_template('it/index.html')
