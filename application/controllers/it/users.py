from flask_bcrypt import Bcrypt
from flask import flash, render_template, redirect, session

from application import app
from application.helpers.password import generate_password
from application.helpers.send_email import password_email, send_email
from application.models.hrs import Hrs
from application.models.user import User


@app.route('/users')
def it_users():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    
    users = User.get_all_users()
    if session["user"]["role"] == "it":
        split_name = session['user']["username"].split(".")
        full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    else:
        full_name = session['user']["username"].capitalize()
    total_reuest = Hrs.total_request()
    
    if session["user"]["role"] == "it":
        return render_template(
            'it/users.html',
            users = users,
            full_name=full_name,
            total_reuest=total_reuest
        )
    return render_template(
        'admin/users/manage_user.html',
        users = users,
        full_name=full_name,
        total_reuest=total_reuest
    )
    
    
@app.route('/users/reset/password/<int:user_id>')
def it_reset_password(user_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    
    reset_data = {
        "user_id": user_id,
    }
    user = User.get_user_by_id(reset_data)
    if not user:
        return redirect("/users")
    password = generate_password()
    reset_data["password"] = Bcrypt().generate_password_hash(password)
    reset_data["email"] = user["email"]
    reset_data["username"] = user["username"]
    User.update_password(reset_data)
    
    try:
        message = password_email(reset_data["username"], password)
        send_email(reset_data["email"],"Password Reset", message)
    except:
        flash("Failed to send email.", "reset")
        return redirect('/admin/reset_password')
    User.update_password(reset_data)
    
    return redirect("/users")
