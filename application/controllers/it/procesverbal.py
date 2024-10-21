from flask import render_template, redirect, request, session

from application import app
from application.helpers.procesverbal_pdf import PDFGenerator
from application.models.hrs import Hrs
from application.models.pc_action import PC_Action


@app.route('/procesverbal')
def procesverbal():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    pc_actions = PC_Action.get_all_pc_actions()
    split_name = session['user']["username"].split(".")
    full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    total_reuest = Hrs.total_request()
    
    return render_template(
        "it/procesverbal.html",
        pc_actions = pc_actions,
        full_name=full_name,
        total_reuest=total_reuest
    )


@app.route('/procesverbal/dorzim/<int:pc_action_id>')
def procesverbal_dorzim(pc_action_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "receptionist"]:
        return redirect("/login")
    
    procesverbal_data = PC_Action.procesverbal_data({"pc_action_id": pc_action_id})
    title = "Dorezim Mjetesh"
    PDFGenerator.generate_procesverbal_pdf(procesverbal_data, title)
    
    if session["user"]["role"] == "it":
        return redirect("/procesverbal")
    else:
        return redirect("/receptionist/procesverbal")


@app.route('/procesverbal/rikthim/<int:pc_action_id>')
def procesverbal_rikthim(pc_action_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] in ["it", "receptionist"]:
        return redirect("/login")
    
    procesverbal_data = PC_Action.procesverbal_data({"pc_action_id": pc_action_id})
    title = "Rikthim Mjetesh"
    PDFGenerator.generate_procesverbal_pdf(procesverbal_data, title)
    
    if session["user"]["role"] == "it":
        return redirect("/procesverbal")
    else:
        return redirect("/receptionist/procesverbal")
