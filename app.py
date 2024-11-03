from flask import Flask, render_template, request, send_file
from random import randint
import qrcode
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/qr_codes'

# Ensure the QR code directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    # Generate a random ticket number
    ticket_number = f"CM{randint(100000, 999999)}"
    qr_data = f"Chennai Metro Ticket\nTicket No: {ticket_number}"

    # Generate QR Code
    qr = qrcode.make(qr_data)
    qr_filename = f"{ticket_number}.png"
    qr_path = os.path.join(app.config['UPLOAD_FOLDER'], qr_filename)
    qr.save(qr_path)

    return render_template('ticket.html', ticket_number=ticket_number, qr_filename=qr_filename)

@app.route('/download_qr/<filename>')
def download_qr(filename):
    qr_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(qr_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
