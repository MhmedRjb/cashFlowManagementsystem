from flask import request ,redirect ,Blueprint , request   ,redirect ,g
from datetime import datetime ,timedelta
import ast
from ...components import dbstring as dbi
from ..main.date_check_required import date_check_required
from datetime import datetime

CFinsertfunctions_bp=Blueprint('CFinsertfunctions',__name__)

def get_current_date():
    return (datetime.now() + timedelta(days=0)).date()

def is_valid_number(value):
    try:
        float(value)
        print('hi')
        return True
    except ValueError:
        print('bi')
        return False

class func ():
    @CFinsertfunctions_bp.route('/update_paid', methods=['POST'])
    @date_check_required(add_days=15)

    def update_paid():
        # get the InvoiceID and Paid values from the form
        invoice_ids = request.form.getlist('invoice_id')
        paid_values = request.form.getlist('paid')
        getpaid_values = request.form.getlist('getpaid')
        real_date_values=request.form.getlist('real_date')
        previous_page = request.form['previous_page']
        print(previous_page)

        for invoice_id, paid ,getpaid ,realDate in zip(invoice_ids, paid_values,getpaid_values,real_date_values):
            invoice_id_tuple = ast.literal_eval(invoice_id)

            if is_valid_number(paid) :
                g.db_access.update_data_in(dbi.MAIN_SALES_ENTRY, {dbi.paid: paid}, dbi.INVOICEID, invoice_id_tuple)

            if realDate == "None" and is_valid_number(getpaid)  :  
                g.db_access.update_data_in(dbi.MAIN_SALES_ENTRY, {dbi.GETPAID: getpaid}, dbi.INVOICEID, invoice_id_tuple)
                
        return redirect(previous_page)
