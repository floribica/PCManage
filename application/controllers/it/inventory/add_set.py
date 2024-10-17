from flask import flash, redirect, render_template, request, session

from application import app
from application.helpers.defaul_data.yaml_config import load_config_yaml
from application.models.computer import Computer
from application.models.headset import Headset
from application.models.hrs import Hrs
from application.models.monitor import Monitor
from application.models.other import Other
from application.models.pc_action import PC_Action


@app.route("/it/add/set", methods=["POST"])
def inventory_pc_add_set():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    pc_action_data = {
        "hr_id": request.form["hr_id"]
    }
    
    computer_data = {
        "serial_nr": request.form["serial_nr"],
        "model": request.form["pc_model"],
        "cpu": request.form["cpu"],
        "ram": request.form["ram"],
        "storage_type": request.form["storage_type"],
        "storage_value": request.form["storage_value"]
    }
    
    monitor_data = {
        "monitor_sn": request.form["monitor_sn"],
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
    
    if not pc_action_data["hr_id"]:
        flash("HR ID is required.", "add_set")
        return redirect("/it/search/set")
    
    if not Computer.validate_computer(computer_data) and not Monitor.validate_monitor(monitor_data) and not Headset.validate_headset(headset_data):
        return redirect("/it/search/set")
    
    Computer.add_computer(computer_data)
    Monitor.add_monitor(monitor_data)
    Headset.add_headset(headset_data)
    Other.add_other(other_data)
    
    fushata = Hrs.get_operator_info(pc_action_data)
    headset_id = Headset.get_headset_id(headset_data)
    other_id = Other.get_other_id(other_data)
    if not fushata or not headset_id or not other_id:
        return redirect("/it/search/set")
    
    pc_action_data["fushata"] = fushata["fushata"]
    pc_action_data["computer_sn"] = computer_data["serial_nr"]
    pc_action_data["monitor_sn"] = monitor_data["monitor_sn"]
    pc_action_data["headset_id"] = headset_id["headset_id"]
    pc_action_data["other_id"] = other_id["other_id"]
    pc_action_data["user_id"] = session["user"]["user_id"]
    
    PC_Action.add_pc_action(pc_action_data)
    Hrs.ready_request(pc_action_data)
    
    return redirect("/it/search/set")


@app.route("/it/search/set", methods=["GET", "POST"])
def inventory_pc_search_set():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()

    if request.method == "POST":
        search_data = {
            "serial_nr": request.form["computer_sn"],
            "monitor_sn": request.form["monitor_sn"],
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
        if not search_data["monitor_sn"]:
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
        
        hrs =Hrs.get_all_approved_request()
        return render_template(
            "it/inventory/add_set.html",
            hrs = hrs,
            computer = computer,
            monitor = monitor,
            headset = headset,
            full_name=full_name
        )

    return render_template(
        "it/inventory/search_set.html",
        full_name=full_name
    )
