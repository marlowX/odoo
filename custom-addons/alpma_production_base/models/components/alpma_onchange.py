# -*- coding: utf-8 -*-
# Part of Alpma. See LICENSE file for full copyright and licensing details.

from odoo import api


@api.onchange('typ_meblarski')
def _onchange_typ_meblarski(self):
    """Ustawia domyślne wartości na podstawie typu"""
    if self.typ_meblarski == 'formatka':
        self.type = 'product'
        self.tracking = 'lot'
    elif self.typ_meblarski == 'zestaw':
        self.type = 'product'
    elif self.typ_meblarski in ['okucia', 'akcesoria']:
        self.type = 'product'
        self.tracking = 'none'
    elif self.typ_meblarski == 'plyta':
        self.type = 'product'
        self.tracking = 'lot'
