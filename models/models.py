# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
# from odoo.exceptions import ValidationError
# import re


class CashRegister(models.Model):
    _name = 'cash.register'
    _description = 'Cash Register'

    name = fields.Char(compute='_make_name', store=True)
    make = fields.Char()
    model = fields.Char()
    description = fields.Text()
    image = fields.Binary()
    value = fields.Float()

    owner_id = fields.Many2one('res.company', string="Owner")
    count_ids = fields.One2many('cash.count', 'till_id', string="Cash Counts")

    last_count = fields.Many2one('cash.count', compute='_last_count', store=True)
    last_counted = fields.Date(related='last_count.date', readonly=True)
    last_balance = fields.Monetary(related='last_count.balance', readonly=True)
    currency_id = fields.Many2one(related='last_count.currency_id', readonly=True)

    @api.depends('count_ids')
    def _last_count(self):
        for r in self:
            if r.count_ids:
                r.last_count = r.count_ids.sorted(key=lambda x: x.date)[-1]
    # summary = fields.Char(compute='_summarize')
    #
    # def _summarize(self):
    #     for r in self:
    #         r.summary = r.description[:100] + '...'

    @api.depends('make', 'model')
    def _make_name(self):
        self.name = '%s - %s' % (self.make, self.model)


class TillCount(models.Model):
    _name = 'cash.count'
    _description = 'Till Count'
    _order = 'till_id, date desc'

    name = fields.Char(compute='_make_name', store=True)

    @api.depends('till_id', 'date')
    def _make_name(self):
        for r in self:
            r.name = '%s[%s]' % (r.till_id.name, r.date)

    till_id = fields.Many2one('cash.register', string="Till")
    currency_id = fields.Many2one('res.currency',
                                  string='Currency',
                                  default=lambda x: x.env.ref("base.EUR"))
    date = fields.Date(default=datetime.today().date())

    # Coins
    one_cent = fields.Integer(string="1c")
    two_cent = fields.Integer(string="2c")
    five_cent = fields.Integer(string="5c")
    ten_cent = fields.Integer(string="10c")
    twenty_cent = fields.Integer(string="20c")
    fifty_cent = fields.Integer(string="50c")
    ones = fields.Integer(string="100c")
    twos = fields.Integer(string="200c")

    # Notes
    fives = fields.Integer(string="5 x")
    tens = fields.Integer(string="10 x")
    twenties = fields.Integer(string="20 x")
    fifties = fields.Integer(string="50 x")
    hundreds = fields.Integer(string="100 x")
    two_hundreds = fields.Integer(string="200 x")
    five_hundreds = fields.Integer(string="500 x")

    balance = fields.Monetary(compute='_compute_balance', currency_field='currency_id')
    coin_total = fields.Monetary(compute='_compute_coins', currency_field='currency_id')
    bill_total = fields.Monetary(compute='_compute_bills', currency_field='currency_id')

    @api.depends('coin_total', 'bill_total')
    def _compute_balance(self):
        for r in self:
            r.balance = r.coin_total + r.bill_total

    @api.onchange('one_cent', 'two_cent', 'five_cent', 'ten_cent', 'twenty_cent', 'fifty_cent', 'ones', 'twos')
    def _compute_coins(self):
        coins = [
            ('one_cent', .01),
            ('two_cent', .02),
            ('five_cent', .05),
            ('ten_cent', .1),
            ('twenty_cent', .2),
            ('fifty_cent', .5),
            ('ones', 1),
            ('twos', 2)
        ]
        for r in self:
            r.coin_total = sum(getattr(r, f) * v for f, v in coins)

    @api.onchange('fives', 'tens', 'twenties', 'fifties', 'hundreds', 'two_hundreds', 'five_hundreds')
    def _compute_bills(self):
        bills = [
            'fives',
            'tens',
            'twenties',
            'fifties',
            'hundreds',
            'two_hundreds',
            'five_hundreds',
        ]
        values = [5, 10, 20, 50, 100, 200, 500]
        for r in self:
            r.bill_total = sum(getattr(r, f) * v for f, v in zip(bills, values))
