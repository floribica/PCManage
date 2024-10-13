from flask_bcrypt import Bcrypt
from flask import redirect, render_template, request, session

from application import app
from application.helpers.password import generate_password
from application.models.user import User


@app.route('/it/change_password', methods=['GET', 'POST'])
def it_change_password():
    if request.method == 'POST':
        change_data = {
            'username': session['user']['username'],
            'old_password': request.form['old_password'],
            'password': request.form['password'],
            'confirm_password': request.form['confirm_password'],
        }

        if change_data['username'] != session['user']['username']:
            return redirect('/it/change_password')

        if not User.validate_user_reset(change_data):
            return redirect('/it/change_password')


        change_data["password"] = Bcrypt().generate_password_hash(change_data["password"])
        
        # Call method to update the user's password in the database
        User.user_reser_password(change_data)
        
        return redirect('/it/change_password')

    if 'user' not in session:
        return redirect('/')
    if session['user']['role'] != 'it':
        return redirect('/')
    
    return render_template('it/change_password.html')
