# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from ast import literal_eval
from utils import random_partition


class CountGenerator(models.TransientModel):
    _name = 'count.generator'
    _description = 'Count Generator'

    till = fields.Many2one('cash.register')
    odoo_draft = fields.Text()

    balance = fields.Float()
    state = fields.Selection([
        ('before', 'before'),
        ('after', 'after')
    ], default='before')

    fifties = fields.Integer()
    hundreds = fields.Integer()
    two_hundreds = fields.Integer()
    five_hundreds = fields.Integer()

    def compute_till(self):
        hand_selected = [
            ('fifties', 5000),
            ('hundreds', 10000),
            ('two_hundreds', 20000),
            ('five_hundreds', 50000)
        ]
        cent_balance = int(100*self.balance)
        selected_balance = 0
        value_dict = {}
        for f, v in hand_selected:
            selected_balance += getattr(self, f)*v
            value_dict[f] = getattr(self, f)

        if selected_balance > cent_balance:
            raise ValidationError("The denominations you have "
                                  "selected is greater than the balance")

        cent_balance -= selected_balance
        denominations = [
            'one_cent',
            'two_cent',
            'five_cent',
            'ten_cent',
            'twenty_cent',
            'fifty_cent',
            'ones',
            'twos',
            'fives',
            'tens',
            'twenties',
        ]
        values = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000]
        x = random_partition(cent_balance, values)
        value_dict.update({k: x[v] for k, v in zip(denominations, values)})
        value_dict['till_id'] = self.till.id
        self.write({'state': 'after', 'odoo_draft': value_dict})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'count.generator',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def confirm_result(self):
        new_count = self.env['cash.count'].create(literal_eval(self.odoo_draft))
        return {
            'view_id': False,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cash.count',
            'res_id': new_count.id,
            'type': 'ir.actions.act_window',
        }

    def reset_form(self):
        self.write({'state': 'before'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'count.generator',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
