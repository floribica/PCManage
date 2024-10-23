from flask_bcrypt import Bcrypt
from flask import flash, render_template, request, redirect, session

from application import app
from application.helpers.send_email import send_email, password_email
from application.helpers.password import generate_password
from application.models.user import User


@app.route('/admin/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        register_data = {
            'username': request.form['username'],
            'role': request.form['role'],
            'email': request.form['email']
        }
        if not User.validate_register(register_data):
            return redirect('/admin/register')
        password = generate_password()
        register_data["password"] = Bcrypt().generate_password_hash(password)
        
        try:
            message = password_email(register_data["username"], password)
            send_email(register_data["email"],"New Account", message)
        except:
            flash("Failed to send email.", "register")
            return redirect('/admin/register')
        
        User.create_user(register_data)
        
        return redirect('/admin/register')
    if 'user' not in session:
        return redirect('/')
    if session['user']['role'] != 'admin':
        return redirect('/')
    return render_template('admin/users/register.html')