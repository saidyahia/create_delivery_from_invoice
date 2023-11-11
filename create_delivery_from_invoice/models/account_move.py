# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,api
from datetime import datetime



class AccountMove(models.Model):
    _inherit = 'account.move'
    picking_ids = fields.One2many('stock.picking', 'invoice_id', string='Pickings')
    delivery_count = fields.Integer(string='Delivery Orders', compute='_compute_picking_ids')
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type',domain=[ ('code', '=', 'outgoing')] ,)
    auto_create_delivery = fields.Boolean(default=False,string='Auto Create Delivery',copy=False,   tracking=True,)

    auto_validate_delivey = fields.Boolean(default=False,string='Auto Validate Delivery',copy=False,   tracking=True,)


    def action_post(self):
        res=super(AccountMove,self).action_post()

        for each in self:
            if each.move_type=='out_invoice' and each.picking_type_id:
                Picking = self.env['stock.picking']
                warehouse_obj = self.env['stock.warehouse']
                destination_id=False
                if (not each.picking_type_id) or (not each.picking_type_id.default_location_dest_id):
                    customerloc, supplierloc = warehouse_obj._get_partner_locations()
                    destination_id = supplierloc.id
                else:
                    destination_id = each.picking_type_id.default_location_dest_id.id
                picking = Picking.create(each._get_new_picking_values(destination_id))
                if picking:
                    for each_line in each.invoice_line_ids:
                        move_val={
                            'to_refund':True,
                            'name': each_line.product_id.name,

                            'product_id':each_line.product_id.id,
                            'product_uom_qty': each_line.quantity,
                            'product_uom': each_line.product_uom_id and each_line.product_uom_id.id or False,

                            'location_id': self.picking_type_id.default_location_src_id.id or False,
                            'location_dest_id': destination_id,
                            'invoice_line_id': each_line.id,

                            'picking_id': picking.id}

                        move_line = self.env['stock.move'].create(move_val)



                if  each.auto_validate_delivey:
                    for pick in each.picking_ids:
                        pick.action_confirm()

                        pick.action_assign()
                        pick.button_validate()
                        # from odoo.tests import tagged, Form
                        # wiz_act = pick.button_validate()
                        # wiz = Form(self.env[wiz_act['res_model']].with_context(wiz_act['context'])).save()
                        # wiz.process()


        return res
    def _get_new_picking_values(self,destination_id):
        return {
            'invoice_id': self.id,
            'scheduled_date':datetime.now(),
            'origin': self.name,
            'company_id': self.company_id.id,
            'move_type':  'direct',
            'partner_id': self.partner_id.id,
            'picking_type_id': self.picking_type_id.id,
            'location_id': self.picking_type_id.default_location_src_id.id or False,
            'location_dest_id': destination_id,
        }

    @api.depends('picking_ids')
    def _compute_picking_ids(self):
        for order in self:
            order.delivery_count = len(order.picking_ids)
    def action_view_delivery(self):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env.ref('stock.action_picking_tree_all').read()[0]

        pickings = self.mapped('picking_ids')
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = pickings.id
        return action
