from flask import redirect, session

from application import app


@app.route('/')
def index():
    if "user" not in session:
        return redirect('/login')
    return redirect('/check')


@app.route('/check')
def check():
    if session['user']['role'] == 'admin':
        return redirect('/admin/dashboard')
    if session['user']['role'] == 'it':
        return redirect('/it/dashboard')
    if session['user']['role'] == 'recruiter':
        return redirect('/recruiter/dashboard')
    if session['user']['role'] == 'receptionist':
        return redirect('/receptionist/dashboard')
    if session['user']['role'] == 'planning':
        return redirect('/planning/dashboard')
    session.clear()
    return redirect('/login')   
