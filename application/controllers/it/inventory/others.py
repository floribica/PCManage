from flask import redirect, render_template, request, session

from application import app
from application.models.hrs import Hrs
from application.models.other import Other


@app.route("/it/others")
def inventory_other():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    
    if session["user"]["role"] == "admin":
        full_name = session["user"]["username"].capitalize()
        others = Other.get_all_others()
        return render_template(
            "admin/inventory/others.html",
            others = others,
            full_name=full_name
        )
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    total_reuest = Hrs.total_request()
    others = Other.get_all_others()
    return render_template(
        "it/inventory/others.html",
        others = others,
        full_name=full_name,
        total_reuest=total_reuest
    )


@app.route("/it/others/edit/<int:other_id>", methods=["GET", "POST"])
def inventory_other_edit(other_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "admin"]:
        return redirect("/login")
    if request.method == "POST":
        other_data = {
            "other_id": other_id,
            "mouse": request.form.get("mouse"),
            "keyboard": request.form.get("keyboard"),
            "dp_vga": request.form.get("dp_vga"),
            "ac": request.form.get("ac"),
            "lan": request.form.get("lan")
        }
        if not Other.validate_other(other_data):
            return redirect(f"/it/others/edit/{other_id}")
        Other.update_other(other_data)
        return redirect("/it/others")
    
    other = Other.get_other_by_id({"other_id": other_id})
    if not other:
        return redirect("/it/others")
    
    if session["user"]["role"] == "admin":
        full_name = session["user"]["username"].capitalize()
        return render_template(
            "admin/inventory/edit/other.html",
            other = other,
            full_name=full_name
        )
    
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    total_reuest = Hrs.total_request()
    
    return render_template(
        "it/inventory/edit/other.html",
        other = other,
        full_name=full_name,
        total_reuest=total_reuest
    )


@app.route("/it/others/delete/<int:other_id>", methods=['DELETE'])
def inventory_other_delete(other_id):
    if "user" not in session:
        return redirect("/login")
    if session["user"]["role"] not in ["it", "admin"]:
        return redirect("/login")
    if request.method == "DELETE":
        Other.delete_monitor({"other_id": other_id})
    return redirect("/it/others")
