# -*- coding: utf-8 -*-
# Part of Alpma. See LICENSE file for full copyright and licensing details.

from odoo import api, _
from odoo.exceptions import ValidationError


@api.constrains('dlugosc_cm', 'szerokosc_cm', 'wysokosc_cm', 'grubosc_plyty_mm', 'grubosc_obrzeza_mm')
def _check_dimensions(self):
    """Sprawdza poprawność wymiarów"""
    for record in self:
        if record.dlugosc_cm and record.dlugosc_cm <= 0:
            raise ValidationError(_("Długość musi być większa od 0"))
        if record.szerokosc_cm and record.szerokosc_cm <= 0:
            raise ValidationError(_("Szerokość musi być większa od 0"))
        if record.wysokosc_cm and record.wysokosc_cm <= 0:
            raise ValidationError(_("Wysokość musi być większa od 0"))
        if record.grubosc_plyty_mm and record.grubosc_plyty_mm <= 0:
            raise ValidationError(_("Grubość płyty musi być większa od 0"))
        if record.grubosc_obrzeza_mm and record.grubosc_obrzeza_mm <= 0:
            raise ValidationError(_("Grubość obrzeża musi być większa od 0"))
