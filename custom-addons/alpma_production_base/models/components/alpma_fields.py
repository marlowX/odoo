# -*- coding: utf-8 -*-
# Part of Alpma. See LICENSE file for full copyright and licensing details.

from odoo import fields

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

# === POWIĄZANIE Z PRODUKTEM GOTOWYM ===
produkt_powiazany = fields.Many2one(
    'product.template',
    string='Produkt powiązany',
    domain="[('typ_meblarski', 'in', ['produkt_pojedynczy', 'zestaw'])]",
    help="SKU produktu gotowego do którego należy ta formatka"
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

# === PARAMETRY SZAFEK (ROZWIJALNE LISTY) ===
parametr_nogi = fields.Many2one(
    'alpma.cabinet.param.nogi',
    string='Parametr nogi',
    help="Typ nóg dla szafki"
)

parametr_uchyt = fields.Many2one(
    'alpma.cabinet.param.uchyt',
    string='Parametr uchyt',
    help="Typ uchwytu dla szafki"
)

parametr_drzwi = fields.Many2one(
    'alpma.cabinet.param.drzwi',
    string='Parametr drzwi',
    help="Typ drzwi dla szafki"
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

# === INTEGRACJE ===
airtable_record_id = fields.Char(
    string='Airtable Record ID',
    help="ID rekordu w Airtable dla synchronizacji"
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

# === WIDOCZNOŚĆ SKU ===
show_sku_field = fields.Boolean(
    string='Pokaż SKU',
    compute='_compute_show_sku',
    help="Czy pokazać pole SKU dla tego typu produktu"
)

# Nowe parametry - typ formatki i typ szafki
parametr_typ_formatki = fields.Many2one(
    'alpma.cabinet.param.typ_formatki',
    string='Typ formatki',
    help='Typ formatki (BOK-L, WG, DRZWI, etc.)'
)

parametr_typ_szafki = fields.Many2one(
    'alpma.cabinet.param.typ_szafki', 
    string='Typ szafki',
    help='Typ/seria szafki (VB, TRES, ALTUS, SUPRA)'
)
