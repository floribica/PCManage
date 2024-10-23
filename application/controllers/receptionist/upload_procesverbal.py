from flask import flash, render_template, redirect, request, session, url_for
import os
from application import app
from application.helpers.procesverbal_pdf import PDFGenerator
from application.models.pc_action import PC_Action
from application.models.upload import Upload

# Define the upload folder for PDF files
UPLOAD_FOLDER_PROCESSVERBAL = os.getenv('UPLOAD_FOLDER_PROCESSVERBAL')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_PROCESSVERBAL

# Allowed file extensions
ALLOWED_EXTENSIONS_PROCESSVERBAL = os.getenv('ALLOWED_EXTENSIONS_PROCESSVERBAL').split(',')

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PROCESSVERBAL[0]

# Route to display the request history and handle the upload form
@app.route('/receptionist/procesverbal', methods=['GET', 'POST'])
def receptionist_procesverbal():
    if "user" not in session:
        return redirect("/login")
    if session["user"]["role"] not in ["admin", "receptionist"]:
        return redirect("/login")
    
    # Get all PC actions to display in the table
    pc_actions = PC_Action.get_all_pc_actions()
    
    # Create the full name from the username in the session
    if session["user"]["role"] == "admin":
        full_name = session['user']["username"].capitalize()
    else:
        split_name = session['user']["username"].split(".")
        full_name = split_name[0].capitalize() + " " + split_name[1].capitalize()
    
    # Handle the PDF upload if the request method is POST
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'pdf_file' not in request.files:
            flash('No file part', "upload_error")
            return redirect(request.referrer)
        
        file = request.files['pdf_file']
        pc_action_id = request.form['pc_action_id']  # Get the PC action ID from the form
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Rename the file to include the PC action ID
            filename = f"{pc_action_id}_{file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)  # Save the file to the uploads folder
            
            uploaded_data = {
                'pc_action_id': pc_action_id,
                'file': filepath
            }
            
            Upload.upload_procesverbal(uploaded_data)
            
            flash('PDF uploaded successfully!')
            return redirect(url_for('receptionist_procesverbal'))
        
        flash('File type not allowed. Only PDF files are accepted.')
        return redirect(request.url)
    
    # Render the template for receptionist with the list of PC actions
    if session["user"]["role"] == "admin":
        return render_template(
            "admin/procesverbal.html",
            pc_actions=pc_actions,
            full_name=full_name
        )
    return render_template(
        "receptionist/upload_procesverbal.html",
        pc_actions=pc_actions,
        full_name=full_name
    )

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER_PROCESSVERBAL):
    os.makedirs(UPLOAD_FOLDER_PROCESSVERBAL)
    

@app.route('/receptionist/close/<int:pc_action_id>')
def receptionist_close_case(pc_action_id):
    if "user" not in session:
        return redirect("/login")
    if session["user"]["role"] in ["admin", "receptionist"]:
        return redirect("/login")
    
    PC_Action.close_case({"pc_action_id": pc_action_id})
    
    return redirect("/receptionist/procesverbal")
