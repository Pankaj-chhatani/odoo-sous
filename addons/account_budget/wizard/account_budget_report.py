# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
from openerp.osv import fields, osv


class account_budget_report(osv.osv_memory):

    _name = "account.budget.report"
    _description = "Account Budget report for analytic account"
    _columns = {
        'date_from': fields.date('Start of period', required=True),
        'date_to': fields.date('End of period', required=True),
    }
    _defaults = {
        'date_from': lambda *a: time.strftime('%Y-01-01'),
        'date_to': lambda *a: time.strftime('%Y-%m-%d'),
    }

    def check_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, context=context)[0]
        datas = {
            'ids': context.get('active_ids', []),
            'model': 'account.budget.post',
            'form': data
        }
        datas['form']['ids'] = datas['ids']
        datas['form']['report'] = 'analytic-full'
        return self.pool['report'].get_action(cr, uid, [], 'account_budget.report_budget', data=datas, context=context)
