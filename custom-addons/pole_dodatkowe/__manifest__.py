# -*- coding: utf-8 -*-
{
    'name': 'Pole Dodatkowe',
    'version': '17.0.1.0.0',
    'category': 'Sales/Products',
    'summary': 'Dodaje pole checkbox Dodatek do produktów - wersja minimalna',
    'description': """
Moduł Pole Dodatkowe - Wersja Minimalna
======================================

Ten moduł dodaje jedno pole checkbox o nazwie "Dodatek" do modelu produktu (product.template).

Funkcjonalności:
---------------
* Pole checkbox "Dodatek" na górze widoku produktu
* Kompatybilne z Odoo 17.0
* Minimalne rozszerzenie bez konfliktów XPath
    """,
    'author': 'Twoja Firma',
    'website': 'https://www.twojastrona.pl',
    'license': 'LGPL-3',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}