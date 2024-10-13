from datetime import datetime
import os

import pdfkit

from flask import render_template, send_file


class PDFGenerator:
    @staticmethod
    def generate_procesverbal_pdf(data, pdf_title):
        # Render the HTML template
        rendered_html = render_template(
            'pdf/procesverbal_dorzim.html',
            pdf_title=pdf_title,
            date=data.get('created_date', '___/___/_______').strftime("%d/%m/%Y"),
            time=data.get('rikthim_date', '___:____').strftime("%H:%M"),
            serial_nr=data.get('serial_nr', 'N/A'),
            model=data.get('model', 'N/A'),
            cpu=data.get('cpu', 'N/A'),
            ram=data.get('ram', 'N/A'),
            storage_type=data.get('storage_type', 'N/A'),
            storage_value=data.get('storage_value', 'N/A'),
            monitor_sn=data.get('monitor_sn', 'N/A'),
            monitor_model=data.get('monitors.model', 'N/A'),
            size=data.get('size', 'N/A'),
            adapter_model=data.get('adapter_model', 'N/A'),
            adapter_sn=data.get('adapter_sn', 'N/A'),
            headset_model=data.get('headset_model', 'N/A'),
            headset_sn=data.get('headset_sn', 'N/A'),
            mouse=data.get('mouse', 'No'),
            keyboard=data.get('keyboard', 'No'),
            dp_vga=data.get('dp_vga', 'N/A'),
            ac=data.get('ac', 'N/A'),
            lan=data.get('lan', 'N/A'),
            employer_name=data.get('username', 'N/A'),
            employee_name=f"{data['first_name']} {data['last_name']}",
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
