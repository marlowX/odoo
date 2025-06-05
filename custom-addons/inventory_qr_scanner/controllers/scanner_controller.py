import json
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class ScannerController(http.Controller):
    
    @http.route('/inventory/scan', type='http', auth='user', website=True)
    def scanner_main_page(self, **kwargs):
        sessions = request.env['inventory.scanner.session'].search([
            ('state', 'in', ['draft', 'in_progress'])
        ])
        
        locations = request.env['stock.location'].search([
            ('usage', '=', 'internal')
        ])
        
        values = {
            'sessions': sessions,
            'locations': locations,
        }
        
        return request.render('inventory_qr_scanner.scanner_main_page', values)
    
    @http.route('/inventory/scan/select/<int:session_id>', type='http', auth='user', website=True)
    def scanner_interface(self, session_id, **kwargs):
        session = request.env['inventory.scanner.session'].browse(session_id)
        if not session.exists():
            return request.redirect('/inventory/scan')
        
        if session.state == 'draft':
            session.action_start()
        
        locations = request.env['stock.location'].search([
            ('usage', '=', 'internal')
        ])
        
        values = {
            'session': session,
            'locations': locations,
            'session_data': json.dumps(session.get_scanner_data())
        }
        
        return request.render('inventory_qr_scanner.scanner_interface', values)
    
    @http.route('/inventory/scan/process', type='json', auth='user', methods=['POST'])
    def process_scan(self, **kwargs):
        try:
            data = kwargs
            scan_code = data.get('code', '').strip()
            session_id = data.get('session_id')
            current_location_id = data.get('location_id')
            quantity = data.get('quantity', 1)
            
            if not scan_code:
                return {'success': False, 'message': 'Empty scan code'}
            
            if scan_code.startswith('LOC:'):
                location_name = scan_code[4:]
                location = request.env['stock.location'].search([
                    '|',
                    ('name', '=', location_name),
                    ('complete_name', 'ilike', location_name)
                ], limit=1)
                
                if location:
                    session = request.env['inventory.scanner.session'].browse(session_id)
                    session.current_location_id = location.id
                    
                    return {
                        'success': True,
                        'message': f'Location set: {location.complete_name}',
                        'type': 'location',
                        'location_id': location.id,
                        'location_name': location.complete_name
                    }
                else:
                    return {
                        'success': False,
                        'message': f'Location not found: {location_name}'
                    }
            
            else:
                if not current_location_id:
                    return {
                        'success': False, 
                        'message': 'Please scan location first'
                    }
                
                result = request.env['stock.quant'].process_scanned_product(
                    session_id=session_id,
                    product_code=scan_code,
                    location_id=current_location_id,
                    quantity=quantity,
                    user_id=request.env.user.id
                )
                
                if result['success']:
                    result['type'] = 'product'
                
                return result
                
        except Exception as e:
            _logger.error(f"Error processing scan: {str(e)}")
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    @http.route('/inventory/scan/location/<int:location_id>', type='json', auth='user')
    def set_location(self, location_id, session_id, **kwargs):
        try:
            session = request.env['inventory.scanner.session'].browse(session_id)
            location = request.env['stock.location'].browse(location_id)
            
            if session.exists() and location.exists():
                session.current_location_id = location.id
                return {
                    'success': True,
                    'message': f'Location set: {location.complete_name}',
                    'location_name': location.complete_name
                }
            else:
                return {'success': False, 'message': 'Invalid session or location'}
                
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    @http.route('/inventory/scan/finish/<int:session_id>', type='json', auth='user')
    def finish_session(self, session_id, **kwargs):
        try:
            session = request.env['inventory.scanner.session'].browse(session_id)
            
            if session.exists() and session.state == 'in_progress':
                session.action_finish()
                return {
                    'success': True,
                    'message': 'Session finished successfully'
                }
            else:
                return {
                    'success': False, 
                    'message': 'Invalid session or session not in progress'
                }
                
        except Exception as e:
            return {'success': False, 'message': str(e)}
