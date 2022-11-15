from flask import Blueprint, render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from . import create_app as app
from PyPDF2 import PdfFileReader, PdfFileWriter

views = Blueprint('views', __name__)

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in app().config['ALLOWED_EXTENSIONS']

def modify_pdf(request, file):
  pageNo = request.form.get('page')
  angle = request.form.get('angle')
  filename = secure_filename(file.filename)
  final_name = f'{filename[:-4]}_rotated_{pageNo}_by_{angle}.pdf'
  new_file = open(os.path.join(app().instance_path, final_name), 'wb')
  
  pdf = PdfFileReader(file)
  final_pdf = PdfFileWriter()
  total_pages = pdf.numPages
  
  for page in range(0, total_pages):
    pdf_page = pdf.getPage(page)
    if page == int(pageNo)-1:
      pdf_page.rotateClockwise(int(angle))
    final_pdf.addPage(pdf_page)
  
  final_pdf.write(new_file)
  new_file.close()
  return final_name

@views.route('/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    if 'file' not in request.files:
      flash('No file found', category='danger')
      return redirect(request.url)
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = modify_pdf(request, file)
      return redirect(url_for('views.download_file', name=filename))
    else:
      flash('Please upload a pdf file.', category='danger');
  return render_template('home.html')

@views.route('/download_file/<name>')
def download_file(name):
  return send_from_directory(app().instance_path, name)