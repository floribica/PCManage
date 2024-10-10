from flask import redirect, render_template, request, session

from application import app
from application.models.monitor import Monitor


@app.route("/it/monitors")
def inventory_monitors():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    monitors = Monitor.get_all_monitors()
    return render_template(
        "it/inventory/monitors.html",
        monitors = monitors
    )
    

@app.route("/it/monitors/edit/<int:monitor_id>", methods=["GET", "POST"])
def inventory_monitor_edit(monitor_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    if request.method == "POST":
        monitor_data = {
            "monitor_id": monitor_id,
            "model": request.form["model"],
            "model_sn": request.form["model_sn"],
            "size": request.form["size"]
        }
        if not Monitor.validate_monitor(monitor_data):
            return redirect(f"/it/monitors/edit/{monitor_id}")
        Monitor.update_monitor(monitor_data)
        return redirect("/it/monitors")
    
    monitor = Monitor.get_monitor_by_id({"monitor_id": monitor_id})
    if not monitor:
        return redirect("/it/monitors")
    return render_template(
        "it/inventory/edit/monitor.html",
        monitor = monitor
    )


@app.route("/it/monitors/delete/<int:monitor_id>", methods=['DELETE'])
def inventory_monitor_delete(monitor_id):
    if "user" not in session:
        return redirect("/login")
    if session["user"]["role"] != "it":
        return redirect("/login")
    if request.method == "DELETE":
        Monitor.delete_monitor({"monitor_id": monitor_id})
    return redirect("/it/monitors")
