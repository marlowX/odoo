# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    # Pola obliczeniowe BOM
    total_plate_area = fields.Float(
        string='Powierzchnia płyt (m²)',
        compute='_compute_furniture_totals',
        store=True,
        digits=(10, 4),
        help='Łączna powierzchnia płyt w m²'
    )
    
    total_edge_length = fields.Float(
        string='Długość obrzeży (m)',
        compute='_compute_furniture_totals',
        store=True,
        digits=(10, 3),
        help='Łączna długość obrzeży w metrach bieżących'
    )
    
    estimated_cost = fields.Monetary(
        string='Szacowany koszt',
        compute='_compute_furniture_totals',
        store=True,
        currency_field='currency_id',
        help='Szacowany koszt wszystkich materiałów'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Waluta',
        default=lambda self: self.env.company.currency_id
    )
    
    is_furniture_bom = fields.Boolean(
        string='BOM meblarski',
        default=False,
        help='Czy to jest BOM wygenerowany automatycznie dla mebli'
    )

    @api.depends('bom_line_ids.product_qty', 'bom_line_ids.product_id', 'bom_line_ids.product_id.standard_price')
    def _compute_furniture_totals(self):
        """Oblicza łączne wartości dla BOM meblarskiego"""
        for bom in self:
            total_area = 0.0
            total_edge = 0.0
            total_cost = 0.0
            
            for line in bom.bom_line_ids:
                product = line.product_id
                qty = line.product_qty or 0.0
                
                # Sprawdź typ meblarski produktu (z modułu meble_produkty)
                if hasattr(product, 'furniture_type') and product.furniture_type:
                    
                    # Powierzchnia płyt - bezpośrednio z qty (już w m²)
                    if product.furniture_type == 'plyta_meblowa':
                        total_area += qty  # qty już w m²
                    
                    # Długość obrzeży - bezpośrednio z qty (już w m)
                    elif product.furniture_type == 'obrzeze':
                        total_edge += qty  # qty już w metrach
                
                # Koszt składnika
                if hasattr(product, 'standard_price') and product.standard_price:
                    total_cost += product.standard_price * qty
            
            bom.total_plate_area = total_area
            bom.total_edge_length = total_edge
            bom.estimated_cost = total_cost

    def action_auto_generate_furniture_bom(self):
        """Automatyczne generowanie BOM na podstawie parametrów formatki"""
        self.ensure_one()
        
        # Sprawdź czy produkt ma typ meblarski
        if not hasattr(self.product_tmpl_id, 'furniture_type'):
            raise UserError(_('Ten produkt nie ma zdefiniowanego typu meblarskiego!\nUpewnij się, że moduł meble_produkty jest zainstalowany.'))
            
        if self.product_tmpl_id.furniture_type != 'formatka':
            raise UserError(_('Automatyczne generowanie BOM jest dostępne tylko dla formatek!'))
        
        product = self.product_tmpl_id
        
        # Sprawdź podstawowe wymiary z debugowaniem
        if not (hasattr(product, 'dlugosc') and hasattr(product, 'szerokosc') and hasattr(product, 'grubosc')):
            raise UserError(_('Formatka nie ma zdefiniowanych wymiarów!\nSprawdź czy moduł meble_produkty jest zainstalowany.'))
            
        # Pobierz wymiary i sprawdź ich wartości
        dlugosc = getattr(product, 'dlugosc', 0) or 0
        szerokosc = getattr(product, 'szerokosc', 0) or 0  
        grubosc = getattr(product, 'grubosc', 0) or 0
        
        if not (dlugosc > 0 and szerokosc > 0 and grubosc > 0):
            raise UserError(_('Wszystkie wymiary formatki muszą być większe od zera!\nAktualne wymiary:\n• Długość: %.1f mm\n• Szerokość: %.1f mm\n• Grubość: %.1f mm') % (dlugosc, szerokosc, grubosc))
        
        # Usuwanie istniejących linii
        if self.bom_line_ids:
            self.bom_line_ids.unlink()
        
        lines_vals = []
        generated_count = 0
        
        # Generowanie linii dla płyty
        if hasattr(product, 'plyta_id') and product.plyta_id:
            # Oblicz powierzchnię w m² używając lokalnych zmiennych
            area_mm2 = dlugosc * szerokosc
            area_m2 = area_mm2 / 1000000
            
            # Znajdź jednostkę miary dla m²
            try:
                uom_m2 = self.env.ref('uom.product_uom_square_meter')
            except:
                uom_m2 = product.plyta_id.uom_id
            
            lines_vals.append({
                'product_id': product.plyta_id.id,
                'product_qty': area_m2,
                'product_uom_id': uom_m2.id,
            })
            generated_count += 1
        
        # Generowanie linii dla obrzeży używając lokalnych zmiennych
        edge_configs = [
            ('obrzeze_gora_id', dlugosc, 'góra'),
            ('obrzeze_dol_id', dlugosc, 'dół'),
            ('obrzeze_lewo_id', szerokosc, 'lewo'),
            ('obrzeze_prawo_id', szerokosc, 'prawo')
        ]
        
        for edge_field, dimension, edge_name in edge_configs:
            if hasattr(product, edge_field):
                edge_product = getattr(product, edge_field, None)
                if edge_product and dimension:
                    # Oblicz długość obrzeża w metrach
                    length_m = dimension / 1000
                    
                    # Znajdź jednostkę miary dla metrów
                    try:
                        uom_m = self.env.ref('uom.product_uom_meter')
                    except:
                        uom_m = edge_product.uom_id
                    
                    lines_vals.append({
                        'product_id': edge_product.id,
                        'product_qty': length_m,
                        'product_uom_id': uom_m.id,
                    })
                    generated_count += 1
        
        # Utwórz linie BOM
        if lines_vals:
            self.write({'bom_line_ids': [(0, 0, vals) for vals in lines_vals]})
            self.write({'is_furniture_bom': True})
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Sukces'),
                    'message': _('BOM został wygenerowany automatycznie!\nDodano %d składników.') % generated_count,
                    'type': 'success',
                }
            }
        else:
            raise UserError(_('Nie można wygenerować BOM!\n\nSprawdź czy formatka ma:\n• Przypisaną płytę\n• Przynajmniej jedno obrzeże\n• Poprawne wymiary'))

    def action_calculate_material_requirements(self):
        """Oblicza zapotrzebowanie materiałowe na podstawie ilości produkcji"""
        self.ensure_one()
        
        # Możliwość rozszerzenia o bardziej zaawansowane obliczenia
        # np. uwzględnienie strat materiału, optymalizacji cięcia itp.
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Zapotrzebowanie materiałowe'),
            'res_model': 'mrp.bom',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def get_furniture_statistics(self):
        """Zwraca statystyki BOM meblarskiego"""
        self.ensure_one()
        
        stats = {
            'total_components': len(self.bom_line_ids),
            'plate_area': self.total_plate_area,
            'edge_length': self.total_edge_length,
            'estimated_cost': self.estimated_cost,
            'cost_breakdown': []
        }
        
        # Breakdown kosztów po typach materiałów
        cost_by_type = {}
        for line in self.bom_line_ids:
            if hasattr(line.product_id, 'furniture_type'):
                ftype = line.product_id.furniture_type
                cost = line.product_id.standard_price * line.product_qty
                
                if ftype not in cost_by_type:
                    cost_by_type[ftype] = 0
                cost_by_type[ftype] += cost
        
        stats['cost_breakdown'] = cost_by_type
        return stats