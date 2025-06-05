from odoo import models, fields, api

class FurnitureColor(models.Model):
    _name = 'furniture.color'
    _description = 'Kolory płyt meblowych'
    _order = 'sequence, name'
    
    name = fields.Char('Nazwa koloru', required=True)
    code = fields.Char('Kod koloru', required=True, help="Kod używany w systemie, np. 18_BIALY")
    thickness = fields.Float('Grubość (mm)', help="Grubość płyty w mm")
    description = fields.Text('Opis')
    active = fields.Boolean('Aktywny', default=True)
    sequence = fields.Integer('Kolejność', default=10)
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Kod koloru musi być unikalny!')
    ]
    
    def name_get(self):
        result = []
        for record in self:
            if record.thickness:
                name = f"{record.name} ({record.thickness}mm)"
            else:
                name = record.name
            result.append((record.id, name))
        return result

class FurnitureProductType(models.Model):
    _name = 'furniture.product.type'
    _description = 'Rodzaje produktów meblowych'
    _order = 'sequence, name'
    
    name = fields.Char('Nazwa', required=True)
    code = fields.Char('Kod', required=True, help="Kod używany w systemie, np. BOK-L")
    description = fields.Text('Opis')
    active = fields.Boolean('Aktywny', default=True)
    sequence = fields.Integer('Kolejność', default=10)
    requires_drilling = fields.Boolean('Wymaga wiercenia', default=True)
    requires_edging = fields.Boolean('Wymaga oklejania', default=True)
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Kod rodzaju produktu musi być unikalny!')
    ]

class FurnitureSeries(models.Model):
    _name = 'furniture.series'
    _description = 'Serie mebli'
    _order = 'sequence, name'
    
    name = fields.Char('Nazwa serii', required=True)
    code = fields.Char('Kod serii', required=True)
    description = fields.Text('Opis serii')
    active = fields.Boolean('Aktywny', default=True)
    sequence = fields.Integer('Kolejność', default=10)
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Kod serii musi być unikalny!')
    ]

class FurnitureDrillingType(models.Model):
    _name = 'furniture.drilling.type'
    _description = 'Typy wiercenia'
    _order = 'sequence, name'
    
    name = fields.Char('Nazwa', required=True)
    code = fields.Char('Kod', required=True, help="Kod typu wiercenia, np. TTTT")
    description = fields.Text('Opis wiercenia')
    active = fields.Boolean('Aktywny', default=True)
    sequence = fields.Integer('Kolejność', default=10)
    drilling_cost = fields.Float('Koszt wiercenia', help="Dodatkowy koszt za ten typ wiercenia")
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Kod typu wiercenia musi być unikalny!')
    ]

class WarehouseLocation(models.Model):
    _name = 'warehouse.location.custom'
    _description = 'Lokalizacje magazynowe'
    _order = 'sequence, name'
    
    name = fields.Char('Nazwa lokalizacji', required=True)
    code = fields.Char('Kod lokalizacji', required=True)
    warehouse_type = fields.Selection([
        ('raw_materials', 'Surowce'),
        ('components', 'Formatki'),
        ('finished_goods', 'Produkty gotowe'),
        ('packaging', 'Pakowanie'),
    ], string='Typ magazynu', required=True)
    description = fields.Text('Opis')
    active = fields.Boolean('Aktywny', default=True)
    sequence = fields.Integer('Kolejność', default=10)
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Kod lokalizacji musi być unikalny!')
    ]

class FurnitureEdging(models.Model):
    _name = 'furniture.edging'
    _description = 'Rodzaje oklein'
    _order = 'sequence, name'
    
    name = fields.Char('Nazwa okleiny', required=True)
    code = fields.Char('Kod okleiny', required=True)
    thickness = fields.Float('Grubość okleiny (mm)')
    color = fields.Char('Kolor')
    description = fields.Text('Opis')
    active = fields.Boolean('Aktywny', default=True)
    sequence = fields.Integer('Kolejność', default=10)
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Kod okleiny musi być unikalny!')
    ]

class FurnitureNamePart(models.Model):
    _name = 'furniture.name.part'
    _description = 'Części nazw produktów'
    _order = 'sequence, name'
    
    name = fields.Char('Nazwa części', required=True)
    code = fields.Char('Kod części', required=True)
    part_type = fields.Selection([
        ('cz1', 'cz1'),
        ('cz2', 'cz2'),
    ], string='Typ części', required=True)
    description = fields.Text('Opis')
    active = fields.Boolean('Aktywny', default=True)
    sequence = fields.Integer('Kolejność', default=10)
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Kod części musi być unikalny!')
    ]

class FurnitureEdging(models.Model):
    _name = 'furniture.edging'
    _description = 'Rodzaje oklein'
    _order = 'sequence, name'
    
    name = fields.Char('Nazwa okleiny', required=True)
    code = fields.Char('Kod okleiny', required=True)
    thickness = fields.Float('Grubość okleiny (mm)')
    color = fields.Char('Kolor')
    description = fields.Text('Opis')
    active = fields.Boolean('Aktywny', default=True)
    sequence = fields.Integer('Kolejność', default=10)
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Kod okleiny musi być unikalny!')
    ]

class FurnitureNamePart(models.Model):
    _name = 'furniture.name.part'
    _description = 'Części nazw produktów'
    _order = 'sequence, name'
    
    name = fields.Char('Nazwa części', required=True)
    code = fields.Char('Kod części', required=True)
    part_type = fields.Selection([
        ('cz1', 'cz1'),
        ('cz2', 'cz2'),
    ], string='Typ części', required=True)
    description = fields.Text('Opis')
    active = fields.Boolean('Aktywny', default=True)
    sequence = fields.Integer('Kolejność', default=10)
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Kod części musi być unikalny!')
    ]
