# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time
import math
import random
from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime ,timedelta
from dateutil.relativedelta import relativedelta
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import base64
import openerplib
import xlrd
import time
import StringIO
import cStringIO

class hr_employee_import_wizard(osv.osv_memory):
    _name = 'hr.employee.import.wizard'
    _columns = {
                'name':fields.char('File Name',size=128),
                'import_data':fields.binary('CSV File'),
    }  
    def import_record(self, cr, uid, ids, context=None):
        emp_pool = self.pool.get('hr.employee')
        slip_pool = self.pool.get('hr.payslip')
        run_pool = self.pool.get('hr.payslip.run')
        contract_pool = self.pool.get('hr.contract')
        attendance_obj = self.pool.get('hr.attendance')
        time_line = self.pool.get('time.adjustment.line')
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            
        

        slip_ids = []
        if context is None:
            context = {}
        active_id = context.get('active_id')
        parent_obj = self.pool.get('time.adjustment').browse(cr,uid,active_id)
        data = self.read(cr, uid, ids, context=context)[0]
        for batch in self.browse(cr ,uid, ids):
            run_data = {}
            if batch.import_data:
                val=base64.decodestring(batch.import_data)
                fp = StringIO.StringIO()
                fp.write(val)
                wb = xlrd.open_workbook(file_contents=fp.getvalue())
                wb.sheet_names()
                sheet_name=wb.sheet_names()
                sh = wb.sheet_by_index(0)
                sh = wb.sheet_by_name(sheet_name[0])
                n_rows=sh.nrows
                n_cols=sh.ncols
                date_from = parent_obj.name
                date_to = parent_obj.time_to
                address_id = parent_obj.address_id.id
                date_from = datetime.strptime(date_from, DATETIME_FORMAT)
                date_to = datetime.strptime(date_to, DATETIME_FORMAT)

                # date_from = date_from + timedelta(hours=5,minutes=30)
                # date_to = date_to + timedelta(hours=5,minutes=30)
                
                # date = datetime.strptime((date_from.strftime('%Y-%m-%d')),"%Y-%m-%d").date()

                date_from = datetime.strftime(date_from,'%Y-%m-%d %H:%M:%S')
                date_to = datetime.strftime(date_to,'%Y-%m-%d %H:%M:%S')

                print "=====",n_rows
                for row in range(1,n_rows):
                    print row
                    emp_code = name = ' '
                    emp_code = sh.row_values(row)[0]
                    emp_id=self.pool.get('hr.employee').search(cr,uid,[('emp_code','=',str(int(emp_code))),('address_id','=',address_id)])
                    if emp_id:
                        print emp_code,emp_id,date_from,date_to
                        attendance_ids = self.pool.get('hr.attendance').search(cr,uid,[('name','>=',date_from),('name','<=',date_to),('employee_id','=',emp_id[0])])
                        if attendance_ids:
                            print emp_code,emp_id,date_from,date_to,attendance_ids
                            # attendance_ids = attendance_ids.sort()
                            print emp_code,emp_id,date_from,date_to,attendance_ids
                            index = len(attendance_ids)
                            if index > 1:
                                out_punch = attendance_obj.browse(cr,uid,attendance_ids[0]).name
                                address_id = attendance_obj.browse(cr,uid,attendance_ids[0]).address_id.id
                                category = attendance_obj.browse(cr,uid,attendance_ids[0]).category
                                in_punch = attendance_obj.browse(cr,uid,attendance_ids[index-1]).name
                                if attendance_ids:
                                    time_line.create(cr,uid,{'employee_id':emp_id[0],'in_time':in_punch,'out_time':out_punch,'time_adjustment_id':active_id,'address_id':address_id,'category':category},context=None)

                        # name=str(emp_code) +'/' + str(batch.month_id.name)
                        # if emp_id:   
                        #     deduction_pool.create(cr,uid,{'deduction_date':date,'name':name,'month_id':batch.month_id.id,'employee_id':emp_id[0],'deduction_type':batch.deduction_type,'deduction_amount':float(amount)})
                        
        return True
                        
                        
                          