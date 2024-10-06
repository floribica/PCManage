from flask_bcrypt import Bcrypt
from flask import redirect, render_template, request, session

from application import app
from application.models.user import User

bcrypt = Bcrypt(app)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login_data = {
            'username': request.form['username'],
            'password': request.form['password']
        }

        # Fetch the user from the database
        user = User.get_user_by_username(login_data)

        if user:
            # Verify the entered password with the stored hashed password
            if bcrypt.check_password_hash(user['password'], login_data['password']):
                # Store user in session and redirect to dashboard
                session['user'] = user
                return redirect('/admin/dashboard')

        # If authentication fails, redirect to login page
        return redirect('/')
    
    return render_template('login/login.html')


@app.route('/logout')
def logout():
    # Clear the session and log the user out
    session.clear()
    return redirect('/login')
