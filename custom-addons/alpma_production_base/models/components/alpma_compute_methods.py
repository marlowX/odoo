# -*- coding: utf-8 -*-
# Part of Alpma. See LICENSE file for full copyright and licensing details.

from odoo import api


def _compute_grubosc(self):
    """Oblicza grubość formatki na podstawie płyty bazowej"""
    for record in self:
        if record.typ_meblarski == 'formatka' and record.plyta_bazowa and record.plyta_bazowa.grubosc_plyty_mm:
            record.grubosc_mm = record.plyta_bazowa.grubosc_plyty_mm
        elif record.typ_meblarski == 'plyta' and record.grubosc_plyty_mm:
            record.grubosc_mm = record.grubosc_plyty_mm
        else:
            record.grubosc_mm = 0.0


def _compute_kolor_material(self):
    """Oblicza kolor na podstawie płyty bazowej lub ręcznego wprowadzenia"""
    for record in self:
        if record.typ_meblarski == 'formatka' and record.plyta_bazowa and record.plyta_bazowa.kolor_manual:
            record.kolor_material = record.plyta_bazowa.kolor_manual
        elif record.kolor_manual:
            record.kolor_material = record.kolor_manual
        else:
            record.kolor_material = ""


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


def _compute_objetosc(self):
    """Oblicza objętość w m³ dla produktów meblarskich"""
    for record in self:
        if record.typ_meblarski in ['produkt_pojedynczy', 'zestaw'] and record.dlugosc_cm and record.szerokosc_cm and record.wysokosc_cm:
            # Konwersja z cm³ na m³
            record.objetosc_m3 = (record.dlugosc_cm * record.szerokosc_cm * record.wysokosc_cm) / 1000000
        else:
            record.objetosc_m3 = 0.0


def _compute_powierzchnia(self):
    """Oblicza powierzchnię w m² dla formatek i płyt"""
    for record in self:
        if record.typ_meblarski in ['formatka', 'plyta'] and record.dlugosc_cm and record.szerokosc_cm:
            # Konwersja z cm² na m²
            record.powierzchnia_m2 = (record.dlugosc_cm * record.szerokosc_cm) / 10000
        else:
            record.powierzchnia_m2 = 0.0


def _compute_show_sku(self):
    """Określa czy pokazać SKU - tylko dla produktów gotowych"""
    for record in self:
        record.show_sku_field = record.typ_meblarski in ['produkt_pojedynczy', 'zestaw', 'okucia', 'akcesoria']
