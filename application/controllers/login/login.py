from flask_bcrypt import Bcrypt
from flask import render_template, request, redirect, session

from application import app

from application.models.user import User


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login_data = {
            'username': request.form['username'],
            'password': request.form['password']
        }
        user = User.get_user_by_username(login_data)
        if user:
            if Bcrypt().check_password_hash(user['password'], request.form['password']):
                session['user'] = user
                return redirect('/admin/dashboard')
        return redirect('/')
    return render_template('login/login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
