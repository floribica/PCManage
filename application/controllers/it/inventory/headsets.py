from flask import flash, redirect, render_template, request, session

from application import app
from application.models.headset import Headset


@app.route("/it/headsets")
def inventory_headset():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    headsets = Headset.get_all_headsets()
    return render_template(
        "it/inventory/headsets.html",
        headsets = headsets
    )
    

@app.route("/it/headsets/edit/<int:headset_id>", methods=["GET", "POST"])
def inventory_headset_edit(headset_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    if request.method == "POST":
        headset_data = {
            "headset_id": headset_id,
            "adapter_model": request.form["adapter_model"],
            "adapter_sn": request.form["adapter_sn"],
            "headset_model": request.form["headset_model"],
            "headset_sn": request.form["headset_sn"]
        }
        if not Headset.validate_headset(headset_data):
            return redirect(f"/it/headsets/edit/{headset_id}")
        Headset.update_headset(headset_data)
        return redirect("/it/headsets")
    
    headset = Headset.get_headset_by_id({"headset_id": headset_id})
    if not headset:
        return redirect("/it/headsets")
    return render_template(
        "it/inventory/edit/headset.html",
        headset = headset
    )


@app.route("/it/headsets/delete/<int:headset_id>", methods=['DELETE'])
def inventory_headset_delete(headset_id):
    if "user" not in session:
        return redirect("/login")
    if session["user"]["role"] != "it":
        return redirect("/login")
    
    if request.method == "DELETE":
        Headset.delete_headset({"headset_id": headset_id})
    return redirect("/it/headsets")

