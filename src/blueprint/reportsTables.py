from flask import Blueprint, render_template
from datetime import datetime ,timedelta
from src.data.databaseIniti import exporter
from src.components import sqlcommonds as sqlcom
from flask import Flask, render_template 
from datetime import datetime ,timedelta
from flask_weasyprint import HTML
from flask import make_response, render_template


def get_current_date(days:int = 0):
    return (datetime.now() + timedelta(days)).date()

displaytables_bp = Blueprint('displaytables', __name__)

@displaytables_bp.route('/Elfateh/main/reports/cashflow/display_dataclints_data')
def display_data():
    data = exporter.readsql(sqlcom.export_clints_data)
    return render_template('entrytable.html', data=data)


@displaytables_bp.route('/Elfateh/main/reports/cashflow')
@displaytables_bp.route('/Elfateh/main/reports/cashflow/display_goodstransectionte')
def display_goodstransectionte():    
    data = exporter.readsql(  sqlcom.export_cashflow_gby_Acc_NmANDtr_dt)

    current_date = get_current_date()
    return render_template('entrytable.html', data=data, current_date=current_date)

@displaytables_bp.route('/Elfateh/main/reports/cashflow/display_all_goodstransectionte')
def display_all_goodstransectionte():

    data = exporter.readsql(
        sqlcom.export_cashflow_fby_afterTODAY
        )
    current_date = get_current_date()
    return render_template('entrytable.html', data=data, current_date=current_date)

@displaytables_bp.route('/Elfateh/main/reports/cashflow/display_cashflowgroup__comapnyname')
def cashflowgroup__comapnyname():
    data = exporter.readsql(sqlcom.export_cashflow_gby_comapnyname)
    current_date = get_current_date()
    return render_template('entrytable.html', data=data, current_date=current_date)

@displaytables_bp.route('/Elfateh/main/reports/cashflow/display_goodstransectionte_summary')
def display_goodstransectionte_summary():
    data = exporter.readsql(sqlcom.export_cashflow_report)
    current_date = get_current_date()
    return render_template('summarytable.html', data=data, current_date=current_date)


@displaytables_bp.route('/Elfateh/main/print/cashflow')
def extractPDFofgoodstransectionte_summary():
    # Retrieve the data from the goodstransectionte table
    data = exporter.readsql(sqlcom.export_cashflow_report)
    column_names = ['اسم الشركة ', 'معاد الأستحقاق ', 'الإجمالي']
    reprot_type='تقرير داخلي'
    report_number='2'
    report_author='أحمد الستري'
    report_date=get_current_date()

    # Render the HTML template with the data
    html = render_template('pdf.html', data=data, column_names=column_names,
                            reprot_type=reprot_type,report_number=report_number,report_author=
                            report_author,report_date=report_date)

    # Generate the PDF
    pdf = HTML(string=html).write_pdf()
    # Create a response object with the PDF data
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={report_date}_cashflowtreport.pdf'

    return response

