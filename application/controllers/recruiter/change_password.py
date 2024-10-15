from flask_bcrypt import Bcrypt
from flask import redirect, render_template, request, session

from application import app
from application.models.user import User


@app.route('/recruiter/change_password', methods=['GET', 'POST'])
def recruiter_change_password():
    if 'user' not in session:
        return redirect('/')
    if session['user']['role'] != 'recruiter':
        return redirect('/')
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    
    if request.method == 'POST':
        change_data = {
            'username': session['user']['username'],
            'old_password': request.form['old_password'],
            'password': request.form['password'],
            'confirm_password': request.form['confirm_password'],
        }

        if change_data['username'] != session['user']['username']:
            return redirect('/recruiter/change_password')

        if not User.validate_user_reset(change_data):
            return redirect('/recruiter/change_password')


        change_data["password"] = Bcrypt().generate_password_hash(change_data["password"])
        
        # Call method to update the user's password in the database
        User.user_reser_password(change_data)
        
        return redirect('/recruiter/change_password')
    
    return render_template(
        'recruiter/change_password.html',
        full_name = full_name
    )
