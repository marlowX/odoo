from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class SellasistSyncWizard(models.TransientModel):
    _name = 'sellasist.sync.wizard'
    _description = 'Wizard synchronizacji Sellasist'
    
    sync_type = fields.Selection([
        ('hours', 'Ostatnie godziny'),
        ('days', 'Ostatnie dni'),
        ('custom', 'Niestandardowy zakres'),
    ], string='Typ synchronizacji', default='hours', required=True)
    
    hours_back = fields.Integer('Godziny wstecz', default=24)
    days_back = fields.Integer('Dni wstecz', default=7)
    
    date_from = fields.Datetime('Data od')
    date_to = fields.Datetime('Data do')
    
    auto_create_orders = fields.Boolean('Automatycznie twórz zamówienia Odoo', default=False)
    
    def action_sync(self):
        """Wykonaj synchronizację z poprawnym przekazywaniem dat"""
        sellasist_order = self.env['sellasist.order']
        
        if self.sync_type == 'custom' and self.date_from and self.date_to:
            # NIESTANDARDOWY ZAKRES - przekaż konkretne daty
            success = sellasist_order.sync_orders_by_date_range(self.date_from, self.date_to)
        else:
            # STANDARDOWE - oblicz godziny wstecz
            if self.sync_type == 'hours':
                hours = self.hours_back
            elif self.sync_type == 'days':
                hours = self.days_back * 24
            else:
                hours = 24
            success = sellasist_order.sync_orders_from_sellasist(hours)
            
        if success:
            if self.auto_create_orders:
                unsynced_orders = sellasist_order.search([('synced', '=', False)])
                for order in unsynced_orders:
                    try:
                        order.action_sync_to_sale_order()
                    except Exception as e:
                        _logger.error(f"Błąd tworzenia zamówienia {order.sellasist_id}: {str(e)}")
                        
            message = f'✅ Synchronizacja zakończona pomyślnie!'
            message_type = 'success'
        else:
            message = f'❌ Błąd synchronizacji'
            message_type = 'danger'
            
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Synchronizacja Sellasist',
                'message': message,
                'type': message_type,
                'sticky': False,
            }
        }
