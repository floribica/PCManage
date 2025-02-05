from flask import flash, redirect, render_template, request, session

from application import app
from application.models.del_headset import Del_Headset
from application.models.hrs import Hrs
from application.helpers.cuffie_excel_read import upload_cuffie_excel



@app.route("/it/del/add/headsets", methods=["POST", "GET"])
def add_del_headset():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
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
    
    if session["user"]["role"] == "admin":
        full_name = session["user"]["username"].capitalize()
        return render_template(
            "admin/del_headsets/add_headset.html",
            full_name=full_name
        )
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    total_reuest = Hrs.total_request()
    return render_template(
        "it/del_headsets/add_headset.html",
        full_name=full_name,
        total_reuest=total_reuest
    )


@app.route("/admin/del/add/excel", methods=["POST"])
def upload_excel():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    
    if request.method == "POST":
        file = request.files["file"]
        #remove spaces
        file.filename = file.filename.replace(" ", "_")
        if not file.filename.endswith(".xlsx"):
            flash("Invalid file format","del_add")
            return redirect("/it/del/add/headsets")
        upload_cuffie_excel(file)
        return redirect("/it/del/add/headsets")
    
    return redirect("/it/del/add/headsets")