# -*- coding: utf-8 -*-
# Part of Alpma. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # === IMPORT KOMPONENTÓW ===
    from .components.alpma_fields import (
        # Podstawowe pola
        typ_meblarski, seria_produktowa, grupa_produkcyjna, is_alpma_product, airtable_record_id,
        # Pola formatek
        cz1, cz2, produkt_powiazany, rozmiar_dlugosc, rozmiar_szerokosc,
        # Wymiary podstawowe
        dlugosc_cm, szerokosc_cm, wysokosc_cm,
        # Płyty i kolory
        plyta_bazowa, grubosc_mm, kolor_material, kolor_manual,
        # Obrzeża
        ok1_obrzeze, ok2_obrzeze, ok3_obrzeze, ok4_obrzeze, wszystkie_obrzeza,
        # Parametry szafek
        parametr_nogi, parametr_uchyt, parametr_drzwi,
        # Parametry okuć
        dlugosc_okucia_mm, nosnosc_kg,
        # Parametry obrzeży
        szerokosc_obrzeza_mm, grubosc_obrzeza_mm, dlugosc_rolki_m,
        # Parametry płyt
        grubosc_plyty_mm,
        # Pola obliczane
        wymiary_display, objetosc_m3, powierzchnia_m2, show_sku_field
    )

    # === IMPORT METOD OBLICZAJĄCYCH ===
    from .components.alpma_compute_methods import (
        _compute_grubosc,
        _compute_kolor_material,
        _compute_wymiary_display,
        _generate_nazwa_formatki,
        _compute_objetosc,
        _compute_powierzchnia,
        _compute_show_sku
    )

    # === IMPORT WALIDACJI ===
    from .components.alpma_constraints import _check_dimensions

    # === IMPORT ONCHANGE ===
    from .components.alpma_onchange import _onchange_typ_meblarski

    # === IMPORT AKCJI ===
    from .components.alpma_actions import action_assign_all_edges
