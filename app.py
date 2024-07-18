from flask import Flask, render_template, request, redirect, url_for, send_file
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/')
def index():
    return redirect(url_for('merge_page'))

@app.route('/merge')
def merge_page():
    return render_template('merge.html', merged_filename=None)

@app.route('/split')
def split_page():
    return render_template('split.html', split_filename=None)

@app.route('/compress')
def compress_page():
    return render_template('compress.html', compressed_filename=None)

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    files = request.files.getlist('files')
    file_paths = []
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        file_paths.append(file_path)

    merger = PdfMerger()
    for file_path in file_paths:
        pdf_data = PdfReader(file_path)
        merger.append(pdf_data)

    merged_filename = 'merged.pdf'
    merger.write(merged_filename)
    merger.close()

    for file_path in file_paths:
        os.remove(file_path)

    return render_template('merge.html', merged_filename=merged_filename)

@app.route('/split', methods=['POST'])
def split_pdfs():
    file = request.files['file']
    start_page = int(request.form['start_page']) - 1
    end_page = int(request.form['end_page'])

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    pdf_reader = PdfReader(file_path)
    pdf_writer = PdfWriter()

    for page_num in range(start_page, end_page):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    split_filename = 'split.pdf'
    with open(split_filename, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    os.remove(file_path)

    return render_template('split.html', split_filename=split_filename)


@app.route('/compress', methods=['POST'])
def compress_pdf():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    pdf_reader = PdfReader(file_path)
    pdf_writer = PdfWriter()

    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    compressed_filename = 'compressed.pdf'
    with open(compressed_filename, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    os.remove(file_path)

    return render_template('compress.html', compressed_filename=compressed_filename)

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
