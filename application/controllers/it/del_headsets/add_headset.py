from flask import flash, redirect, render_template, request, session

from application import app
from application.models.del_headset import Del_Headset



@app.route("/it/del/add/headsets", methods=["POST", "GET"])
def add_del_headset():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    if request.method == "POST":
        headser_data = {
            "headset_sn": request.form["headset_sn"],
            "operator": request.form["operator"],
            "user_id": session["user"]["user_id"]
        }
        
        if not Del_Headset.validate_headset(headser_data):
            return redirect("/it/del/add/headsets")
        
        Del_Headset.add_del_headset(headser_data)
        return redirect("/it/del/add/headsets")
    
    return render_template("it/del_headsets/add_headset.html")