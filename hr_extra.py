# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

from datetime import datetime
import itertools
from openerp import tools
from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _

import time
import math
import random
from datetime import datetime ,timedelta
from dateutil.relativedelta import relativedelta
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class time_adjustment(osv.Model):
    _name = 'time.adjustment'
    _columns = {
        'name' : fields.datetime('Time From'),
        'time_to' : fields.datetime('Time To'),
        'time_h' : fields.integer('H'),
        'time_m' : fields.integer('M'),
        'opration' : fields.selection([('-','-'),('+','+')],'Operator'),
        'address_id' : fields.many2one('res.partner','Working Address'),
        'lines' : fields.one2many('time.adjustment.line','time_adjustment_id','Employee List'),
    }

    def approve_update_punch(self,cr,uid,ids,context=None):
        print "Inside Function"
        time_h = self.browse(cr,uid,ids).time_h
        time_m = self.browse(cr,uid,ids).time_m
        for each in self.browse(cr,uid,ids).lines:
            print "===========",each,each.in_time,each.out_time
            employee_id = each.employee_id.id
            date_from = each.in_time
            date_to = each.out_time

            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            
            date_from = datetime.strptime(date_from, DATETIME_FORMAT)
            date_to = datetime.strptime(date_to, DATETIME_FORMAT)

            date_from = date_from + timedelta(hours=5,minutes=30)
            date_to = date_to + timedelta(hours=5,minutes=30)
            
            date = datetime.strptime((date_from.strftime('%Y-%m-%d')),"%Y-%m-%d").date()

            date_from = datetime.strftime(date_from,'%Y-%m-%d %H:%M:%S')
            date_to = datetime.strftime(date_to,'%Y-%m-%d %H:%M:%S')
            print "===========",each,date_from,date_to,employee_id
            attendance_ids = self.pool.get('hr.attendance').search(cr,uid,[('name','>=',each.in_time),('name','<=',each.out_time),('employee_id','=',employee_id)])
            if attendance_ids:
                for each_atten in self.pool.get('hr.attendance').browse(cr,uid,attendance_ids):
                    atten_time = each_atten.name
                    atten_time = datetime.strptime(atten_time, DATETIME_FORMAT)
                    atten_time = atten_time + timedelta(hours=5,minutes=30)
                    print "===========",atten_time

            error

class time_adjustment_line(osv.Model):
    _name = 'time.adjustment.line'
    _columns = {
        'time_adjustment_id' : fields.many2one('time.adjustment','Time Adjustment'),
        'employee_id' : fields.many2one('hr.employee','Employee'),
        'in_time' : fields.datetime('In Punch'),
        'out_time' : fields.datetime('Out Punch'),
        'category': fields.selection([('worker', 'Worker'), ('staff', 'Staff'), ('contractor', 'Contractor')], 'Category'),
        'address_id' : fields.many2one('res.partner', 'Working Address'),
    }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
