from src.data.Dataprocessor import DataProcessor as dprs
from src.data.DataBaseConnection import DatabaseExporter as dbcon
from flask import Flask, render_template , request ,flash ,session ,redirect ,url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import  ValidationError,Optional
from werkzeug.utils import secure_filename
import os
from datetime import datetime ,timedelta
from flask_weasyprint import HTML, render_pdf
from src.blueprint.reportsTables import displaytables_bp
from src.data.databaseIniti import exporter
import ast
from src.components import filepaths as fpth

from src.blueprint.cashFlowButtons import cashFlowButtons_bp



app = Flask(__name__)
app.config['SECRET_KEY']='123456789'
app.secret_key = '123456789'
app.register_blueprint(displaytables_bp)
app.register_blueprint(cashFlowButtons_bp)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), r'Excel_files')

def get_current_date():
    return (datetime.now() + timedelta(days=0)).date()

class FileHandler :

    def __init__(self, upload_folder,ALLOWED_EXTENSIONS):
        self.upload_folder = upload_folder
        self.ALLOWED_EXTENSIONS = ALLOWED_EXTENSIONS
    def is_valid_file(self, file):
        if file:
            filename = file.filename
            ext = os.path.splitext(filename)[1]
            print(f'File extension: {ext}')
            return ext in self.ALLOWED_EXTENSIONS
        return False

    def save_file(self, file):
        if self.is_valid_file(file):
            file.save(os.path.join(self.upload_folder, secure_filename(file.filename)))
        else:
            
            raise ValidationError('Invalid file stype. Only .xls and .xlsx files are allowed.')

file_handler = FileHandler(app.config['UPLOAD_FOLDER'], ALLOWED_EXTENSIONS=['.xls', '.xlsx'])
class UploadForm(FlaskForm):
    file = FileField('file2', validators=[Optional(), file_handler.is_valid_file])
    submit = SubmitField('Upload file')

    @app.route('/', methods=['GET', 'POST'])
    @app.route('/Elfateh', methods=['GET', 'POST'])
    @app.route('/Elfateh/main', methods=['GET', 'POST'])
    @app.route('/Elfateh/main/reports', methods=['GET', 'POST'])
    def home():
        form = UploadForm()
        if request.method == 'POST':
            try:
                if form.file.data:
                    file_handler.save_file(form.file.data)

            except ValidationError as e:
                flash(str(e), 'error')

    
        folder_path = fpth.main_folder_path
        folder_contents = []
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            mtime = os.path.getmtime(item_path)
            mtime_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
            folder_contents.append((item, mtime_str))
        return render_template('home.html', folder_contents=folder_contents,form=form)



class func ():
    @app.route('/update_paid', methods=['POST'])
    def update_paid():
        # get the InvoiceID and Paid values from the form
        invoice_ids = request.form.getlist('invoice_id')
        paid_values = request.form.getlist('paid')
        getpaid_values = request.form.getlist('getpaid')
        real_date_values=request.form.getlist('real_date')
        previous_page = request.form['previous_page']

        for invoice_id, paid ,getpaid ,realDate in zip(invoice_ids, paid_values,getpaid_values,real_date_values):
            invoice_id_tuple = ast.literal_eval(invoice_id)
            print(realDate)
            if paid :
                print(exporter.update_data_in('main_sales_entry', {'Paid': paid}, 'InvoiceID', invoice_id_tuple))
                exporter.update_data_in('main_sales_entry', {'Paid': paid}, 'InvoiceID', invoice_id_tuple)
            if realDate == "None" and getpaid  :  
                exporter.update_data_in('main_sales_entry', {'getpaid': getpaid}, 'InvoiceID', invoice_id_tuple)
        return redirect(previous_page)
    

class in_way():
    @app.route('/Elfateh/main/Inventory/')
    def inventory():
        return render_template('commingsoonreports.html')
    
    @app.route('/Elfateh/main/reports/clinets_statistics')
    def clinets_statistics():
        return render_template('commingsoonreports.html')
    
    @app.route('/Elfateh/main/reports/genral_statistics')
    def genral_statistics():
        return render_template('commingsoonreports.html')
    

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
