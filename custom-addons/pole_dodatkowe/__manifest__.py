# -*- coding: utf-8 -*-
{
    'name': 'Pole Dodatkowe',
    'version': '17.0.1.0.0',
    'category': 'Sales/Products',
    'summary': 'Dodaje pole checkbox Dodatek do produktów',
    'description': """
Moduł Pole Dodatkowe
===================

Ten moduł dodaje jedno pole checkbox o nazwie "Dodatek" do modelu produktu (product.template).

Funkcjonalności:
---------------
* Pole checkbox "Dodatek" na górze widoku produktu
* Proste i czyste rozszerzenie formularza produktu
* Integracja z istniejącymi widokami produktów
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