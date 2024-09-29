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
    session.clear()
    return redirect('/login')   
