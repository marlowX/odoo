from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class FurnitureBOM(models.Model):
    _name = 'furniture.bom'
    _description = 'Receptura meblarska (BOM)'
    _rec_name = 'product_tmpl_id'
    
    # Produkt końcowy (formatka)
    product_tmpl_id = fields.Many2one('product.template', string='Produkt (formatka)', required=True, 
                                     domain="[('furniture_category', '=', 'component')]")
    product_id = fields.Many2one('product.product', string='Wariant produktu', 
                                domain="[('product_tmpl_id', '=', product_tmpl_id)]")
    
    # Informacje podstawowe
    code = fields.Char('Kod BOM')
    sequence = fields.Integer('Kolejność', default=10)
    type = fields.Selection([
        ('normal', 'Produkcja'),
        ('phantom', 'Zestaw (phantom)'),
    ], string='Typ BOM', default='normal', required=True)
    
    # Ilości
    product_qty = fields.Float('Ilość do wyprodukowania', default=1.0, required=True)
    product_uom_id = fields.Many2one('uom.uom', string='Jednostka miary', required=True)
    
    # Linie BOM (surowce)
    bom_line_ids = fields.One2many('furniture.bom.line', 'bom_id', string='Składniki')
    
    # Obliczenia
    total_cost = fields.Float('Całkowity koszt', compute='_compute_total_cost', store=True)
    
    # Aktywność
    active = fields.Boolean('Aktywny', default=True)
    
    @api.depends('bom_line_ids.subtotal')
    def _compute_total_cost(self):
        for bom in self:
            bom.total_cost = sum(line.subtotal for line in bom.bom_line_ids)
    
    @api.model
    def create_bom_from_formatka(self, formatka_id):
        """Automatyczne tworzenie BOM na podstawie parametrów formatki"""
        _logger.info(f"=== ROZPOCZĘCIE TWORZENIA BOM DLA FORMATKI ID: {formatka_id} ===")
        
        formatka = self.env['product.template'].browse(formatka_id)
        _logger.info(f"Znaleziono formatkę: {formatka.name}")
        _logger.info(f"Czy formatka: {formatka.czy_formatka}")
        _logger.info(f"Wymiary: {formatka.dlugosc}x{formatka.szerokosc}x{formatka.grubosc}")
        _logger.info(f"Kolor płyty ID: {formatka.kolor_plyty_id}")
        _logger.info(f"Kod koloru płyty: {formatka.kolor_plyty}")
        
        if not formatka.czy_formatka:
            _logger.warning(f"Produkt {formatka.name} nie jest formatką!")
            return False
        
        # Oblicz powierzchnię
        area_needed = (formatka.dlugosc * formatka.szerokosc) / 1000000  # mm² na m²
        _logger.info(f"Obliczona powierzchnia: {area_needed} m²")
        
        # Znajdź odpowiednią płytę surowcową na podstawie koloru i grubości
        plate_domain = [
            ('furniture_category', '=', 'raw_material'),
            ('grubosc', '=', formatka.grubosc)
        ]
        _logger.info(f"Szukam płyty z domeną: {plate_domain}")
        
        if formatka.kolor_plyty_id:
            plate_domain.append(('kolor_plyty_id', '=', formatka.kolor_plyty_id.id))
            _logger.info(f"Dodano filtr koloru: kolor_plyty_id = {formatka.kolor_plyty_id.id}")
        
        plate = self.env['product.template'].search(plate_domain, limit=1)
        _logger.info(f"Znaleziona płyta: {plate.name if plate else 'BRAK'}")
        
        if not plate:
            _logger.warning("Nie znaleziono odpowiedniej płyty! Szukam po kodzie...")
            # Alternatywne wyszukiwanie po kodzie
            plate_code = f"{formatka.grubosc}_{formatka.kolor_plyty}" if formatka.kolor_plyty else f"{formatka.grubosc}_BIALY"
            plate = self.env['product.template'].search([
                ('default_code', '=', plate_code),
                ('furniture_category', '=', 'raw_material')
            ], limit=1)
            _logger.info(f"Płyta znaleziona po kodzie {plate_code}: {plate.name if plate else 'NADAL BRAK'}")
        
        vals = {
            'product_tmpl_id': formatka.id,
            'code': f"BOM-{formatka.nazwa_gen or formatka.name}",
            'product_qty': 1.0,
            'product_uom_id': self.env.ref('uom.product_uom_unit').id,
        }
        
        _logger.info(f"Tworzę BOM z danymi: {vals}")
        bom = self.create(vals)
        _logger.info(f"BOM utworzony z ID: {bom.id}")
        
        # Dodaj linię dla płyty
        if plate:
            _logger.info(f"Dodaję płytę do BOM: {plate.name}")
            try:
                line_vals = {
                    'bom_id': bom.id,
                    'product_tmpl_id': plate.id,
                    'product_qty': area_needed,
                    'product_uom_id': self.env.ref('uom.product_uom_meter').id,  # m²
                }
                _logger.info(f"Dane linii płyty: {line_vals}")
                plate_line = self.env['furniture.bom.line'].create(line_vals)
                _logger.info(f"Linia płyty utworzona z ID: {plate_line.id}")
            except Exception as e:
                _logger.error(f"Błąd tworzenia linii płyty: {e}")
        else:
            _logger.error("BRAK PŁYTY - nie można dodać do BOM!")
        
        # Dodaj linie dla oklein (jeśli potrzebne)
        if formatka.oklejanie:
            perimeter = 2 * (formatka.dlugosc + formatka.szerokosc) / 1000  # mm na m
            _logger.info(f"Obliczony obwód: {perimeter} m")
            
            # Dla każdej okleiny
            for okleina_field in ['okleina1_id', 'okleina2_id', 'okleina3_id', 'okleina4_id']:
                okleina = getattr(formatka, okleina_field)
                if okleina:
                    _logger.info(f"Przetwarzam oklejkę: {okleina.code}")
                    # Znajdź odpowiednie obrzeże
                    edge_domain = [
                        ('furniture_category', '=', 'edge_material'),
                        ('name', 'ilike', okleina.code)
                    ]
                    edge = self.env['product.template'].search(edge_domain, limit=1)
                    
                    if not edge:
                        # Alternatywne wyszukiwanie po default_code
                        edge = self.env['product.template'].search([
                            ('default_code', '=', okleina.code),
                            ('furniture_category', '=', 'edge_material')
                        ], limit=1)
                    
                    _logger.info(f"Znalezione obrzeże dla {okleina.code}: {edge.name if edge else 'BRAK'}")
                    
                    if edge:
                        try:
                            edge_line_vals = {
                                'bom_id': bom.id,
                                'product_tmpl_id': edge.id,
                                'product_qty': perimeter / 4,  # Zakładamy 4 krawędzie
                                'product_uom_id': self.env.ref('uom.product_uom_meter').id,  # mb
                            }
                            _logger.info(f"Dane linii obrzeża: {edge_line_vals}")
                            edge_line = self.env['furniture.bom.line'].create(edge_line_vals)
                            _logger.info(f"Linia obrzeża utworzona z ID: {edge_line.id}")
                        except Exception as e:
                            _logger.error(f"Błąd tworzenia linii obrzeża {okleina.code}: {e}")
                    else:
                        _logger.warning(f"Nie znaleziono obrzeża dla {okleina.code}")
        
        _logger.info(f"=== ZAKOŃCZENIE TWORZENIA BOM DLA FORMATKI ID: {formatka_id} ===")
        return bom

