from flask_bcrypt import Bcrypt
from flask import flash, render_template, request, redirect, session

from application import app
from application.helpers.send_email import send_email, password_email
from application.helpers.password import generate_password
from application.models.user import User


@app.route('/admin/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        reset_data = {
            'username': request.form['username'],
            'email': request.form['email']
        }
        if not User.validate_reset(reset_data):
            return redirect('/admin/reset_password')
        password = generate_password()
        reset_data["password"] = Bcrypt().generate_password_hash(password)
        
        try:
            message = password_email(reset_data["email"], password)
            send_email(reset_data["email"],"Password Reset", message)
        except:
            flash("Failed to send email.", "reset")
            return redirect('/admin/reset_password')
        User.update_password(reset_data)
        
        return redirect('/admin/reset_password')
    if 'user' not in session:
        return redirect('/')
    if session['user']['role'] != 'admin':
        return redirect('/')
    return render_template('admin/reset_password.html')
