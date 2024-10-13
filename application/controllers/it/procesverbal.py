from flask import render_template, redirect, request, session

from application import app
from application.helpers.procesverbal_pdf import PDFGenerator
from application.models.pc_action import PC_Action


@app.route('/procesverbal')
def procesverbal():
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    pc_actions = PC_Action.get_all_pc_actions() 
    
    return render_template(
        "it/procesverbal.html",
        pc_actions = pc_actions
    )


@app.route('/procesverbal/dorzim/<int:pc_action_id>')
def procesverbal_dorzim(pc_action_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    procesverbal_data = PC_Action.procesverbal_data({"pc_action_id": pc_action_id})
    title = "Dorezim Mjetesh"
    PDFGenerator.generate_procesverbal_pdf(procesverbal_data, title)
    
    return redirect("/procesverbal")


@app.route('/procesverbal/rikthim/<int:pc_action_id>')
def procesverbal_rikthim(pc_action_id):
    if "user" not in session:
        return redirect("/login")
    if not session["user"]["role"] == "it":
        return redirect("/login")
    
    procesverbal_data = PC_Action.procesverbal_data({"pc_action_id": pc_action_id})
    title = "Rikthim Mjetesh"
    PDFGenerator.generate_procesverbal_pdf(procesverbal_data, title)
    
    return redirect("/procesverbal")
