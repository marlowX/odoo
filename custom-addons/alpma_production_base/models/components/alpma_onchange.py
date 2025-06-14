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


@api.onchange('parametr_typ_formatki', 'parametr_typ_szafki', 'dlugosc_cm', 'szerokosc_cm', 'rozmiar_dlugosc', 'rozmiar_szerokosc', 'plyta_bazowa', 'kolor_manual')
def _onchange_parametr_formatki(self):
    """Aktualizuj nazwę przy zmianie parametrów formatki"""
    if self.typ_meblarski == 'formatka':
        nazwa_gen = self._generate_nazwa_formatki()
        if nazwa_gen:
            self.name = nazwa_gen