class FurnitureBOMLine(models.Model):
    _name = 'furniture.bom.line'
    _description = 'Linia BOM - składnik'
    _rec_name = 'product_tmpl_id'
    
    # Powiązania
    bom_id = fields.Many2one('furniture.bom', string='BOM', required=True, ondelete='cascade')
    sequence = fields.Integer('Kolejność', default=10)
    
    # Produkt składnik (surowiec)
    product_tmpl_id = fields.Many2one('product.template', string='Surowiec', required=True,
                                     domain="[('furniture_category', 'in', ['raw_material', 'edge_material'])]")
    product_id = fields.Many2one('product.product', string='Wariant surowca',
                                domain="[('product_tmpl_id', '=', product_tmpl_id)]")
    
    # Ilości
    product_qty = fields.Float('Ilość potrzebna', required=True, default=1.0)
    product_uom_id = fields.Many2one('uom.uom', string='Jednostka miary', required=True)
    
    # Koszty
    product_cost = fields.Float('Koszt jednostkowy', related='product_tmpl_id.standard_price', readonly=True)
    subtotal = fields.Float('Koszt całkowity', compute='_compute_subtotal', store=True)
    
    # Dodatkowe informacje
    operation_id = fields.Many2one('furniture.operation', string='Operacja')
    notes = fields.Text('Uwagi')
    
    @api.depends('product_qty', 'product_cost')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.product_qty * line.product_cost

class FurnitureOperation(models.Model):
    _name = 'furniture.operation'
    _description = 'Operacje produkcyjne'
    
    name = fields.Char('Nazwa operacji', required=True)
    code = fields.Char('Kod operacji')
    operation_type = fields.Selection([
        ('cutting', 'Cięcie'),
        ('drilling', 'Wiercenie'),
        ('edging', 'Oklejanie'),
        ('assembly', 'Montaż'),
        ('finishing', 'Wykończenie'),
    ], string='Typ operacji')
    
    # Parametry czasowe
    setup_time = fields.Float('Czas przygotowania (min)')
    time_per_unit = fields.Float('Czas na jednostkę (min)')
    
    # Koszty
    cost_per_hour = fields.Float('Koszt za godzinę')
    
    # Maszyna/stanowisko
    workcenter_id = fields.Char('Stanowisko pracy')
    
    description = fields.Text('Opis operacji')
    active = fields.Boolean('Aktywny', default=True)
