from flask import render_template, redirect, session

from application import app


@app.route('/admin/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    if session['user']['role'] != 'admin':
        return redirect('/')
    return render_template('admin/index.html')
