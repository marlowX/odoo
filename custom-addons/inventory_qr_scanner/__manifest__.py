{
    'name': 'Inventory QR Scanner',
    'version': '17.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'QR Code Scanner for Inventory Management',
    'description': 'Simple QR scanner for inventory using mobile camera',
    'author': 'AlpSys',
    'website': 'https://erp.alpsys.pl',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/scanner_views.xml',
        'views/scanner_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'inventory_qr_scanner/static/src/css/scanner.css',
            'inventory_qr_scanner/static/src/js/scanner.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
