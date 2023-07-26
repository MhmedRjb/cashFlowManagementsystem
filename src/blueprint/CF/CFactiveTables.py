from flask import Blueprint, render_template
from datetime import datetime ,timedelta
from src.data.databaseIniti import exporter
from src.components import sqlcommonds as sqlcom
from datetime import datetime ,timedelta
from flask_weasyprint import HTML
from flask import make_response, render_template
from src.blueprint.CF.reportsDataFUNC import get_current_date



CFactiveTables_bp = Blueprint('CFactiveTables', __name__,url_prefix='/Elfateh/main/reports/cashflow')

@CFactiveTables_bp.route('/display_dataclints_data')
def display_data():
    data = exporter.readsql(sqlcom.export_clints_data)
    return render_template('entrytable.html', data=data)


@CFactiveTables_bp.route('')
@CFactiveTables_bp.route('/display_goodstransectionte')
def display_goodstransectionte():    
    data = exporter.readsql(  sqlcom.export_cashflow_gby_Acc_NmANDtr_dt)

    current_date = get_current_date()
    return render_template('entrytable.html', data=data, current_date=current_date)

@CFactiveTables_bp.route('/display_all_goodstransectionte')
def display_all_goodstransectionte():

    data = exporter.readsql(
        sqlcom.export_cashflow_fby_afterTODAY
        )
    current_date = get_current_date()
    return render_template('entrytable.html', data=data, current_date=current_date)

@CFactiveTables_bp.route('/display_cashflowgroup__comapnyname')
def cashflowgroup__comapnyname():
    data = exporter.readsql(sqlcom.export_cashflow_gby_comapnyname)
    current_date = get_current_date()
    return render_template('entrytable.html', data=data, current_date=current_date)

@CFactiveTables_bp.route('/display_goodstransectionte_summary')
def display_goodstransectionte_summary():
    data = exporter.readsql(sqlcom.export_cashflow_report)
    current_date = get_current_date()
    return render_template('summarytable.html', data=data, current_date=current_date)


