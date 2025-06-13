# -*- coding: utf-8 -*-
# Part of Alpma. See LICENSE file for full copyright and licensing details.


def action_assign_all_edges(self):
    """Przypisuje wybrane obrzeże do wszystkich 4 stron"""
    for record in self:
        if record.wszystkie_obrzeza:
            record.ok1_obrzeze = record.wszystkie_obrzeza
            record.ok2_obrzeze = record.wszystkie_obrzeza
            record.ok3_obrzeze = record.wszystkie_obrzeza
            record.ok4_obrzeze = record.wszystkie_obrzeza
