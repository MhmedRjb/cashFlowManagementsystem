from flask import Blueprint ,g
from flask import redirect ,url_for
from src.components.readexcel import readexcel as excel2sql
import src.components.dbstring as dbi 
from src.components import filepaths as fpth
from src.components.sqlcommonds import callupdateCashflow_excelPRoducer
from ..main.date_check_required import date_check_required
from datetime import datetime

CFstartButtons_bp = Blueprint('CFstartButtons', __name__,url_prefix='/comapny_name/main/reports/cashflow')

@CFstartButtons_bp.route('/export_datagood_transection', methods=['POST','GET'])
@date_check_required(add_days=15)
def export_goodstransectiontedata():
    expected_cols_goods_transection = ['Acc_Nm' ,'Itm_cd', 'TR_NO']
    processor_goods_transection =excel2sql(fpth.goodstransectionte_filepath, expected_cols_goods_transection)
    processor_goods_transection.read_data()
    data = processor_goods_transection.data.fillna(value=0)
    g.db_access.export_data_first(data, dbi.cashflow_excelINsql)
    return redirect(url_for('FileHandler.home', message='Data exported successfully!'))


@CFstartButtons_bp.route('/export_clints_data', methods=['POST','GET'])
@date_check_required(add_days=15)

def export_data_clients():
    expected_cols_goods_transection = ['acc_nm']
    processor_goods_transection =excel2sql(fpth.clientsdb_filephath, expected_cols_goods_transection)
    processor_goods_transection.read_data()
    g.db_access.export_data_first(processor_goods_transection.data, dbi.clients_excelINsql)
    return redirect(url_for('FileHandler.home', message='Data exported successfully!'))
    
@CFstartButtons_bp.route('/delete_dataFromDataBasegood_transection', methods=['POST','GET'])
@date_check_required(add_days=15)
def updatethedata():
    g.db_access.call_sql('CALL update_main_sales_entry()')
    return redirect(url_for('FileHandler.home', message='Data updated successfully!'))


