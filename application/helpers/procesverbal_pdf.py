from datetime import datetime
import os

import pdfkit

from flask import render_template, send_file


class PDFGenerator:
    @staticmethod
    def generate_procesverbal_pdf(data, pdf_title):
        # Render the HTML template
        date = datetime.now().strftime("%d/%m/%Y")
        time = datetime.now().strftime("%H:%M")
        rendered_html = render_template(
            'pdf/procesverbal_dorzim.html',
            pdf_title=pdf_title.upper(),
            date=date.upper(),
            time=time.upper(),
            serial_nr=data.get('serial_nr', '__________').upper(),
            model=data.get('model', '__________').upper(),
            cpu=data.get('cpu', '__________').upper(),
            ram=data.get('ram', '__________').upper(),
            storage_type=data.get('storage_type', '__________').upper(),
            storage_value=data.get('storage_value', '__________').upper(),
            monitor_sn=data.get('monitor_sn', '__________').upper(),
            monitor_model=data.get('monitors.model', '__________').upper(),
            size=data.get('size', '__________'),
            adapter_model=data.get('adapter_model', '__________').upper(),
            adapter_sn=data.get('adapter_sn', '__________').upper(),
            headset_model=data.get('headset_model', '__________').upper(),
            headset_sn=data.get('headset_sn', '__________').upper(),
            mouse=data.get('mouse', 'No').upper(),
            keyboard=data.get('keyboard', 'No').upper(),
            dp_vga=data.get('dp_vga', '__________').upper(),
            ac=data.get('ac', '__________').upper(),
            lan=data.get('lan', '__________').upper(),
            employer_name=data.get('username', '__________').upper(),
            employee_name=f"{data['first_name'].upper()} {data['last_name'].upper()}"
        )

        # Create a timestamped file name
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{pdf_title}_{data['first_name']}_{data['last_name']}_{date}.pdf"

        # Define the Downloads folder
        home_dir = os.path.expanduser("~")
        downloads_folder = os.path.join(home_dir, "Downloads")

        # Ensure the folder exists
        if not os.path.exists(downloads_folder):
            os.makedirs(downloads_folder)

        # PDF file path
        pdf_file_path = os.path.join(downloads_folder, file_name)

        # Generate the PDF using pdfkit
        pdfkit.from_string(rendered_html, pdf_file_path)

        # Serve the file for download
        return send_file(pdf_file_path, as_attachment=True)
