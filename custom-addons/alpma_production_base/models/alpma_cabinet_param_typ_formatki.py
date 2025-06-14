from odoo import models, fields, api

class AlpmaCabinetParamTypFormatki(models.Model):
    _name = 'alpma.cabinet.param.typ_formatki'
    _description = 'Parametry typu formatki Alpma'
    _order = 'sequence, name'

    name = fields.Char('Nazwa typu formatki', required=True)
    code = fields.Char('Kod typu', required=True, help='Kod używany w nazwie formatki (np. BOK-L, WG, DRZWI)')
    description = fields.Text('Opis')
    sequence = fields.Integer('Kolejność', default=10)
    active = fields.Boolean('Aktywny', default=True)

    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for record in self:
            if record.code:
                name = f"{record.code} - {record.name}"
            else:
                name = record.name
            result.append((record.id, name))
        return result

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Kod typu formatki musi być unikalny!')
    ]
