# -*- coding: utf-8 -*-
# Part of Alpma. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # === POLA PODSTAWOWE ALPMA ===
    typ_meblarski = fields.Selection([
        ('zestaw', 'Zestaw'),
        ('produkt_pojedynczy', 'Produkt pojedynczy'),
        ('formatka', 'Formatka'),
        ('okucia', 'Okucia'),
        ('akcesoria', 'Akcesoria'),
        ('karton', 'Karton'),
        ('styropian', 'Styropian'),
        ('plyta', 'Płyta meblowa'),
        ('obrzeza', 'Obrzeża')
    ], string='Typ meblarski', default='produkt_pojedynczy',
       help="Określa typ produktu w systemie produkcji Alpma")

    # === SERIA PRODUKTOWA ===
    seria_produktowa = fields.Many2one(
        'product.category', 
        string='Seria produktowa',
        domain="[('is_alpma_series', '=', True)]",
        help="Seria produktowa: VB, SUPRA, TRES, ALTUS itp."
    )

    # === PARAMETRY FORMATKI (cz1, cz2) ===
    cz1 = fields.Char(
        string='cz1 (Część 1)',
        help="Pierwsza część nazwy formatki (np. BOK-L, POLKA, DRZWI)"
    )
    
    cz2 = fields.Char(
        string='cz2 (Seria)',
        help="Seria szafki (VB, SUPRA, TRES itp.) - wymagane"
    )

    # === WYMIARY PODSTAWOWE (FORMATKI I MEBLE) ===
    dlugosc_cm = fields.Float(
        string='Długość (cm)',
        digits=(8, 1),
        help="Długość formatki/mebla w centymetrach"
    )
    
    szerokosc_cm = fields.Float(
        string='Szerokość (cm)',
        digits=(8, 1),
        help="Szerokość formatki/mebla w centymetrach"
    )

    # === ROZMIAR STANDARDOWY (dla formatek) ===
    rozmiar_dlugosc = fields.Float(
        string='Rozmiar Długość',
        digits=(8, 1),
        help="Standardowy rozmiar długości dla formatki"
    )
    
    rozmiar_szerokosc = fields.Float(
        string='Rozmiar Szerokość',
        digits=(8, 1),
        help="Standardowy rozmiar szerokości dla formatki"
    )

    # === WYMIAR DODATKOWY DLA MEBLI ===
    wysokosc_cm = fields.Float(
        string='Wysokość (cm)', 
        digits=(8, 1),
        help="Wysokość mebla w centymetrach (tylko dla produktów i zestawów)"
    )

    # === GRUBOŚĆ FORMATKI (z płyty) ===
    plyta_bazowa = fields.Many2one(
        'product.template',
        string='Płyta bazowa',
        domain="[('typ_meblarski', '=', 'plyta')]",
        help="Płyta z której jest krojona formatka"
    )

    grubosc_mm = fields.Float(
        string='Grubość (mm)',
        compute='_compute_grubosc',
        store=True,
        digits=(8, 1),
        help="Grubość formatki pobrana z płyty bazowej"
    )

    # === KOLOR/MATERIAŁ (z płyty lub własny) ===
    kolor_material = fields.Char(
        string='Kolor/Materiał',
        compute='_compute_kolor_material',
        store=True,
        help="Kolor lub materiał pobierany z płyty bazowej lub własny"
    )

    kolor_manual = fields.Char(
        string='Kolor (ręczny)',
        help="Ręcznie wprowadzony kolor (jeśli różny od płyty)"
    )

    # === OBRZEŻA FORMATKI (4 strony) ===
    ok1_obrzeze = fields.Many2one(
        'product.template',
        string='ok1 - Długość góra',
        domain="[('typ_meblarski', '=', 'obrzeza')]",
        help="Obrzeże na długość góra formatki"
    )
    
    ok2_obrzeze = fields.Many2one(
        'product.template',
        string='ok2 - Szerokość prawa',
        domain="[('typ_meblarski', '=', 'obrzeza')]",
        help="Obrzeże na szerokość prawa formatki"
    )
    
    ok3_obrzeze = fields.Many2one(
        'product.template',
        string='ok3 - Długość dół',
        domain="[('typ_meblarski', '=', 'obrzeza')]",
        help="Obrzeże na długość dół formatki"
    )
    
    ok4_obrzeze = fields.Many2one(
        'product.template',
        string='ok4 - Szerokość lewa',
        domain="[('typ_meblarski', '=', 'obrzeza')]",
        help="Obrzeże na szerokość lewa formatki"
    )

    # === SZYBKIE PRZYPISANIE OBRZEŻY ===
    wszystkie_obrzeza = fields.Many2one(
        'product.template',
        string='Wszystkie obrzeża',
        domain="[('typ_meblarski', '=', 'obrzeza')]",
        help="Wybierz obrzeże do przypisania na wszystkie strony"
    )

    # === PARAMETRY OKUĆ ===
    dlugosc_okucia_mm = fields.Float(
        string='Długość okucia (mm)',
        digits=(8, 0),
        help="Długość okucia w milimetrach (np. prowadnica 450mm)"
    )

    nosnosc_kg = fields.Float(
        string='Nośność (kg)',
        digits=(8, 1),
        help="Nośność okucia w kilogramach"
    )

    # === PARAMETRY OBRZEŻY ===
    szerokosc_obrzeza_mm = fields.Float(
        string='Szerokość obrzeża (mm)',
        digits=(8, 1),
        help="Szerokość obrzeża w milimetrach (np. 22mm, 45mm)"
    )

    grubosc_obrzeza_mm = fields.Float(
        string='Grubość obrzeża (mm)',
        digits=(8, 1),
        help="Grubość obrzeża w milimetrach (np. 0.5mm, 0.8mm, 1mm, 2mm)"
    )

    dlugosc_rolki_m = fields.Float(
        string='Długość rolki (m)',
        digits=(8, 0),
        help="Długość rolki obrzeża w metrach (np. 50m)"
    )

    # === PARAMETRY PŁYT ===
    grubosc_plyty_mm = fields.Float(
        string='Grubość płyty (mm)',
        digits=(8, 1),
        help="Grubość płyty meblowej w milimetrach (np. 18mm)"
    )

    # === GRUPA PRODUKCYJNA ===
    grupa_produkcyjna = fields.Char(
        string='Grupa produkcyjna',
        help="Grupa dla optymalizacji produkcji i grupowania"
    )

    # === POLA OBLICZANE ===
    wymiary_display = fields.Char(
        string='Wymiary',
        compute='_compute_wymiary_display',
        store=True,
        help="Wyświetlane wymiary w zależności od typu"
    )

    objetosc_m3 = fields.Float(
        string='Objętość (m³)',
        compute='_compute_objetosc',
        store=True,
        digits=(10, 4),
        help="Objętość produktu w metrach sześciennych"
    )

    powierzchnia_m2 = fields.Float(
        string='Powierzchnia (m²)',
        compute='_compute_powierzchnia',
        store=True,
        digits=(10, 4),
        help="Powierzchnia formatki/płyty w metrach kwadratowych"
    )

    # === OZNACZENIA ===
    is_alpma_product = fields.Boolean(
        string='Produkt Alpma',
        default=True,
        help="Czy to jest produkt zarządzany przez system Alpma"
    )

    # === COMPUTE METHODS ===
    @api.depends('plyta_bazowa', 'plyta_bazowa.grubosc_plyty_mm')
    def _compute_grubosc(self):
        """Oblicza grubość formatki na podstawie płyty bazowej"""
        for record in self:
            if record.typ_meblarski == 'formatka' and record.plyta_bazowa and record.plyta_bazowa.grubosc_plyty_mm:
                record.grubosc_mm = record.plyta_bazowa.grubosc_plyty_mm
            elif record.typ_meblarski == 'plyta' and record.grubosc_plyty_mm:
                record.grubosc_mm = record.grubosc_plyty_mm
            else:
                record.grubosc_mm = 0.0

    @api.depends('plyta_bazowa', 'plyta_bazowa.kolor_manual', 'kolor_manual')
    def _compute_kolor_material(self):
        """Oblicza kolor na podstawie płyty bazowej lub ręcznego wprowadzenia"""
        for record in self:
            if record.typ_meblarski == 'formatka' and record.plyta_bazowa and record.plyta_bazowa.kolor_manual:
                record.kolor_material = record.plyta_bazowa.kolor_manual
            elif record.kolor_manual:
                record.kolor_material = record.kolor_manual
            else:
                record.kolor_material = ""

    @api.depends('typ_meblarski', 'cz1', 'cz2', 'rozmiar_dlugosc', 'rozmiar_szerokosc', 'dlugosc_cm', 'szerokosc_cm', 'kolor_material')
    def _compute_wymiary_display(self):
        """Oblicza string wymiarów i generuje nazwę automatycznie"""
        for record in self:
            if record.typ_meblarski == 'formatka':
                # Generuj nazwę według formuły z Airtable
                nazwa_gen = record._generate_nazwa_formatki()
                if nazwa_gen and nazwa_gen != record.name:
                    record.name = nazwa_gen
                    
                # Format wymiarów: 390x280x18mm BIAŁY
                if record.dlugosc_cm and record.szerokosc_cm:
                    wymiary = f"{record.dlugosc_cm:g}x{record.szerokosc_cm:g}"
                    if record.grubosc_mm:
                        wymiary += f"x{record.grubosc_mm:g}mm"
                    if record.kolor_material:
                        wymiary += f" {record.kolor_material}"
                    record.wymiary_display = wymiary
                else:
                    record.wymiary_display = ""
                    
            elif record.typ_meblarski in ['produkt_pojedynczy', 'zestaw']:
                # Format: 60x30x90 cm (DługośćxSzerokośćxWysokość)
                wymiary = []
                if record.dlugosc_cm:
                    wymiary.append(f"{record.dlugosc_cm:g}")
                if record.szerokosc_cm:
                    wymiary.append(f"{record.szerokosc_cm:g}")
                if record.wysokosc_cm:
                    wymiary.append(f"{record.wysokosc_cm:g}")
                
                if wymiary:
                    record.wymiary_display = "x".join(wymiary) + " cm"
                else:
                    record.wymiary_display = ""
                    
            elif record.typ_meblarski == 'okucia':
                # Format: 450mm (25kg)
                if record.dlugosc_okucia_mm:
                    wymiary = f"{record.dlugosc_okucia_mm:g}mm"
                    if record.nosnosc_kg:
                        wymiary += f" ({record.nosnosc_kg:g}kg)"
                    record.wymiary_display = wymiary
                else:
                    record.wymiary_display = ""
                    
            elif record.typ_meblarski == 'obrzeza':
                # Format: 22x0.8mm x 50m BIAŁY
                wymiary_parts = []
                if record.szerokosc_obrzeza_mm:
                    wymiary_parts.append(f"{record.szerokosc_obrzeza_mm:g}")
                if record.grubosc_obrzeza_mm:
                    if wymiary_parts:
                        wymiary_parts[0] += f"x{record.grubosc_obrzeza_mm:g}mm"
                    else:
                        wymiary_parts.append(f"{record.grubosc_obrzeza_mm:g}mm")
                elif wymiary_parts:
                    wymiary_parts[0] += "mm"
                
                if record.dlugosc_rolki_m:
                    wymiary_parts.append(f"{record.dlugosc_rolki_m:g}m")
                
                wymiary = " x ".join(wymiary_parts) if wymiary_parts else ""
                
                if record.kolor_material and wymiary:
                    wymiary += f" {record.kolor_material}"
                
                record.wymiary_display = wymiary
                    
            elif record.typ_meblarski == 'plyta':
                # Format: 2800x2070x18mm BIAŁY
                if record.dlugosc_cm and record.szerokosc_cm:
                    wymiary = f"{record.dlugosc_cm:g}x{record.szerokosc_cm:g}"
                    if record.grubosc_plyty_mm:
                        wymiary += f"x{record.grubosc_plyty_mm:g}mm"
                    if record.kolor_material:
                        wymiary += f" {record.kolor_material}"
                    record.wymiary_display = wymiary
                else:
                    record.wymiary_display = ""
            else:
                record.wymiary_display = ""

    def _generate_nazwa_formatki(self):
        """Generuje nazwę formatki według formuły z Airtable"""
        self.ensure_one()
        
        if not self.cz1:
            return ""
            
        nazwa_parts = [self.cz1]
        
        # Dodaj rozmiar jeśli jest
        if self.rozmiar_dlugosc and self.rozmiar_szerokosc:
            nazwa_parts.append(f"{self.rozmiar_dlugosc:g}x{self.rozmiar_szerokosc:g}")
        elif self.rozmiar_dlugosc:
            nazwa_parts.append(f"{self.rozmiar_dlugosc:g}")
        elif self.rozmiar_szerokosc:
            nazwa_parts.append(f"{self.rozmiar_szerokosc:g}")
            
        # Dodaj cz2 jeśli jest
        if self.cz2:
            nazwa_parts.append(self.cz2)
            
        # Dodaj wymiary rzeczywiste
        if self.dlugosc_cm:
            if self.szerokosc_cm:
                nazwa_parts.append(f"{self.dlugosc_cm:g}x{self.szerokosc_cm:g}")
            else:
                nazwa_parts.append(f"{self.dlugosc_cm:g}")
                
        # Dodaj kolor
        if self.kolor_material:
            nazwa_parts.append(self.kolor_material)
            
        return "-".join(nazwa_parts)

    @api.depends('typ_meblarski', 'dlugosc_cm', 'szerokosc_cm', 'wysokosc_cm')
    def _compute_objetosc(self):
        """Oblicza objętość w m³ dla produktów meblarskich"""
        for record in self:
            if record.typ_meblarski in ['produkt_pojedynczy', 'zestaw'] and record.dlugosc_cm and record.szerokosc_cm and record.wysokosc_cm:
                # Konwersja z cm³ na m³
                record.objetosc_m3 = (record.dlugosc_cm * record.szerokosc_cm * record.wysokosc_cm) / 1000000
            else:
                record.objetosc_m3 = 0.0

    @api.depends('typ_meblarski', 'dlugosc_cm', 'szerokosc_cm')
    def _compute_powierzchnia(self):
        """Oblicza powierzchnię w m² dla formatek i płyt"""
        for record in self:
            if record.typ_meblarski in ['formatka', 'plyta'] and record.dlugosc_cm and record.szerokosc_cm:
                # Konwersja z cm² na m²
                record.powierzchnia_m2 = (record.dlugosc_cm * record.szerokosc_cm) / 10000
            else:
                record.powierzchnia_m2 = 0.0

    # === CONSTRAINTS ===
    @api.constrains('dlugosc_cm', 'szerokosc_cm', 'wysokosc_cm', 'grubosc_plyty_mm', 'grubosc_obrzeza_mm')
    def _check_dimensions(self):
        """Sprawdza poprawność wymiarów"""
        for record in self:
            if record.dlugosc_cm and record.dlugosc_cm <= 0:
                raise ValidationError(_("Długość musi być większa od 0"))
            if record.szerokosc_cm and record.szerokosc_cm <= 0:
                raise ValidationError(_("Szerokość musi być większa od 0"))
            if record.wysokosc_cm and record.wysokosc_cm <= 0:
                raise ValidationError(_("Wysokość musi być większa od 0"))
            if record.grubosc_plyty_mm and record.grubosc_plyty_mm <= 0:
                raise ValidationError(_("Grubość płyty musi być większa od 0"))
            if record.grubosc_obrzeza_mm and record.grubosc_obrzeza_mm <= 0:
                raise ValidationError(_("Grubość obrzeża musi być większa od 0"))

    # === ONCHANGE METHODS ===
    @api.onchange('typ_meblarski')
    def _onchange_typ_meblarski(self):
        """Ustawia domyślne wartości na podstawie typu"""
        if self.typ_meblarski == 'formatka':
            self.type = 'product'
            self.tracking = 'lot'
        elif self.typ_meblarski == 'zestaw':
            self.type = 'product'
        elif self.typ_meblarski in ['okucia', 'akcesoria']:
            self.type = 'product'
            self.tracking = 'none'
        elif self.typ_meblarski == 'plyta':
            self.type = 'product'
            self.tracking = 'lot'

    # === ACTIONS ===
    def action_assign_all_edges(self):
        """Przypisuje wybrane obrzeże do wszystkich 4 stron"""
        for record in self:
            if record.wszystkie_obrzeza:
                record.ok1_obrzeze = record.wszystkie_obrzeza
                record.ok2_obrzeze = record.wszystkie_obrzeza
                record.ok3_obrzeze = record.wszystkie_obrzeza
                record.ok4_obrzeze = record.wszystkie_obrzeza
