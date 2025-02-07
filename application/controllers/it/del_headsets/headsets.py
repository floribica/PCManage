from flask import flash, redirect, render_template, request, session

from application import app
from application.models.del_headset import Del_Headset
from application.models.hrs import Hrs



@app.route("/it/del/headsets")
def del_headset():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    
    headsets = Del_Headset.get_all_del_headsets()
    
    if session["user"]["role"] == "admin":
        full_name = session["user"]["username"].capitalize()
        return render_template(
            "admin/del_headsets/headsets.html",
            headsets = headsets,
            full_name=full_name
        )
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    total_reuest = Hrs.total_request()
    
    return render_template(
        "it/del_headsets/headsets.html",
        headsets = headsets,
        full_name=full_name,
        total_reuest=total_reuest
    )
    

@app.route("/it/del_headsets/return/<string:serial_number>")
def return_headset(serial_number):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    Del_Headset.headset_returnd({"serial_number": serial_number})
    return redirect("/it/del/headsets")
