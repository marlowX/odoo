{
    'name': 'Produkt Formatka',
    'version': '2.1',
    'category': 'Manufacturing',
    'summary': 'System produktów meblarskich z BOM i zarządzaniem surowcami',
    'depends': ['product', 'stock', 'uom'],
    'data': [
        'security/ir.model.access.csv',
        'views/furniture_config_views.xml',
        'views/product_template_views.xml',
        'views/furniture_bom_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
