# -*- coding: utf-8 -*-
# Part of Alpma. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class AlpmaCabinetParamNogi(models.Model):
    _name = 'alpma.cabinet.param.nogi'
    _description = 'Parametry nóg szafek'
    _order = 'sequence, name'

    name = fields.Char(
        string='Nazwa parametru',
        required=True,
        help="Nazwa parametru nóg (np. N1, N2, standardowe)"
    )
    
    code = fields.Char(
        string='Kod',
        help="Krótki kod parametru (np. N1, N2)"
    )
    
    description = fields.Text(
        string='Opis',
        help="Szczegółowy opis parametru nóg"
    )
    
    sequence = fields.Integer(
        string='Kolejność',
        default=10,
        help="Kolejność wyświetlania"
    )
    
    active = fields.Boolean(
        string='Aktywny',
        default=True,
        help="Czy parametr jest aktywny"
    )

    def name_get(self):
        """Wyświetl kod + nazwę"""
        result = []
        for record in self:
            if record.code:
                name = f"{record.code} - {record.name}"
            else:
                name = record.name
            result.append((record.id, name))
        return result


class AlpmaCabinetParamUchyt(models.Model):
    _name = 'alpma.cabinet.param.uchyt'
    _description = 'Parametry uchwytów szafek'
    _order = 'sequence, name'

    name = fields.Char(
        string='Nazwa parametru',
        required=True,
        help="Nazwa parametru uchwytu (np. U1, U2, klasyczny)"
    )
    
    code = fields.Char(
        string='Kod',
        help="Krótki kod parametru (np. U1, U2)"
    )
    
    description = fields.Text(
        string='Opis',
        help="Szczegółowy opis parametru uchwytu"
    )
    
    sequence = fields.Integer(
        string='Kolejność',
        default=10,
        help="Kolejność wyświetlania"
    )
    
    active = fields.Boolean(
        string='Aktywny',
        default=True,
        help="Czy parametr jest aktywny"
    )

    def name_get(self):
        """Wyświetl kod + nazwę"""
        result = []
        for record in self:
            if record.code:
                name = f"{record.code} - {record.name}"
            else:
                name = record.name
            result.append((record.id, name))
        return result


class AlpmaCabinetParamDrzwi(models.Model):
    _name = 'alpma.cabinet.param.drzwi'
    _description = 'Parametry drzwi szafek'
    _order = 'sequence, name'

    name = fields.Char(
        string='Nazwa parametru',
        required=True,
        help="Nazwa parametru drzwi (np. D1, D2, standardowe)"
    )
    
    code = fields.Char(
        string='Kod',
        help="Krótki kod parametru (np. D1, D2)"
    )
    
    description = fields.Text(
        string='Opis',
        help="Szczegółowy opis parametru drzwi"
    )
    
    sequence = fields.Integer(
        string='Kolejność',
        default=10,
        help="Kolejność wyświetlania"
    )
    
    active = fields.Boolean(
        string='Aktywny',
        default=True,
        help="Czy parametr jest aktywny"
    )

    def name_get(self):
        """Wyświetl kod + nazwę"""
        result = []
        for record in self:
            if record.code:
                name = f"{record.code} - {record.name}"
            else:
                name = record.name
            result.append((record.id, name))
        return result
