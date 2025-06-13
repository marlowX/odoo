# -*- coding: utf-8 -*-
# Part of Alpma. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    # === ALPMA SERIES ===
    is_alpma_series = fields.Boolean(
        string='Seria Alpma',
        default=False,
        help="Czy ta kategoria reprezentuje serię produktową Alpma"
    )

    # === KONFIGURACJA SERII ===
    seria_kod = fields.Char(
        string='Kod serii',
        help="Krótki kod serii używany w SKU (np. VB, SUPRA, TRES)"
    )

    seria_opis = fields.Text(
        string='Opis serii',
        help="Szczegółowy opis serii produktowej"
    )

    # === KOLORY DOSTĘPNE W SERII ===
    dostepne_kolory = fields.Char(
        string='Dostępne kolory',
        help="Lista dostępnych kolorów oddzielona przecinkami (np. BIAŁY,CZARNY,WOTAN)"
    )

    # === WYMIARY STANDARDOWE ===
    standardowe_szerokosci = fields.Char(
        string='Standardowe szerokości',
        help="Dostępne szerokości w cm oddzielone przecinkami (np. 30,60,80,100)"
    )

    standardowe_wysokosci = fields.Char(
        string='Standardowe wysokości', 
        help="Dostępne wysokości w cm oddzielone przecinkami (np. 30,60,90,120)"
    )

    # === ROUTING I SZABLONY ===
    domyslny_routing = fields.Many2one(
        'mrp.routing',
        string='Domyślny routing',
        help="Standardowy routing produkcji dla tej serii"
    )

    szablon_bom = fields.Many2one(
        'mrp.bom',
        string='Szablon BOM',
        help="Szablon BOM dla automatycznego generowania"
    )

    # === STATYSTYKI ===
    liczba_produktow = fields.Integer(
        string='Liczba produktów',
        compute='_compute_liczba_produktow',
        help="Ilość produktów w tej serii"
    )

    # === COMPUTE METHODS ===
    def _compute_liczba_produktow(self):
        """Oblicza liczbę produktów w serii"""
        for category in self:
            # Poprawne pole to product_count lub liczymy ręcznie
            products = self.env['product.template'].search([('categ_id', '=', category.id)])
            category.liczba_produktow = len(products)

    # === HELPER METHODS ===
    def get_dostepne_kolory_list(self):
        """Zwraca listę dostępnych kolorów"""
        self.ensure_one()
        if self.dostepne_kolory:
            return [kolor.strip() for kolor in self.dostepne_kolory.split(',')]
        return []

    def get_standardowe_szerokosci_list(self):
        """Zwraca listę standardowych szerokości jako float"""
        self.ensure_one()
        if self.standardowe_szerokosci:
            try:
                return [float(szer.strip()) for szer in self.standardowe_szerokosci.split(',')]
            except ValueError:
                return []
        return []

    def get_standardowe_wysokosci_list(self):
        """Zwraca listę standardowych wysokości jako float"""
        self.ensure_one()
        if self.standardowe_wysokosci:
            try:
                return [float(wys.strip()) for wys in self.standardowe_wysokosci.split(',')]
            except ValueError:
                return []
        return []

    # === ACTIONS ===
    def action_view_products(self):
        """Akcja do wyświetlenia produktów w serii"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Produkty serii {self.name}',
            'res_model': 'product.template',
            'view_mode': 'tree,form',
            'domain': [('categ_id', '=', self.id)],
            'context': {
                'default_categ_id': self.id,
                'default_is_alpma_product': True,
                'default_seria_produktowa': self.id,
            }
        }

    @api.model
    def create_alpma_series(self, nazwa, kod, parent_id=False):
        """Helper do tworzenia nowych serii Alpma"""
        vals = {
            'name': nazwa,
            'seria_kod': kod,
            'is_alpma_series': True,
            'parent_id': parent_id,
        }
        return self.create(vals)
