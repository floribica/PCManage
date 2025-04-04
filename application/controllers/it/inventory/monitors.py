from flask import redirect, render_template, request, session

from application import app
from application.models.hrs import Hrs
from application.models.monitor import Monitor


@app.route("/it/monitors")
def inventory_monitors():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    
    monitors = Monitor.get_all_monitors()
    
    if session["user"]["role"] == "admin":
        full_name = session["user"]["username"].capitalize()
        return render_template(
            "admin/inventory/monitors.html",
            monitors = monitors,
            full_name = full_name
        )
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    total_reuest = Hrs.total_request()
    
    return render_template(
        "it/inventory/monitors.html",
        monitors = monitors,
        full_name=full_name,
        total_reuest=total_reuest
    )
    

@app.route("/it/monitors/edit/<string:monitor_sn>", methods=["GET", "POST"])
def inventory_monitor_edit(monitor_sn):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    
    if request.method == "POST":
        monitor_data = {
            "monitor_sn": monitor_sn,
            "model": request.form["model"],
            "size": request.form["size"]
        }
        if not Monitor.validate_monitor(monitor_data):
            return redirect(f"/it/monitors/edit/{monitor_sn}")
        Monitor.update_monitor(monitor_data)
        return redirect("/it/monitors")
    
    monitor = Monitor.get_monitor_by_id({"monitor_sn": monitor_sn})
    if not monitor:
        return redirect("/it/monitors")
    
    if session["user"]["role"] == "admin":
        full_name = session["user"]["username"].capitalize()
        return render_template(
            "admin/inventory/edit/monitor.html",
            monitor = monitor,
            full_name=full_name
        )
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    total_reuest = Hrs.total_request()
    
    return render_template(
        "it/inventory/edit/monitor.html",
        monitor = monitor,
        full_name=full_name,
        total_reuest=total_reuest
    )


@app.route("/it/monitors/delete/<string:monitor_sn>", methods=['DELETE'])
def inventory_monitor_delete(monitor_sn):
    if "user" not in session:
        return redirect("/login")
    if session["user"]["role"] not in ["it", "admin"]:
        return redirect("/login")
    if request.method == "DELETE":
        Monitor.delete_monitor({"monitor_sn": monitor_sn})
    return redirect("/it/monitors")
