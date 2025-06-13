from odoo import models, fields, api
import json

class InventoryScannerSession(models.Model):
    _name = 'inventory.scanner.session'
    _description = 'Inventory Scanner Session'
    _order = 'create_date desc'
    
    name = fields.Char(string='Session Name', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='State', default='draft')
    
    scanner_mode = fields.Selection([
        ('auto', 'Automatic (+1 per scan)'),
        ('manual', 'Manual (enter quantity)')
    ], string='Scanner Mode', default='auto', required=True)
    
    current_location_id = fields.Many2one(
        'stock.location', 
        string='Current Location',
        domain=[('usage', '=', 'internal')]
    )
    
    user_id = fields.Many2one(
        'res.users', 
        string='Responsible', 
        default=lambda self: self.env.user,
        required=True
    )
    
    company_id = fields.Many2one(
        'res.company', 
        string='Company', 
        default=lambda self: self.env.company
    )
    
    scan_count = fields.Integer(string='Total Scans', default=0)
    product_count = fields.Integer(string='Products Scanned', default=0)
    
    def action_start(self):
        self.state = 'in_progress'
        return True
    
    def action_finish(self):
        self.state = 'done'
        return True
    
    def action_cancel(self):
        self.state = 'cancelled'
        return True
    
    def get_scanner_data(self):
        return {
            'session_id': self.id,
            'name': self.name,
            'scanner_mode': self.scanner_mode,
            'current_location_id': self.current_location_id.id if self.current_location_id else False,
            'current_location_name': self.current_location_id.complete_name if self.current_location_id else '',
            'state': self.state
        }
    
    def open_scanner(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        scanner_url = f"{base_url}/inventory/scan/select/{self.id}"
        
        return {
            'type': 'ir.actions.act_url',
            'url': scanner_url,
            'target': 'new',
        }


class StockQuant(models.Model):
    _inherit = 'stock.quant'
    
    scanner_session_id = fields.Many2one('inventory.scanner.session', string='Scanner Session')
    scan_datetime = fields.Datetime(string='Scan Date/Time')
    scanned_by_user_id = fields.Many2one('res.users', string='Scanned By')
    scan_count = fields.Integer(string='Scan Count', default=0)
    
    @api.model
    def process_scanned_product(self, session_id, product_code, location_id, quantity=1, user_id=None):
        product = self.env['product.product'].search([
            '|',
            ('default_code', '=', product_code),
            ('barcode', '=', product_code)
        ], limit=1)
        
        if not product:
            return {
                'success': False,
                'message': f'Product not found: {product_code}'
            }
        
        session = self.env['inventory.scanner.session'].browse(session_id)
        if not session.exists():
            return {
                'success': False,
                'message': 'Session not found'
            }
        
        location = self.env['stock.location'].browse(location_id)
        if not location.exists():
            return {
                'success': False,
                'message': 'Location not found'
            }
        
        quant = self.search([
            ('product_id', '=', product.id),
            ('location_id', '=', location_id),
        ], limit=1)
        
        current_time = fields.Datetime.now()
        current_user = user_id or self.env.user.id
        
        if quant:
            if session.scanner_mode == 'auto':
                new_quantity = quant.quantity + quantity
            else:
                new_quantity = quantity
                
            quant.write({
                'quantity': new_quantity,
                'scanner_session_id': session_id,
                'scan_datetime': current_time,
                'scanned_by_user_id': current_user,
                'scan_count': quant.scan_count + 1
            })
        else:
            quant = self.create({
                'product_id': product.id,
                'location_id': location_id,
                'quantity': quantity,
                'scanner_session_id': session_id,
                'scan_datetime': current_time,
                'scanned_by_user_id': current_user,
                'scan_count': 1
            })
            new_quantity = quantity
        
        session.scan_count += 1
        
        return {
            'success': True,
            'message': f'Updated {product.name}: {new_quantity}',
            'product_name': product.name,
            'quantity': new_quantity,
            'location_name': location.complete_name
        }
