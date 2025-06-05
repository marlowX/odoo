from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    # Wymiary
    dlugosc = fields.Float('Długość (mm)')
    szerokosc = fields.Float('Szerokość (mm)')
    wysokosc = fields.Float('Wysokość (mm)')
    grubosc = fields.Float('Grubość (mm)', default=18.0)
    
    # Części nazwy - jako Many2one
    cz1_id = fields.Many2one('furniture.name.part', string='cz1', domain="[('part_type', '=', 'cz1')]")
    cz2_id = fields.Many2one('furniture.name.part', string='cz2', domain="[('part_type', '=', 'cz2')]")
    
    # Okleiny - jako Many2one
    okleina1_id = fields.Many2one('furniture.edging', string='Okleina 1')
    okleina2_id = fields.Many2one('furniture.edging', string='Okleina 2')
    okleina3_id = fields.Many2one('furniture.edging', string='Okleina 3')
    okleina4_id = fields.Many2one('furniture.edging', string='Okleina 4')
    
    # Stare pola tekstowe dla kompatybilności
    cz1 = fields.Char('cz1', compute='_compute_cz1_code', store=True)
    cz2 = fields.Char('cz2', compute='_compute_cz2_code', store=True)
    okleina1 = fields.Char('Okleina 1', compute='_compute_okleina1_code', store=True)
    okleina2 = fields.Char('Okleina 2', compute='_compute_okleina2_code', store=True)
    okleina3 = fields.Char('Okleina 3', compute='_compute_okleina3_code', store=True)
    okleina4 = fields.Char('Okleina 4', compute='_compute_okleina4_code', store=True)
    
    # Many2one pola
    kolor_plyty_id = fields.Many2one('furniture.color', string='Kolor płyty')
    rodzaj_produktu_id = fields.Many2one('furniture.product.type', string='Rodzaj produktu')
    seria_mebla_id = fields.Many2one('furniture.series', string='Seria mebla')
    wiercenie_id = fields.Many2one('furniture.drilling.type', string='Typ wiercenia')
    lokalizacja_magazyn_id = fields.Many2one('warehouse.location.custom', string='Lokalizacja magazynowa')
    
    # Computed pola
    kolor_plyty = fields.Char('Kod koloru', compute='_compute_kolor_code', store=True)
    rodzaj_produktu = fields.Char('Kod rodzaju', compute='_compute_rodzaj_code', store=True)
    seria_mebla = fields.Char('Kod serii', compute='_compute_seria_code', store=True)
    wiercenie = fields.Char('Kod wiercenia', compute='_compute_wiercenie_code', store=True)
    
    # Boolean pola
    oklejanie = fields.Boolean('Wymaga oklejania', default=True)
    na_magazynie = fields.Boolean('Trzymaj na magazynie')
    produkt_zestawu = fields.Boolean('Część zestawu')
    wymaga_wiercenia = fields.Boolean('Wymaga wiercenia', default=True)
    czy_formatka = fields.Boolean('To jest formatka')
    formatka_generowana = fields.Boolean('Automatycznie generowana')
    
    # Integracje
    sellasist_sku = fields.Char('SKU Sellasist')
    airtable_record_id = fields.Char('ID rekordu Airtable')
    ean_code = fields.Char('Kod EAN')
    
    # Nazwy
    nazwa_gen = fields.Char('Nazwa generowana')
    nazwa_wiertarka = fields.Char('Nazwa dla wiertarki')
    nazwa_krotka = fields.Char('Nazwa krótka')
    
    # Computed methods
    @api.depends('cz1_id')
    def _compute_cz1_code(self):
        for record in self:
            record.cz1 = record.cz1_id.code if record.cz1_id else ''
    
    @api.depends('cz2_id')
    def _compute_cz2_code(self):
        for record in self:
            record.cz2 = record.cz2_id.code if record.cz2_id else ''
    
    @api.depends('okleina1_id')
    def _compute_okleina1_code(self):
        for record in self:
            record.okleina1 = record.okleina1_id.code if record.okleina1_id else ''
    
    @api.depends('okleina2_id')
    def _compute_okleina2_code(self):
        for record in self:
            record.okleina2 = record.okleina2_id.code if record.okleina2_id else ''
    
    @api.depends('okleina3_id')
    def _compute_okleina3_code(self):
        for record in self:
            record.okleina3 = record.okleina3_id.code if record.okleina3_id else ''
    
    @api.depends('okleina4_id')
    def _compute_okleina4_code(self):
        for record in self:
            record.okleina4 = record.okleina4_id.code if record.okleina4_id else ''
    
    @api.depends('kolor_plyty_id')
    def _compute_kolor_code(self):
        for record in self:
            record.kolor_plyty = record.kolor_plyty_id.code if record.kolor_plyty_id else ''
    
    @api.depends('rodzaj_produktu_id')
    def _compute_rodzaj_code(self):
        for record in self:
            record.rodzaj_produktu = record.rodzaj_produktu_id.code if record.rodzaj_produktu_id else ''
    
    @api.depends('seria_mebla_id')
    def _compute_seria_code(self):
        for record in self:
            record.seria_mebla = record.seria_mebla_id.code if record.seria_mebla_id else ''
    
    @api.depends('wiercenie_id')
    def _compute_wiercenie_code(self):
        for record in self:
            record.wiercenie = record.wiercenie_id.code if record.wiercenie_id else ''

    # Kategorie produktów
    furniture_category = fields.Selection([
        ('raw_material', 'Surowiec'),
        ('component', 'Formatka'), 
        ('finished_product', 'Produkt gotowy'),
        ('edge_material', 'Obrzeże'),
        ('hardware', 'Okucie'),
    ], string='Kategoria meblarska')
    
    # Dla surowców - płyt meblowych
    plate_length = fields.Float('Długość płyty (mm)', help="Dla płyt surowcowych")
    plate_width = fields.Float('Szerokość płyty (mm)', help="Dla płyt surowcowych") 
    plate_supplier = fields.Char('Dostawca płyty')
    plate_color_name = fields.Char('Nazwa koloru u dostawcy')
    
    # Dla obrzeży
    edge_length_total = fields.Float('Długość obrzeża (mb)', help="Całkowita długość obrzeża w metrach bieżących")
    edge_width = fields.Float('Szerokość obrzeża (mm)')
    edge_supplier = fields.Char('Dostawca obrzeża')
    
    # Parametry magazynowe
    min_stock_level = fields.Float('Minimalny stan magazynowy')
    max_stock_level = fields.Float('Maksymalny stan magazynowy')
    reorder_point = fields.Float('Punkt ponownego zamówienia')
    lead_time_days = fields.Integer('Czas dostawy (dni)')
    
    # Jednostki miary dla różnych typów
    uom_type = fields.Selection([
        ('piece', 'Sztuka'),
        ('m2', 'Metr kwadratowy'),
        ('mb', 'Metr bieżący'),
        ('kg', 'Kilogram'),
    ], string='Typ jednostki')

    def action_create_bom(self):
        """Tworzy BOM dla formatki"""
        if self.furniture_category == 'component':
            bom = self.env['furniture.bom'].create_bom_from_formatka(self.id)
            if bom:
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Receptura (BOM)',
                    'res_model': 'furniture.bom',
                    'res_id': bom.id,
                    'view_mode': 'form',
                    'target': 'current',
                }
        return {'type': 'ir.actions.act_window_close'}
    
    def action_view_bom(self):
        """Otwiera BOM dla produktu"""
        boms = self.env['furniture.bom'].search([('product_tmpl_id', '=', self.id)])
        if boms:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Receptury (BOM)',
                'res_model': 'furniture.bom',
                'domain': [('product_tmpl_id', '=', self.id)],
                'view_mode': 'tree,form',
                'target': 'current',
            }
        return self.action_create_bom()

    def action_create_multiple_boms(self):
        """Tworzy BOM dla wielu formatek naraz - akcja zbiorcza"""
        _logger.info(f"=== ROZPOCZĘCIE ZBIORCZEGO TWORZENIA BOM DLA {len(self)} FORMATEK ===")
        
        success_count = 0
        error_count = 0
        
        for formatka in self:
            if formatka.czy_formatka and formatka.furniture_category == 'component':
                try:
                    # Sprawdź czy BOM już istnieje
                    existing_bom = self.env['furniture.bom'].search([
                        ('product_tmpl_id', '=', formatka.id)
                    ], limit=1)
                    
                    if not existing_bom:
                        _logger.info(f"Tworzę BOM dla formatki: {formatka.name}")
                        bom = self.env['furniture.bom'].create_bom_from_formatka(formatka.id)
                        if bom:
                            success_count += 1
                            _logger.info(f"✅ BOM utworzony dla {formatka.name}")
                        else:
                            error_count += 1
                            _logger.warning(f"❌ Nie udało się utworzyć BOM dla {formatka.name}")
                    else:
                        _logger.info(f"BOM już istnieje dla {formatka.name}, pomijam...")
                        
                except Exception as e:
                    error_count += 1
                    _logger.error(f"❌ Błąd tworzenia BOM dla {formatka.name}: {e}")
            else:
                _logger.warning(f"Produkt {formatka.name} nie jest formatką, pomijam...")
        
        _logger.info(f"=== ZAKOŃCZENIE ZBIORCZEGO TWORZENIA BOM ===")
        _logger.info(f"Sukces: {success_count}, Błędy: {error_count}")
        
        # Pokaż komunikat użytkownikowi
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Zbiorcze tworzenie BOM',
                'message': f'Utworzono {success_count} receptur. Błędów: {error_count}',
                'type': 'success' if error_count == 0 else 'warning',
                'sticky': False,
            }
        }
