# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Główne pole typu meblarskiego
    furniture_type = fields.Selection([
        ('formatka', 'Formatka'),
        ('plyta_meblowa', 'Płyta meblowa'),
        ('obrzeze', 'Obrzeże'),
        ('okucia', 'Okucia'),
        ('kartony', 'Kartony'),
        ('tkaniny', 'Tkaniny'),
    ], string='Typ meblarski', help='Typ produktu w kategorii meblarskiej')

    # === POLA DLA FORMATEK ===
    czy_formatka = fields.Boolean(
        string='Czy formatka',
        compute='_compute_czy_formatka',
        store=True,
        help='Automatycznie ustawiane gdy typ = formatka'
    )
    
    # Wymiary formatki
    dlugosc = fields.Float(
        string='Długość (mm)',
        digits=(10, 1),
        help='Długość formatki w milimetrach'
    )
    
    szerokosc = fields.Float(
        string='Szerokość (mm)',
        digits=(10, 1),
        help='Szerokość formatki w milimetrach'
    )
    
    grubosc = fields.Float(
        string='Grubość (mm)',
        digits=(10, 1),
        help='Grubość formatki w milimetrach'
    )
    
    # Wybór płyty dla formatki
    plyta_id = fields.Many2one(
        'product.template',
        string='Płyta',
        domain="[('furniture_type', '=', 'plyta_meblowa')]",
        help='Płyta używana do wykonania formatki'
    )
    
    # Wybór obrzeży dla formatki
    obrzeze_gora_id = fields.Many2one(
        'product.template',
        string='Obrzeże góra',
        domain="[('furniture_type', '=', 'obrzeze')]",
        help='Obrzeże na górnej krawędzi'
    )
    
    obrzeze_dol_id = fields.Many2one(
        'product.template',
        string='Obrzeże dół',
        domain="[('furniture_type', '=', 'obrzeze')]",
        help='Obrzeże na dolnej krawędzi'
    )
    
    obrzeze_lewo_id = fields.Many2one(
        'product.template',
        string='Obrzeże lewo',
        domain="[('furniture_type', '=', 'obrzeze')]",
        help='Obrzeże na lewej krawędzi'
    )
    
    obrzeze_prawo_id = fields.Many2one(
        'product.template',
        string='Obrzeże prawo',
        domain="[('furniture_type', '=', 'obrzeze')]",
        help='Obrzeże na prawej krawędzi'
    )

    # === POLA DLA PŁYT MEBLOWYCH ===
    plate_length = fields.Float(
        string='Długość płyty (mm)',
        digits=(10, 1),
        help='Długość standardowej płyty w milimetrach'
    )
    
    plate_width = fields.Float(
        string='Szerokość płyty (mm)',
        digits=(10, 1),
        help='Szerokość standardowej płyty w milimetrach'
    )
    
    plate_thickness = fields.Float(
        string='Grubość płyty (mm)',
        digits=(10, 1),
        help='Grubość płyty w milimetrach'
    )
    
    plate_material = fields.Selection([
        ('wiórowa', 'Płyta wiórowa'),
        ('mdf', 'Płyta MDF'),
        ('hdf', 'Płyta HDF'),
        ('laminowana', 'Płyta laminowana'),
        ('melaminowana', 'Płyta melaminowana'),
        ('fornirowana', 'Płyta fornirowana'),
    ], string='Rodzaj płyty')
    
    plate_color = fields.Char(
        string='Kolor płyty',
        help='Kolor lub dekór płyty'
    )
    
    plate_surface = fields.Selection([
        ('gładka', 'Gładka'),
        ('strukturalna', 'Strukturalna'),
        ('matowa', 'Matowa'),
        ('połyskowa', 'Połyskowa'),
    ], string='Powierzchnia')

    # === POLA DLA OBRZEŻY ===
    edge_length = fields.Float(
        string='Długość obrzeża (mm)',
        digits=(10, 1),
        help='Długość rolki obrzeża w milimetrach'
    )
    
    edge_width = fields.Float(
        string='Szerokość obrzeża (mm)',
        digits=(10, 1),
        help='Szerokość obrzeża w milimetrach'
    )
    
    edge_thickness = fields.Float(
        string='Grubość obrzeża (mm)',
        digits=(10, 2),
        help='Grubość obrzeża w milimetrach'
    )
    
    edge_material = fields.Selection([
        ('abs', 'ABS'),
        ('pvc', 'PVC'),
        ('pp', 'PP (Polipropylen)'),
        ('drewno', 'Drewno naturalne'),
        ('fornir', 'Fornir'),
        ('aluminium', 'Aluminium'),
    ], string='Materiał obrzeża')
    
    edge_color = fields.Char(
        string='Kolor obrzeża',
        help='Kolor obrzeża'
    )

    # === POLA DLA OKUĆ ===
    hardware_type = fields.Selection([
        ('zawiasy', 'Zawiasy'),
        ('prowadnice', 'Prowadnice'),
        ('uchwyty', 'Uchwyty'),
        ('knopy', 'Knopy'),
        ('zamki', 'Zamki'),
        ('wsporniki', 'Wsporniki'),
        ('nogi', 'Nogi'),
        ('kółka', 'Kółka'),
    ], string='Typ okucia')
    
    hardware_material = fields.Selection([
        ('stal', 'Stal'),
        ('stal_nierdzewna', 'Stal nierdzewna'),
        ('mosiądz', 'Mosiądz'),
        ('aluminium', 'Aluminium'),
        ('plastik', 'Plastik'),
        ('drewno', 'Drewno'),
    ], string='Materiał okucia')
    
    hardware_finish = fields.Selection([
        ('naturalne', 'Naturalne'),
        ('chromowane', 'Chromowane'),
        ('niklowane', 'Niklowane'),
        ('lakierowane', 'Lakierowane'),
        ('anodowane', 'Anodowane'),
        ('malowane', 'Malowane'),
    ], string='Wykończenie')
    
    hardware_load_capacity = fields.Float(
        string='Nośność (kg)',
        digits=(10, 1),
        help='Maksymalna nośność okucia w kilogramach'
    )

    # === POLA DLA KARTONÓW ===
    carton_length = fields.Float(
        string='Długość kartonu (mm)',
        digits=(10, 1),
        help='Długość kartonu w milimetrach'
    )
    
    carton_width = fields.Float(
        string='Szerokość kartonu (mm)',
        digits=(10, 1),
        help='Szerokość kartonu w milimetrach'
    )
    
    carton_height = fields.Float(
        string='Wysokość kartonu (mm)',
        digits=(10, 1),
        help='Wysokość kartonu w milimetrach'
    )
    
    carton_type = fields.Selection([
        ('jednorodny', 'Karton jednorodny'),
        ('falisty', 'Karton falisty'),
        ('warstwowy', 'Karton warstwowy'),
    ], string='Typ kartonu')
    
    carton_strength = fields.Float(
        string='Wytrzymałość (kg)',
        digits=(10, 1),
        help='Wytrzymałość kartonu na naciski'
    )

    # === POLA DLA TKANIN ===
    fabric_width = fields.Float(
        string='Szerokość tkaniny (cm)',
        digits=(10, 1),
        help='Szerokość rolki tkaniny w centymetrach'
    )
    
    fabric_composition = fields.Char(
        string='Skład tkaniny',
        help='Skład materiałowy tkaniny (np. 100% bawełna)'
    )
    
    fabric_pattern = fields.Selection([
        ('gładka', 'Gładka'),
        ('w_paski', 'W paski'),
        ('w_kratkę', 'W kratkę'),
        ('kwiatowa', 'Kwiatowa'),
        ('geometryczna', 'Geometryczna'),
        ('abstrakcyjna', 'Abstrakcyjna'),
    ], string='Wzór tkaniny')
    
    fabric_weight = fields.Float(
        string='Gramatura (g/m²)',
        digits=(10, 1),
        help='Gramatura tkaniny w gramach na metr kwadratowy'
    )
    
    fabric_care = fields.Text(
        string='Sposób pielęgnacji',
        help='Instrukcje dotyczące pielęgnacji tkaniny'
    )

    @api.depends('furniture_type')
    def _compute_czy_formatka(self):
        """Automatycznie ustawia pole czy_formatka na podstawie typu"""
        for record in self:
            record.czy_formatka = (record.furniture_type == 'formatka')

    # Walidacje usunięte - pozwalamy na elastyczne tworzenie produktów

    def get_formatted_dimensions(self):
        """Zwraca sformatowane wymiary w zależności od typu produktu"""
        self.ensure_one()
        
        if self.furniture_type == 'formatka':
            if self.dlugosc and self.szerokosc and self.grubosc:
                return f"{self.dlugosc:.0f} × {self.szerokosc:.0f} × {self.grubosc:.0f} mm"
        
        elif self.furniture_type == 'plyta_meblowa':
            if self.plate_length and self.plate_width and self.plate_thickness:
                return f"{self.plate_length:.0f} × {self.plate_width:.0f} × {self.plate_thickness:.0f} mm"
        
        elif self.furniture_type == 'obrzeze':
            if self.edge_length and self.edge_width and self.edge_thickness:
                return f"L: {self.edge_length:.0f} mm, W: {self.edge_width:.1f} mm, T: {self.edge_thickness:.1f} mm"
        
        return _('Brak wymiarów')

    def action_configure_furniture_product(self):
        """Otwiera konfigurację produktu meblarskiego"""
        self.ensure_one()
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Konfiguracja produktu meblarskiego'),
            'res_model': 'product.template',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_create_bom(self):
        """Tworzy BOM dla formatki - wymaga zainstalowanego modułu MRP"""
        if self.furniture_type != 'formatka':
            return {'type': 'ir.actions.act_window_close'}
            
        # Sprawdź czy moduł MRP jest zainstalowany
        try:
            self.env['mrp.bom']
        except KeyError:
            # Moduł MRP nie jest zainstalowany
            raise UserError(_('Moduł Manufacturing (MRP) musi być zainstalowany aby tworzyć receptury BOM.'))
        
        # Podstawowe wartości BOM
        bom_vals = {
            'product_tmpl_id': self.id,
            'product_id': False,
            'product_qty': 1.0,
            'type': 'normal',
        }
        
        # Dodaj pole is_furniture_bom tylko jeśli istnieje (moduł liczenie_bom zainstalowany)
        if 'is_furniture_bom' in self.env['mrp.bom']._fields:
            bom_vals['is_furniture_bom'] = True
        
        bom = self.env['mrp.bom'].create(bom_vals)
        
        # Automatycznie generuj BOM jeśli mamy wszystkie dane
        if hasattr(bom, 'action_auto_generate_furniture_bom'):
            try:
                bom.action_auto_generate_furniture_bom()
            except Exception:
                pass  # Kontynuuj mimo błędu auto-generacji
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Receptura (BOM)'),
            'res_model': 'mrp.bom',
            'res_id': bom.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_auto_generate_bom(self):
        """Tworzy BOM i automatycznie generuje składniki dla formatki"""
        if self.furniture_type != 'formatka':
            return {'type': 'ir.actions.act_window_close'}
            
        # Sprawdź czy moduł MRP jest zainstalowany
        try:
            self.env['mrp.bom']
        except KeyError:
            raise UserError(_('Moduł Manufacturing (MRP) musi być zainstalowany aby tworzyć receptury BOM.'))
        
        # Znajdź istniejący BOM lub utwórz nowy
        existing_bom = self.env['mrp.bom'].search([('product_tmpl_id', '=', self.id)], limit=1)
        
        if existing_bom:
            bom = existing_bom
        else:
            # Podstawowe wartości BOM
            bom_vals = {
                'product_tmpl_id': self.id,
                'product_id': False,
                'product_qty': 1.0,
                'type': 'normal',
            }
            
            # Dodaj pole is_furniture_bom tylko jeśli istnieje
            if 'is_furniture_bom' in self.env['mrp.bom']._fields:
                bom_vals['is_furniture_bom'] = True
            
            bom = self.env['mrp.bom'].create(bom_vals)
        
        # Automatycznie generuj składniki BOM jeśli funkcja jest dostępna
        if hasattr(bom, 'action_auto_generate_furniture_bom'):
            try:
                return bom.action_auto_generate_furniture_bom()
            except Exception as e:
                raise UserError(_('Błąd podczas automatycznego generowania BOM: %s') % str(e))
        else:
            # Jeśli moduł liczenie_bom nie jest zainstalowany, otwórz BOM do ręcznej edycji
            return {
                'type': 'ir.actions.act_window',
                'name': _('Receptura (BOM) - dodaj składniki ręcznie'),
                'res_model': 'mrp.bom',
                'res_id': bom.id,
                'view_mode': 'form',
                'target': 'current',
            }

    def action_view_boms(self):
        """Otwiera wszystkie BOM dla produktu"""
        boms = self.env['mrp.bom'].search([('product_tmpl_id', '=', self.id)])
        
        if len(boms) == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Receptura (BOM)'),
                'res_model': 'mrp.bom',
                'res_id': boms.id,
                'view_mode': 'form',
                'target': 'current',
            }
        elif len(boms) > 1:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Receptury (BOM)'),
                'res_model': 'mrp.bom',
                'domain': [('product_tmpl_id', '=', self.id)],
                'view_mode': 'tree,form',
                'target': 'current',
            }
        else:
            return self.action_create_bom()

    def get_surface_area_m2(self):
        """Oblicza powierzchnię w m² dla formatek i płyt"""
        self.ensure_one()
        
        if self.furniture_type == 'formatka' and self.dlugosc and self.szerokosc:
            area_mm2 = self.dlugosc * self.szerokosc
            return area_mm2 / 1000000
        
        elif self.furniture_type == 'plyta_meblowa' and self.plate_length and self.plate_width:
            area_mm2 = self.plate_length * self.plate_width
            return area_mm2 / 1000000
        
        return 0.0

    def get_perimeter_m(self):
        """Oblicza obwód w metrach dla formatek i płyt"""
        self.ensure_one()
        
        if self.furniture_type == 'formatka' and self.dlugosc and self.szerokosc:
            perimeter_mm = 2 * (self.dlugosc + self.szerokosc)
            return perimeter_mm / 1000
        
        elif self.furniture_type == 'plyta_meblowa' and self.plate_length and self.plate_width:
            perimeter_mm = 2 * (self.plate_length + self.plate_width)
            return perimeter_mm / 1000
        
        return 0.0