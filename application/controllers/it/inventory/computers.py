from flask import flash, redirect, render_template, request, session

from application import app
from application.models.computer import Computer
from application.models.hrs import Hrs


@app.route("/it/computers")
def inventory_pc():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    
    computers = Computer.get_all_computers()
    
    if session["user"]["role"] == "admin":
        full_name = session["user"]["username"].capitalize()
        return render_template(
            "admin/inventory/computers.html",
            computers = computers,
            full_name=full_name
        )
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    total_reuest = Hrs.total_request()
    
    return render_template(
        "it/inventory/computers.html",
        computers = computers,
        full_name=full_name,
        total_reuest=total_reuest
    )


@app.route("/it/computers/edit/<string:serial_nr>", methods=["GET", "POST"])
def inventory_pc_edit(serial_nr):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")

    if request.method == "POST":
        computer_data = {
            "serial_nr": serial_nr,
            "model": request.form["model"],
            "cpu": request.form["cpu"],
            "ram": request.form["ram"],
            "storage_type": request.form["storage_type"],
            "storage_value": request.form["storage_value"]
        }
        if len(computer_data["model"]) < 5:
            flash("Model name must be at least 5 characters long.", "model")
            return redirect(f"/it/computers/edit/{serial_nr}")
        Computer.update_computer(computer_data)
        return redirect("/it/computers")
    
    computer = Computer.get_computer_by_serial_nr({"serial_nr": serial_nr})
    if not computer:
        return redirect("/it/computers")
    
    if session["user"]["role"] == "admin":
        full_name = session["user"]["username"].capitalize()
        return render_template(
            "admin/inventory/edit/computer.html",
            computer = computer,
            full_name=full_name
        )
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    total_reuest = Hrs.total_request()
    
    return render_template(
        "it/inventory/edit/computer.html",
        computer = computer,
        full_name=full_name,
        total_reuest=total_reuest
    )


@app.route("/it/computers/delete/<string:serial_nr>", methods=['DELETE'])
def inventory_pc_delete(serial_nr):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    
    if request.method == "DELETE":
        Computer.delete_computer({"serial_nr": serial_nr})
    return redirect("/it/computers")
