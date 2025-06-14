{
    'name': 'Alpma Production Base',
    'version': '17.0.1.0.2',
    'category': 'Manufacturing',
    'summary': 'Bazowe rozszerzenia MRP dla produkcji mebli Alpma',
    'description': """
Alpma Production Base
====================

Moduł bazowy dla systemu produkcji mebli Alpma.

Funkcjonalności:
- Rozszerzenie product.template o pola meblowe
- Serie produktowe jako kategorie
- Podstawowe typy produktów (zestawy, produkty, formatki, okucia)
- Jednostki miary specyficzne dla mebli
- Integracja z Airtable (record ID)
- Konfigurowalne parametry szafek (nogi, uchwyty, drzwi)

Wymagania:
- Odoo 17.0 Community Edition
- Moduły: mrp, stock, product, sale
    """,
    'author': 'Alpma',
    'website': 'https://alpmeb.pl',
    'depends': [
        'base',
        'product', 
        'mrp',
        'stock',
        'sale'
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        
        # Data  
        'data/product_category_data.xml',
        'data/alpma_cabinet_params_data.xml',
        'data/alpma_cabinet_param_typ_formatki_data.xml',
        'data/alpma_cabinet_param_typ_szafki_data.xml',
        
        # Views
        'views/product_template_views.xml',
        'views/product_category_views.xml',
        'views/alpma_cabinet_params_views.xml',
        'views/alpma_cabinet_param_typ_formatki_views.xml',
        'views/alpma_cabinet_param_typ_szafki_views.xml',
        
        # Menu
        'views/alpma_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'alpma_production_base/static/src/css/alpma_styles.css',
        ],
    },
    'demo': [
        'demo/product_demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'sequence': 100,
}
