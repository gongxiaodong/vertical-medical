# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Dave Lasley <dave@laslabs.com>
#    Copyright: 2015 LasLabs, Inc.
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

from openerp import models, api, fields, _


class MedicalPrescriptionToSaleWizard(models.TransientModel):
    _name = 'medical.prescription.to.sale.wizard'
    _description = 'Convert Medical Prescription(s) to Sale Order(s)'

    def _compute_default_session(self, ):
        return self.env['medical.prescription.order'].browse(
            self._context.get('active_id')
        )
    
    prescription_id = fields.Many2one(
        comodel_name='medical.prescription.order',
        string='Prescription',
        required=True,
        default=_compute_default_session,
    )
    split_orders = fields.Selection([
        ('customer', 'By Customer'),
        ('patient', 'By Patient'),
        ('all', 'By Rx Line'),
    ],
        help='How to split the orders'
    )
    order_ids = fields.Many2many(
        comodel_name='sale.order',
        string='Orders',
        help='Created orders',
    )
    state = fields.Selection([
        ('start', 'Started'),
        ('partial', 'Partial'),
        ('done', 'Completed'),
        ('cancel', 'Cancelled'),
    ])


class MedicalPrescriptionToSaleWizardSale(models.TransientModel):
    _name = 'medical.prescription.to.sale.wizard.sale'
    _description = 'Temporary order info for Sale2Rx workflow'
    product_uom_qty = fields.Integer()
