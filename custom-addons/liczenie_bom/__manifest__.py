# -*- coding: utf-8 -*-
{
    'name': 'Liczenie BOM - Meble',
    'version': '1.0.0',
    'category': 'Manufacturing',
    'summary': 'Automatyczne obliczenia BOM dla produktów meblarskich',
    'description': """
        Moduł odpowiedzialny za automatyczne obliczenia zestawień materiałowych (BOM)
        dla produktów meblarskich. Obsługuje:
        - Obliczenia powierzchni płyt
        - Obliczenia długości obrzeży
        - Kalkulacje kosztów materiałów
        - Automatyczne generowanie BOM
    """,
    'author': 'Furniture Solutions',
    'license': 'LGPL-3',
    'depends': ['product', 'mrp', 'stock', 'meble_produkty'],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_bom_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}