from flask import flash, redirect, render_template, request, session

from application import app
from application.models.headset import Headset
from application.models.hrs import Hrs


@app.route("/it/headsets")
def inventory_headset():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    
    headsets = Headset.get_all_headsets()
    
    if session["user"]["role"] == "admin":
        full_name = session["user"]["username"].capitalize()
        return render_template(
            "admin/inventory/headsets.html",
            headsets = headsets,
            full_name = full_name
        )
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    total_reuest = Hrs.total_request()
    
    return render_template(
        "it/inventory/headsets.html",
        headsets = headsets,
        full_name=full_name,
        total_reuest=total_reuest
    )
    

@app.route("/it/headsets/edit/<int:headset_id>", methods=["GET", "POST"])
def inventory_headset_edit(headset_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    
    if request.method == "POST":
        headset_data = {
            "headset_id": headset_id,
            "adapter_model": request.form["adapter_model"],
            "adapter_sn": request.form["adapter_sn"],
            "headset_model": request.form["headset_model"],
            "serial_number": request.form["serial_number"]
        }
        if not Headset.validate_headset(headset_data):
            return redirect(f"/it/headsets/edit/{headset_id}")
        Headset.update_headset(headset_data)
        return redirect("/it/headsets")
    
    headset = Headset.get_headset_by_id({"headset_id": headset_id})
    if not headset:
        return redirect("/it/headsets")
    
    if session["user"]["role"] == "admin":
        full_name = session["user"]["username"].capitalize()
        return render_template(
            "admin/inventory/edit/headset.html",
            headset = headset,
            full_name = full_name
        )
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    total_reuest = Hrs.total_request()
    
    return render_template(
        "it/inventory/edit/headset.html",
        headset = headset,
        full_name=full_name,
        total_reuest=total_reuest
    )


@app.route("/it/headsets/delete/<int:headset_id>", methods=['DELETE'])
def inventory_headset_delete(headset_id):
    if "user" not in session:
        return redirect("/login")
    if session["user"]["role"] not in ["it", "admin"]:
        return redirect("/login")
    
    if request.method == "DELETE":
        Headset.delete_headset({"headset_id": headset_id})
    return redirect("/it/headsets")

