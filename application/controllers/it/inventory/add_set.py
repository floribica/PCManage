from flask import flash, redirect, render_template, request, session

from application import app
from application.helpers.defaul_data.yaml_config import load_config_yaml
from application.models.computer import Computer
from application.models.headset import Headset
from application.models.monitor import Monitor


@app.route("/it/add/set", methods=["POST"])
def inventory_pc_add_set():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    computer_data = {
        "serial_nr": request.form["serial_nr"],
        "model": request.form["pc_model"],
        "cpu": request.form["cpu"],
        "ram": request.form["ram"],
        "storage_type": request.form["storage_type"],
        "storage_value": request.form["storage_value"]
    }
    
    monitor_data = {
        "model_sn": request.form["model_sn"],
        "model": request.form["monitor_model"],
        "size": request.form["size"]
    }
    
    headset_data = {
        "adapter_model": request.form["adapter_model"],
        "adapter_sn": request.form["adapter_sn"],
        "headset_model": request.form["headset_model"],
        "headset_sn": request.form["headset_sn"]
    }
    
    other_data = {
        "mouse": request.form["mouse"],
        "keyboard": request.form["keyboard"],
        "dp_vga": request.form["dp_vga"],
        "ac": request.form["ac"],
        "lan": request.form["lan"],
    }

    return redirect("/it/search/set")


@app.route("/it/search/set", methods=["GET", "POST"])
def inventory_pc_search_set():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")

    if request.method == "POST":
        search_data = {
            "serial_nr": request.form["computer_sn"],
            "model_sn": request.form["monitor_sn"],
            "headset_sn": request.form["headset_sn"],
            "adapter_sn": request.form["adapter_sn"],
        }
        #search for computer
        if not search_data["serial_nr"]:
            flash("Computer serial number is required.", "search_set")
            return redirect("/it/search/set")
        else:
            computer = Computer.get_computer_by_serial_nr(search_data)
            if not computer:
                yaml_file = "application/helpers/defaul_data/computer.yaml"
                computer = load_config_yaml(yaml_file)
        #search for monitor
        if not search_data["model_sn"]:
            flash("Monitor serial number is required.", "search_set")
            return redirect("/it/search/set")
        else:
            monitor = Monitor.get_monitor_by_serial_nr(search_data)
            if not monitor:
                yaml_file = "application/helpers/defaul_data/monitor.yaml"
                monitor = load_config_yaml(yaml_file)
        #search for headset or adapter
        if not search_data["headset_sn"] and not search_data["adapter_sn"]:
            flash("Headset or adapter serial number is required.", "search_set")
            return redirect("/it/search/set")
        else:
            headset = Headset.get_headset_by_serial_nr(search_data)
            if not headset:
                yaml_file = "application/helpers/defaul_data/headset.yaml"
                headset = load_config_yaml(yaml_file)
        return render_template(
            "it/inventory/add_set.html",
            computer = computer,
            monitor = monitor,
            headset = headset
        )

    return render_template("it/inventory/search_set.html")
