# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    invoice_id = fields.Many2one("account.move", string="Invoice")

class Stock_move(models.Model):
    _inherit = 'stock.move'

    invoice_line_id = fields.Many2one("account.move.line", string="Invoice line")
