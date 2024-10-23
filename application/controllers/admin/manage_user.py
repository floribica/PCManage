from flask import redirect, session

from application import app
from application.models.user import User


@app.route('/users/deactivate/<int:user_id>')
def deactivate_user(user_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "admin":
        return redirect("/login")
    
    User.deactivate_user({"user_id": user_id})
    
    return redirect("/users")


@app.route('/users/activate/<int:user_id>')
def activate_user(user_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "admin":
        return redirect("/login")
    
    User.activate_user({"user_id": user_id})
    
    return redirect("/users")
