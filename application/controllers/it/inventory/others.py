from flask import redirect, render_template, request, session

from application import app
from application.models.other import Other


@app.route("/it/others")
def inventory_other():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    others = Other.get_all_others()
    return render_template(
        "it/inventory/others.html",
        others = others
    )


@app.route("/it/others/edit/<int:other_id>", methods=["GET", "POST"])
def inventory_other_edit(other_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
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
    return render_template(
        "it/inventory/edit/other.html",
        other = other
    )


@app.route("/it/others/delete/<int:other_id>", methods=['DELETE'])
def inventory_other_delete(other_id):
    if "user" not in session:
        return redirect("/login")
    if session["user"]["role"] != "it":
        return redirect("/login")
    if request.method == "DELETE":
        Other.delete_monitor({"other_id": other_id})
    return redirect("/it/others")
