# -*- coding: utf-8 -*-
{
    'name': 'Meble - Produkty',
    'version': '1.0.0',
    'category': 'Manufacturing',
    'summary': 'Typy produktów meblarskich z dynamicznymi polami',
    'description': """
        Moduł definiujący typy produktów meblarskich i ich specyficzne pola:
        - Formatki (wymiary, obrzeża, płyty)
        - Płyty meblowe (wymiary, grubość, materiał)
        - Obrzeża (długość, grubość, kolor)
        - Okucia (typ, materiał, wykończenie)
        - Kartony (wymiary, nośność)
        - Tkaniny (skład, wzór, szerokość)
        
        Każdy typ produktu pokazuje tylko odpowiednie pola w widoku.
    """,
    'author': 'Furniture Solutions',
    'license': 'LGPL-3',
    'depends': ['product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}