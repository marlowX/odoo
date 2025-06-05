# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Pole checkbox Dodatek
    dodatek = fields.Boolean(
        string='Dodatek',
        default=False,
        help='Zaznacz jeśli produkt jest dodatkiem'
    )