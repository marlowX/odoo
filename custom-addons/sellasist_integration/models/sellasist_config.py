from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class SellasistConfig(models.Model):
    _name = 'sellasist.config'
    _description = 'Konfiguracja Sellasist'
    _rec_name = 'name'
    
    name = fields.Char('Nazwa', required=True, default='Konfiguracja Sellasist')
    api_key = fields.Char('Klucz API', required=True)
    active = fields.Boolean('Aktywne', default=True)
    
    # Konfiguracja automatycznej synchronizacji
    auto_sync_enabled = fields.Boolean('Automatyczna synchronizacja', default=True,
                                     help="Włącz automatyczną synchronizację przez cron")
    auto_sync_hours = fields.Integer('Zakres synchronizacji (godziny)', default=1,
                                   help="Ile godzin wstecz synchronizować orders_logs")
    cron_interval_minutes = fields.Integer('Interwał crona (minuty)', default=60,
                                         help="Co ile minut uruchamiać synchronizację")
    auto_create_orders = fields.Boolean('Automatycznie twórz zamówienia Odoo', default=False,
                                      help="Czy cron ma automatycznie tworzyć zamówienia sprzedaży w Odoo")
    
    def test_connection(self):
        """Test połączenia z API Sellasist"""
        try:
            import requests
            
            headers = {
                'accept': 'application/json',
                'apiKey': self.api_key
            }
            
            response = requests.get(
                'https://alpma.sellasist.pl/api/v1/orders_logs',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                message = f'✅ Połączenie OK! Znaleziono {len(data)} logów zamówień.'
                message_type = 'success'
            else:
                message = f'❌ Błąd połączenia: HTTP {response.status_code}'
                message_type = 'warning'
                
        except Exception as e:
            message = f'❌ Błąd: {str(e)}'
            message_type = 'danger'
            
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Test połączenia Sellasist',
                'message': message,
                'type': message_type,
                'sticky': False,
            }
        }
    
    def action_sync_orders(self):
        """Otwórz wizard synchronizacji zamówień"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Synchronizacja Sellasist',
            'res_model': 'sellasist.sync.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
    
    def write(self, vals):
        """Aktualizuj cron po zmianie konfiguracji"""
        result = super().write(vals)
        if any(field in vals for field in ['auto_sync_enabled', 'cron_interval_minutes']):
            self._update_cron_job()
        return result
    
    def _update_cron_job(self):
        """Zaktualizuj zadanie cron na podstawie konfiguracji"""
        cron = self.env.ref('sellasist_integration.ir_cron_sellasist_sync', raise_if_not_found=False)
        if cron:
            cron.write({
                'active': self.auto_sync_enabled,
                'interval_number': self.cron_interval_minutes,
                'interval_type': 'minutes'
            })
            
    def update_cron_from_config(self):
        """Ręczne odświeżenie crona"""
        self._update_cron_job()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Cron zaktualizowany',
                'message': f'Cron: {self.cron_interval_minutes} min, zakres: {self.auto_sync_hours}h',
                'type': 'success',
            }
        }
