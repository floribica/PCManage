from flask import flash, redirect, render_template, request, session

from application import app
from application.models.del_headset import Del_Headset
from application.models.hrs import Hrs



@app.route("/it/del/headsets")
def del_headset():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    total_reuest = Hrs.total_request()
    
    headsets = Del_Headset.get_all_del_headsets()
    return render_template(
        "it/del_headsets/headsets.html",
        headsets = headsets,
        full_name=full_name,
        total_reuest=total_reuest
    )
    

@app.route("/it/del_headsets/return/<string:headset_sn>")
def return_headset(headset_sn):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    Del_Headset.headset_returnd({"headset_sn": headset_sn})
    return redirect("/it/del/headsets")
