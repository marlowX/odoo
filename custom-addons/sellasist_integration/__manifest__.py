{
    'name': 'Sellasist Integration',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'Integracja z systemem Sellasist',
    'description': """
        Moduł integracji z systemem Sellasist
        =====================================
        
        * Pobieranie zamówień z API Sellasist
        * Synchronizacja produktów
        * Zarządzanie konfiguracją API
        * Automatyczne fakturowanie
    """,
    'author': 'Alpma',
    'website': '',
    'depends': ['base', 'sale', 'stock', 'account'],
    'data': [
        'data/ir_actions_server.xml',
        'views/sellasist_config_views.xml',
        'views/sellasist_order_views.xml',
        'wizard/sellasist_sync_wizard_views.xml',
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
